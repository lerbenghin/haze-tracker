import os
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def get_psi():
    resp = requests.get("https://api-open.data.gov.sg/v2/real-time/api/psi", timeout=10)
    resp.raise_for_status()
    item = resp.json()["data"]["items"][0]
    readings = item["readings"]["psi_twenty_four_hourly"]
    timestamp = item["timestamp"]
    return readings, timestamp


def get_pm25():
    resp = requests.get(
        "https://api-open.data.gov.sg/v2/real-time/api/pm25", timeout=10
    )
    resp.raise_for_status()
    item = resp.json()["data"]["items"][0]
    readings = item["readings"]["pm25_one_hourly"]
    return readings


def format_message(psi_readings, timestamp, pm25_readings):
    lines = [f"💨 *PSI Update for Ler* ({timestamp})", "", "*24hr PSI:*"]
    for region, value in psi_readings.items():
        lines.append(f"{region.capitalize()}: {value}")
    lines.append("")
    lines.append("*Hourly PM2.5 (µg/m³):*")
    for region, value in pm25_readings.items():
        lines.append(f"{region.capitalize()}:{value}")
    return "\n".join(lines)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    r = requests.post(url, data=payload, timeout=10)
    print(r.status_code, r.text)  # add this line temporarily
    r.raise_for_status()


if __name__ == "__main__":
    psi_readings, timestamp = get_psi()
    pm25_readings = get_pm25()
    message = format_message(psi_readings, timestamp, pm25_readings)
    send_telegram(message)
    print("Sent: ", message)
