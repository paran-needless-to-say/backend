# core/screen/services.py

def get_next_hops(address, network, max_hops):
    return {
        "summary": "BRIDGE_TO_MIXER",
        "contrib": {"recency": 0.41, "hop": 0.36, "same_denom": 0.23},
        "evidence": [
            {
                "type": "tx",
                "hash": "0x..1",
                "label": "bridge_out",
                "ts": "2025-08-31T23:10Z",
                "url": "https://..."
            },
            {
                "type": "tx",
                "hash": "0x..2",
                "label": "mixer_deposit",
                "ts": "2025-08-31T23:45Z",
                "url": "https://..."
            }
        ],
        "metrics": {"dt_minutes": 35, "amount_delta_pct": 0.18},
        "risk": "RED",
        "rule_ids": ["T1_BRIDGE_MIXER_s45M", "T2_SAME_DENOM_s1PCT"],
        "policy_version": "v0.3.2",
        "decision_id": "dec_demo_red"
    }
