import json
from pathlib import Path

def check_scam_address(address: str) -> str:
    try:
        # Load scam address DB
        db_path = Path("C:/Users/HP/scam-database/blacklist/address.json")
        with db_path.open("r", encoding="utf-8") as f:
            scam_data = json.load(f)

        address = address.lower().strip()

        if address in scam_data:
            label = scam_data[address].get("label", "Scam")
            return f"🚨 Address `{address}` is flagged as **{label}**."
        else:
            return f"✅ Address `{address}` appears clean (not found in ScamSniffer GitHub list)."

    except Exception as e:
        return f"❌ Error loading scam DB: {str(e)}"
result = check_scam_address("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
print(result)
