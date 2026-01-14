import requests
import time

# --- BİLGİLERİN ---
TELEGRAM_TOKEN = "8570142293:AAH6Nh5yY7i8NPE8hTVway-AD5YPg9qYLMk"
CHAT_ID = "1557082529"
WALLET_TO_WATCH = "E1zGzPY1WdJoHSzf928NWTkZjcAhnUaN1xzF6BhCTsvS"
HELIUS_API_KEY = "0942caa0-5fa4-4fd2-99d7-0a18897f9b31"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except:
        pass

last_seen_tx = None
print("🔍 Takip başlatıldı (Render üzerinden)...")

while True:
    try:
        url = f"https://api.helius.xyz/v0/addresses/{WALLET_TO_WATCH}/transactions?api-key={HELIUS_API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            transactions = response.json()
            if transactions:
                current_tx = transactions[0].get('signature')
                if last_seen_tx is not None and current_tx != last_seen_tx:
                    desc = transactions[0].get('description', 'Yeni İşlem!')
                    icon = "🟢" if "buy" in desc.lower() or "swap" in desc.lower() else "🔴"
                    msg = f"{icon} <b>YENİ HAREKET!</b>\n\n{desc}\n\n🔗 <a href='https://solscan.io/tx/{current_tx}'>Solscan</a>"
                    send_telegram(msg)
                    print(f"✅ Bildirim gönderildi: {current_tx}")
                last_seen_tx = current_tx
    except Exception as e:
        print(f"Hata: {e}")
    time.sleep(10) # 
