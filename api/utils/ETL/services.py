import subprocess
import pandas as pd
import io
import os
import math

RPC_URL = os.getenv("RPC_URL")

# ERC 주요 메서드 시그니처
TOKEN_TRANSFER_METHODS = {
    # ERC-20
    "0xa9059cbb": "erc20_transfer",  # transfer(address,uint256)
    "0x23b872dd": "erc20_transferFrom",  # transferFrom(address,address,uint256)

    # ERC-721
    "0x42842e0e": "erc721_safeTransferFrom",  # safeTransferFrom(address,address,uint256)
    "0xb88d4fde": "erc721_safeTransferFrom_data",  # safeTransferFrom(address,address,uint256,bytes)

    # ERC-1155
    "0xf242432a": "erc1155_safeTransferFrom",  # safeTransferFrom(address,address,uint256,uint256,bytes)
    "0x2eb2c2d6": "erc1155_safeBatchTransferFrom",  # safeBatchTransferFrom(address,address,uint256[],uint256[],bytes)
}

# Swap 함수 시그니처 (Uniswap, Curve 등)
SWAP_METHODS = {
    # Uniswap V2 (and SushiSwap, etc.)
    "0x38ed1739": "uniswap_v2_swapExactTokensForTokens",
    "0x18cbafe5": "uniswap_v2_swapExactETHForTokens",
    "0x8803dbee": "uniswap_v2_swapTokensForExactTokens",
    "0x7ff36ab5": "uniswap_v2_swapExactETHForTokens",
    "0x4a25d94a": "uniswap_v2_swapTokensForExactETH",
    "0xfb3bdb41": "uniswap_v2_swapETHForExactTokens",
    "0x42712a67": "uniswap_v2_swapExactTokensForETH",

    # Uniswap V3
    "0x414bf389": "uniswap_v3_exactInput",
    "0x2e95b6c8": "uniswap_v3_exactOutput",
    "0xf28c0498": "uniswap_v3_exactInputSingle",
    "0x09b81346": "uniswap_v3_exactOutputSingle",

    # Curve
    "0x5c11d795": "curve_exchange",
    "0x3df02124": "curve_exchangeUnderlying",
    "0xa6417ed6": "curve_exchangeMultiple",

    # Balancer
    "0x52bbbe29": "balancer_swap",
    "0x8a8c523c": "balancer_batchSwap",
}

# Bridge 함수 시그니처
BRIDGE_METHODS = {
    # Multichain
    "0x44bc937b": "multichain_anySwapOutUnderlying",
    "0xf7d8c883": "multichain_anySwapOut",
    "0x79f89197": "multichain_anySwapOutNative",

    # Hop
    "0x1c411e9a": "hop_swapAndSend",

    # Polygon PoS Bridge
    "0x2e1a7d4d": "polygon_withdraw",

    # Arbitrum
    "0x8c8c7f8a": "arbitrum_outboundTransfer",

    # Optimism
    "0x94b576de": "optimism_depositERC20",
    "0x3b4b138c": "optimism_withdraw",

    # Stargate
    "0x617ba037": "stargate_swap",
}


def get_transaction_trace(start_block, end_block):
    result_json = _fetch_blocks_and_txs(start_block, end_block)
    _tag_transaction_type(result_json)
    return result_json


# ETL 활용하여 블록, 트랜잭션 데이터 추출 함수
def _fetch_blocks_and_txs(start_block, end_block):
    result_json = {"blocks": [], "transactions": []}

    cmd = _get_cmd(start_block, end_block, RPC_URL)
    result = _run_script(cmd)
    output = _validation_block_process(result)

    if output is None:
        return result_json

    block_lines, tx_lines = _get_data(output)

    _validation_block(block_lines, result_json)
    _validation_transaction(result_json, tx_lines)

    return _sanitize_floats(result_json)


def _get_data(output):
    current = None
    block_lines, tx_lines = [], []

    for line in output:
        if line.startswith("number,hash"):
            current = "block"
        elif line.startswith("hash,nonce"):
            current = "tx"

        if current == "block":
            block_lines.append(line)
        elif current == "tx":
            tx_lines.append(line)

    return block_lines, tx_lines


def _get_cmd(start_block, end_block, rpc_url):
    return [
        "ethereumetl",
        "export_blocks_and_transactions",
        "--start-block", str(start_block),
        "--end-block", str(end_block),
        "--provider-uri", rpc_url,
        "--blocks-output", "-",
        "--transactions-output", "-",
        "--batch-size", "10",
        "--max-workers", "5"
    ]


def _run_script(cmd):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def _validation_block_process(result):
    if result.returncode != 0:
        print(f"블록 처리 실패:", result.stderr.strip())
        return None

    if not result.stdout.strip():
        print(f"블록 출력이 비었습니다.")
        return None

    return result.stdout.strip().splitlines()


def _validation_transaction(result_json, tx_lines):
    if tx_lines:
        try:
            txs_df = pd.read_csv(io.StringIO("\n".join(tx_lines)))
            txs_df = _replace_invalid_numbers(txs_df)
            result_json["transactions"] = txs_df.to_dict(orient="records")
        except Exception as e:
            print(f"트랜잭션 CSV 파싱 오류:", e)


def _validation_block(block_lines, result_json):
    if block_lines:
        try:
            blocks_df = pd.read_csv(io.StringIO("\n".join(block_lines)))
            blocks_df = _replace_invalid_numbers(blocks_df)
            result_json["blocks"] = blocks_df.to_dict(orient="records")
        except Exception as e:
            print(f"블록 CSV 파싱 오류:", e)


def _replace_invalid_numbers(df: pd.DataFrame):
    return df.replace([float("inf"), -float("inf")], None).where(pd.notnull(df), None)


def _sanitize_floats(data):
    if isinstance(data, dict):
        return {k: _sanitize_floats(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_sanitize_floats(v) for v in data]
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None
    return data


def _tag_transaction_type(result_json):
    filtered_txs = []

    for tx in result_json.get("transactions", []):
        value = int(tx.get("value", 0)) if tx.get("value") else 0
        input_data = str(tx.get("input", "")).lower()

        tx_type = None

        if value > 0:
            tx_type = "native"
        elif input_data and input_data != "0x":
            selector = input_data[:10]
            if selector in TOKEN_TRANSFER_METHODS:
                tx_type = TOKEN_TRANSFER_METHODS[selector]
            elif selector in SWAP_METHODS:
                print(SWAP_METHODS[selector])
                tx_type = SWAP_METHODS[selector]
            elif selector in BRIDGE_METHODS:
                print(BRIDGE_METHODS[selector])
                tx_type = BRIDGE_METHODS[selector]

        if tx_type:
            tx["tx_type"] = tx_type
            filtered_txs.append(tx)

    result_json["transactions"] = filtered_txs
