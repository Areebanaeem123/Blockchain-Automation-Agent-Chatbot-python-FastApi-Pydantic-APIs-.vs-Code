from langchain.tools import Tool
from tools.email_utils import send_alert_email

def set_price_alert_with_email(query):
    try:
        parts = query.split("::")
        coin = parts[0].strip().lower()
        threshold = float(parts[1].strip())
        email = parts[2].strip()
        # Send confirmation email
        success, message = send_alert_email(email, coin, threshold)
        if success:
            return f"✅ Price alert set for {coin} at ${threshold:,}. {message}"
        else:
            return f"⚠️ Alert not fully confirmed. {message}"

    except Exception as e:
        return f"❌ Error processing alert: {e}"

price_alert_tool = Tool(
    name="EmailPriceAlertSetter",
    func=set_price_alert_with_email,
    description="Set a crypto price alert and send confirmation to user email. Input should be 'coin::threshold::email'"
)
