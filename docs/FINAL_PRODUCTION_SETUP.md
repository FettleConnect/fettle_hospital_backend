# Fettle Post-Migration Checklist & Production Setup

This document outlines the final steps required by the infrastructure administrator to finalize the CloudConnect SIP migration and ensure the automated analytics engine is fully functional.

## 1. Primary Documentation to Refer
- **`docs/livekit_asterisk_setup_steps.pdf`**: Follow this for the binary installation of Redis, LiveKit, and Asterisk 20.
- **`docs/ASTERISK_CONFIG.md`**: Refer to this for the specific configuration parameters (pjsip.conf, extensions.conf) required for CloudConnect production SIP headers.
- **`docs/missing_data_request.txt`**: Share this with the hospital management to calibrate the ROI calculations.

---

## 2. Infrastructure Action Items (Your End)

### **A. Asterisk & SIP Bridging**
The backend is ready, but the server needs the SIP PBX configured:
1. **Apply Configs**: Update `/etc/asterisk/pjsip.conf` and `/etc/asterisk/extensions.conf` using the templates in `docs/ASTERISK_CONFIG.md`.
2. **Security Groups**: Ensure the following AWS Security Group ports are open:
   - **UDP/TCP 7065**: CloudConnect SIP Signaling.
   - **UDP 10000 - 40000**: CloudConnect Media/RTP range.
   - **TCP 7880-7881**: LiveKit signaling.

### **B. LiveKit Cloud Webhook Setup**
To enable the **Automated Monitoring** (replacing the manual Process Calls button):
1. Log into your **LiveKit Dashboard**.
2. Navigate to **Settings > Webhooks**.
3. Set the Webhook URL to: `https://hospital.fettleconnect.com:8000/api/livekit_webhook/`.
4. Ensure the `room_finished` event is enabled.

### **C. WhatsApp Integration**
The code currently uses a placeholder function `cloudconnect_whatsapp_msg`. 
- **Action**: Provide the API endpoint and credentials for your Indian WhatsApp provider (e.g., CloudConnect, interakt, or Meta directly).
- **Current State**: It will print the message to the logs but won't send a physical message until the HTTP logic is finalized with your specific vendor.

---

## 3. Deployment Commands (Run on EC2)

```bash
cd /home/fettle_backend
git fetch origin master
git reset --hard origin/master
python manage.py migrate
sudo systemctl restart fettle_backend
sudo systemctl restart fettle_celery
```

## 4. Systemd Service Templates

### **Backend (SSL Server)**
File: `/etc/systemd/system/fettle_backend.service`
```ini
[Unit]
Description=Django Fettle Backend Persistent Service
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/fettle_backend
ExecStart=/home/fettle_backend/env/bin/python manage.py runsslserver 0.0.0.0:8000 --certificate /home/fettle_backend/fullchain.pem --key /home/fettle_backend/privkey.pem
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### **Celery (Background Tasks)**
File: `/etc/systemd/system/fettle_celery.service`
```ini
[Unit]
Description=Celery Worker for Fettle Backend
After=network.target redis.service

[Service]
Type=forking
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/fettle_backend
EnvironmentFile=/home/fettle_backend/.env
ExecStart=/home/fettle_backend/env/bin/celery -A project worker -l info -P gevent --detach
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 5. Frontend Deployment
Since the GitHub push for the frontend failed (`Repository not found`), you must manually deploy the `dist/` folder generated on this local machine to your web server. 

**Key Frontend Features now live:**
- ROI Analytics Tab.
- Department Breakdown Table.
- Automated "In Progress" pulsing indicators in the Call Logging table.
- Campaign CRUD Manager.

---
*Documentation updated February 28, 2026.*
