# 🛡️ Sentinel: Real-Time Log Monitoring & Intrusion Detection System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
![ELK Stack](https://img.shields.io/badge/Elasticsearch-7.17-orange?style=flat&logo=elastic)
![Kibana](https://img.shields.io/badge/Kibana-7.17-hotpink?style=flat&logo=kibana)
![Security](https://img.shields.io/badge/Focus-Cybersecurity-red?style=flat&logo=security)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview
**Sentinel** is a lightweight, real-time security auditing tool designed to detect **Brute Force Attacks** and unauthorized access attempts in server environments. 

By leveraging the power of **Python** for log parsing and the **ELK Stack (Elasticsearch & Kibana)** for visualization, this system provides a comprehensive dashboard for monitoring server health. It features an automated **Email Alerting System** that notifies administrators instantly when critical security thresholds are breached.

## 🚀 Key Features
* **🕷️ Intelligent Log Parsing:** Uses advanced Regex patterns to extract timestamp, user identity, IP address, and HTTP status codes from raw server logs.
* **🚨 Automated Intrusion Detection:** Automatically flags users who trigger multiple `401 Unauthorized` errors within a short time window (Brute Force Pattern).
* **📧 Real-Time Alerting:** Integrated SMTP client sends immediate email notifications to administrators with attack details (User, IP, Severity).
* **📊 Interactive Dashboard:** Visualizes attack vectors, login frequencies, and threat origins using **Kibana 7.17**.
* **💾 Persistent Logging:** All security incidents are indexed in **Elasticsearch** for historical analysis and forensic auditing.

## 🛠️ Technology Stack
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Core Logic** | Python 3.12 | Log generation, parsing, and detection algorithms. |
| **Database** | Elasticsearch 7.17 | NoSQL database for indexing parsed log data. |
| **Visualization** | Kibana 7.17 | Web-based dashboard for real-time graphs. |
| **Alerting** | `aiosmtpd` / `smtplib` | Custom SMTP handling for email notifications. |
| **Simulation** | Python `logging` | Generates realistic synthetic server traffic. |

## ⚙️ Architecture
1.  **Log Generation:** A Python thread simulates live server traffic (Status 200 vs 401).
2.  **Ingestion:** The **Monitor** reads the active log file in real-time (like `tail -f`).
3.  **Analysis:** Regex filters apply pattern matching to identify potential threats.
4.  **Action:**
    * **Safe Data:** Indexed to Elasticsearch for general traffic monitoring.
    * **Threat Data:** Triggers an Email Alert and logs a high-severity incident to Elasticsearch.
5.  **Visualization:** Kibana updates charts dynamically as new data arrives.

## 🔧 Installation & Setup

### 1. Prerequisites
* **Python 3.8+** installed.
* **Elasticsearch 7.17** & **Kibana 7.17** (Running locally).

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Log-Monitoring-System.git](https://github.com/YOUR_USERNAME/Log-Monitoring-System.git)
cd Log-Monitoring-System

3. Install Dependencies

pip install -r requirements.txt

4. Configure the Database (ELK)
Ensure your local Elasticsearch instance is running at http://localhost:9200.

Note: Security (xpack) should be disabled for this development version.

🖥️ Usage Guide
Step 1: Start the Fake Email Server (for Debugging)
Open a terminal and run:

Bash
python fake_email_server.py
This will listen for alert emails and print them to the console.

Step 2: Launch the System
Open a second terminal and run:

Bash

python main.py
This starts the Log Generator and the Security Monitor simultaneously.

Step 3: Visualize in Kibana
Open http://localhost:5601.

Navigate to Stack Management > Data Views.

Create a data view for server-traffic* (General Logs) and security-alerts* (Attacks).

Go to the Discover tab to see real-time data flow.

Author: Dhruv Kholia

Cybersecurity Enthusiast & Developer
