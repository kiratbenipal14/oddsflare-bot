import requests
from bs4 import BeautifulSoup
import time
from config import TELEGRAM_TOKEN, TELEGRAM_USER_ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")

def check_live_matches():
    try:
        response = requests.get('https://www.cricbuzz.com/cricket-match/live-scores', timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = soup.find_all('div', class_='cb-mtch-lst cb-col cb-col-100 cb-tms-itm')

        alerts = []
        for match in matches:
            title = match.find('a').text.strip()
            status = match.find('div', class_='cb-text-live').text.strip() if match.find('div', class_='cb-text-live') else ''
            
            if 'wicket' in status.lower() or 'out' in status.lower() or 'collapse' in status.lower():
                alerts.append(f"Wicket/Collapse Alert: {title} | {status}")

            if 'six' in status.lower() or 'four' in status.lower():
                alerts.append(f"Big Hit Alert: {title} | {status}")

            if 'powerplay' in title.lower() and 'collapse' in status.lower():
                alerts.append(f"Powerplay Collapse Warning: {title} | {status}")

        return alerts

    except Exception as e:
        print(f"Error checking matches: {e}")
        return []

if __name__ == "__main__":
    alerts = check_live_matches()
    if alerts:
        for alert in alerts:
            send_telegram_message(alert)
    else:
        send_telegram_message("No flips detected yet. Bot is monitoring...")
