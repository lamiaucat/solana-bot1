import requests
import time
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- KİŞİSEL BİLGİLERİN ---
TELEGRAM_TOKEN = "8570142293:AAH6Nh5yY7i8NPE8hTVway-AD5YPg9qYLMk"
CHAT_ID = "1557082529"
WALLET_TO_WATCH = "E1zGzPY1WdJoHSzf928NWTkZjcAhnUaN1xzF6BhCTsvS"
HELIUS_API_KEY = "0942caa0-5fa4-4fd2-99d7-0a18897f9b31"

# 1. RENDER PORT HATASINI ÇÖZEN SUNUCU
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Bot Aktif ve Calisiyor!")

def run_health_server():
    # Render'ın verdiği portu kullan, yoksa 10000 kullan
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"✅ Web Sunucusu Başlatıldı - Port: {port}")
    server.serve_forever()

# 2. ASIL TAKİP BOTU FONKSİYONU
def start_wallet_watcher():
    last_seen_tx = None
    print(f"🔍 Takip Başlatıldı: {WALLET_TO_WATCH}")
    
    while True:
        try:
            url = f"https://api.helius.xyz/v0/addresses/{WALLET_TO_WATCH}/transactions?api-key={HELIUS_API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                txs = response.json()
                if txs:
                    current_tx = txs[0].get('signature')
                    if last_seen_tx is not None and current_tx != last_seen_tx:
                        desc = txs[0].get('description', 'Yeni İşlem!')
                        msg = f"🟢 <b>YENİ HAREKET!</b>\n\n{desc}\n\n🔗 <a href='https://solscan.io/tx/{current_tx}'>Solscan</a>"
                        # Telegram'a gönder
                        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                                      data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})
                        print(f"✅ Bildirim Gönderildi: {current_tx}")
                    last_seen_tx = current_tx
        except Exception as e:
            print(f"Hata: {e}")
        time.sleep(15) # 15 saniyede bir kontrol et

# 3. ANA ÇALIŞTIRICI
if __name__ == "__main__":
    # Web sunucusunu ayrı bir kolda (thread) başlat ki botu engellemesin
    threading.Thread(target=run_health_server, daemon=True).start()
    # Botu başlat
    start_wallet_watcher()
