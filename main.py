import logging
import time
import random
import re
import threading
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from elasticsearch import Elasticsearch

# --- CONFIGURATION ---
LOG_FILE = 'server_logs.log'
ES_HOST = "http://localhost:9200"
THRESHOLD = 3

# --- EMAIL CONFIG (Debug Server) ---
SMTP_SERVER = 'localhost'
SMTP_PORT = 1025
SENDER_EMAIL = 'security@soc.com'
RECEIVER_EMAIL = 'admin@company.com'

# ---- CONNECT TO DATABASE ----
es = None
try:
    es = Elasticsearch(ES_HOST)
    if es.ping():
        print("[SYSTEM] ✅ Connected to Elasticsearch")
    else:
        print("[SYSTEM] ⚠️  Elasticsearch is running but not ready (Wait a moment)")
        es = None
except Exception as e:
    print(f"[SYSTEM] ❌ Connection Failed: {e}")
    es = None

# --- 1. LOG GENERATOR (Simulates Traffic) ---
def run_generator():
    logger = logging.getLogger('generator')
    logger.setLevel(logging.INFO)
    open(LOG_FILE, 'w').close() # Clear old logs
    
    handler = logging.FileHandler(LOG_FILE)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    
    users = ['admin', 'dhruv', 'manager', 'guest']
    ips = ['192.168.1.50', '10.0.0.12', '172.16.5.9', '8.8.8.8']

    print("[GENERATOR] Traffic simulation started...")
    while True:
        user = random.choice(users)
        ip = random.choice(ips)
        
        # 20% Chance of Attack Pattern
        if random.random() < 0.2:
            for _ in range(random.randint(3, 5)):
                logger.info(f"Login Failed - User: {user} - IP: {ip} - Status: 401 Unauthorized")
                time.sleep(0.3)
        else:
            logger.info(f"Login Success - User: {user} - IP: {ip} - Status: 200 OK")
        
        time.sleep(random.randint(2, 5))

# --- 2. EMAIL ALERT ---
def send_email(user, ip, count):
    msg = MIMEText(f"CRITICAL: User '{user}' failed {count} logins from IP {ip}.\nEvent logged to ELK.")
    msg['Subject'] = f"🚨 Brute Force Detected: {user}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
        print(f" [📧] Email Alert Sent to {RECEIVER_EMAIL}")
    except:
        print(f" [❌] Email Failed (Ensure Debug Server is running)")

# --- 3. SECURITY MONITOR (Core Logic) ---
def run_monitor():
    print("[MONITOR] Watching logs for attacks...")
    log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - .* User: (\w+) - IP: ([\d\.]+) - Status: (\d{3} \w+)')
    failed_attempts = {}

    with open(LOG_FILE, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            match = log_pattern.search(line)
            if match:
                timestamp, user, ip, status = match.groups()

                # A. Send to Kibana (Live Traffic)
                if es:
                    doc = {
                        "timestamp": datetime.now(),
                        "user": user,
                        "ip": ip,
                        "status": status,
                    }
                    try: es.index(index="server-traffic", document=doc)
                    except: pass

                # B. Detect Attacks
                if "401" in status:
                    failed_attempts[user] = failed_attempts.get(user, 0) + 1
                    print(f" -> Warning: {user} failed ({failed_attempts[user]}/{THRESHOLD})")
                    
                    if failed_attempts[user] >= THRESHOLD:
                        print(f" [!!!] ALERT: Brute Force by {user}")
                        send_email(user, ip, failed_attempts[user])
                        
                        # Log Critical Alert to Kibana
                        if es:
                            es.index(index="security-alerts", document={
                                "timestamp": datetime.now(),
                                "user": user,
                                "type": "BRUTE_FORCE",
                                "severity": "HIGH"
                            })
                        failed_attempts[user] = 0
                else:
                    if user in failed_attempts: failed_attempts[user] = 0

if __name__ == "__main__":
    t = threading.Thread(target=run_generator, daemon=True)
    t.start()
    time.sleep(1)
    run_monitor()
