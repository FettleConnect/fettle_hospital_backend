# Fettle Analytics Backend

Fettle Backend is a high-performance, Django-powered healthcare engagement platform. It orchestrates AI-driven patient communications via inbound and outbound voice calls, generates clinical insights from transcripts, and provides comprehensive analytics for hospital administrators.

---

## 🏗️ System Architecture

The system is built on a distributed microservices architecture coordinated via Docker:

1.  **Django API (Web/Celery)**: The core brain. It handles hospital management, patient data, and triggers call tasks.
2.  **LiveKit Server**: Manages real-time WebRTC sessions and agent dispatching.
3.  **LiveKit SIP Bridge**: Bridges traditional telephony (PSTN) from Vobiz/CloudConnect into LiveKit WebRTC rooms.
4.  **Voice Agent (Host-based)**: A Python-based worker using the LiveKit Agents SDK. It handles STT (Deepgram/Soniox), LLM (OpenAI GPT-4o), and TTS (Cartesia).
5.  **Redis**: Acts as the message broker for Celery and the state store for LiveKit (Trunks, Rules, and Room metadata).
6.  **PostgreSQL**: The persistent relational store for patients, hospitals, and call records.

### Call Flow Logic
*   **Outbound**: `call.py` (or Celery) -> LiveKit API -> SIP Trunk (Vobiz) -> Patient.
*   **Inbound**: Patient -> Vobiz -> SIP Bridge (Port 5061) -> Dispatch Rule -> LiveKit Room -> Voice Agent.

---

## 📂 Project Structure

```text
├── app/                # Core models (Hospital, Patient) and clinical dashboard APIs
├── phone_calling/      # SIP orchestration, LiveKit integration, and call tasks
├── inbound_dashboard/  # Specialized analytics for inbound call performance
├── chatbot/            # LangGraph-based dermatology patient assistant
├── docs/               # Technical documentation and Voice Agent source code
│   ├── agent_v2.py     # The primary Voice AI Agent implementation
│   └── DEVOPS.md       # Hard-earned lessons on SIP and LiveKit networking
├── config/             # Configuration files
│   ├── livekit/        # livekit.yaml and sip.yaml
│   └── tls/            # SSL certificates for production
├── docker/             # Specialized Dockerfiles for LiveKit components
└── manage.py           # Django management entrypoint
```

---

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Python 3.12+ (for host-based agent)
*   LiveKit CLI (`lk`) installed on host

### Development Setup
1.  **Clone and Env**:
    ```bash
    cp .env.dev.example .env.dev
    # Update keys for OpenAI, Deepgram, Cartesia, and Vobiz
    ```
2.  **Start Services**:
    ```bash
    docker compose --profile dev up -d
    ```
3.  **Migrations**:
    ```bash
    docker compose exec web python manage.py migrate
    ```

---

## 🚢 Production Details & Deployment

### Server Information
*   **Primary Node**: `165.232.185.104` (DigitalOcean)
*   **Access**: Root access via `fettle_ssh.key`
*   **Certificates**: Managed by Let's Encrypt at `/etc/letsencrypt/live/hospital.fettleconnect.com/`

### Critical Production Nuances
*   **SIP Persistence**: Never run `docker compose down` without ensuring the `redisdata` volume is preserved. If lost, SIP trunks must be recreated via `lk sip create`.
*   **Networking**: Both `livekit-server` and `livekit-sip` MUST use `network_mode: host`.
*   **UDP Port Range**: Ports `50000-60000` MUST be open in the Cloud Firewall for WebRTC media.
*   **Agent Identity**: The agent name is strictly defined as `my-agent`. This must match in `agent_v2.py`, `livekit_calling.py`, and the SIP Dispatch Rule.

### Deployment Steps
1.  **Sync Code**:
    ```bash
    git pull origin feature/hospital-platform-enhancements
    ```
2.  **Restart Stack**:
    ```bash
    docker compose -f docker-compose.yml --profile prod up -d --build
    ```
3.  **Restart Voice Agent**:
    ```bash
    systemctl restart fettle-agent
    ```

---

## 🚨 Troubleshooting & Lessons Learned

### "Ghost Trunks" (404 Error)
If outbound calls return a 404, the SIP Trunk was likely wiped from Redis. Use the reconstruction script in `docs/DEVOPS.md` to restore IDs.

### "Multiple Voices" (Overlapping Agents)
If you hear two agents talking, it means a rogue agent worker is running. Ensure only **one** instance of `fettle-agent.service` is active and no `python docs/agent_v2.py` processes are stuck in Docker.

### "Not Available" (Inbound Rings but doesn't answer)
Ensure the SIP Dispatch Rule contains the `room_config` block. If it's missing, LiveKit won't trigger the agent to join the room.

---

## 🤝 Contributing
1.  Create a branch from `develop`.
2.  Follow `PEP8` for Python and ensure all new APIs are registered in `project/urls.py`.
3.  **Strict Constraint**: Never push `DEBUG=True` or `127.0.0.1` URLs to the `.env.prod` configuration.

---

*For deep technical details on SIP signaling and media handshake fixes, refer to [docs/DEVOPS.md](./docs/DEVOPS.md).*
