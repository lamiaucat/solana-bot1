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

# Render'ın beklediği kapıyı (port) açan mini sunucu
class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot Aktif!")

def run_web_server():
    # Render her zaman 'PORT' isimli bir değişken gönderir
    port = int(os.environ.get("PORT", 8080)) 
    server = HTTPServer(('0.0.0.0', port), SimpleServer)
    print(f"--- Sunucu {port} portunda baslatildi ---")
    server.serve_forever()

def start_watching():
    last_tx = None
    print(f"--- Takip Baslatildi: {WALLET_TO_WATCH} ---")
    while True:
        try:
            url = f"https://api.helius.xyz/v0/addresses/{WALLET_TO_WATCH}/transactions?api-key={HELIUS_API_KEY}"
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                if data:
                    current = data[0].get('signature')
                    if last_tx and current != last_tx:
                        msg = f"🟢 <b>HAREKET!</b>\n\n{data[0].get('description')}\n\n🔗 <a href='https://solscan.io/tx/{current}'>Solscan</a>"
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})
                    last_tx = current
        except: pass
        time.sleep(20)

if __name__ == "__main__":
    # ÖNCE web sunucusunu başlatıyoruz ki Render hata vermesin
    threading.Thread(target=run_web_server, daemon=True).start()
    start_watching()
