import requests
import time
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- BİLGİLERİN ---
TELEGRAM_TOKEN = "8570142293:AAH6Nh5yY7i8NPE8hTVway-AD5YPg9qYLMk"
CHAT_ID = "1557082529"
WALLET_TO_WATCH = "E1zGzPY1WdJoHSzf928NWTkZjcAhnUaN1xzF6BhCTsvS"
HELIUS_API_KEY = "0942caa0-5fa4-4fd2-99d7-0a18897f9b31"

# Render'ın kapanmaması için basit bir web sunucusu
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Calisiyor!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try: requests.post(url, data=payload)
    except: pass

def start_bot():
    last_seen_tx = None
    print("🔍 Takip başlatıldı...")
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
                        msg = f"🟢 <b>YENİ HAREKET!</b>\n\n{desc}\n\n🔗 <a href='https://solscan.io/tx/{current_tx}'>Solscan</a>"
                        send_telegram(msg)
                    last_seen_tx = current_tx
        except Exception as e: print(f"Hata: {e}")
        time.sleep(10)

# Hem web sunucusunu hem botu aynı anda başlat
if __name__ == "__main__":
    threading.Thread(target=run_health_server, daemon=True).start()
    start_bot()
