# Fettle Backend - Project Overview

Fettle Backend is a Django-based system designed for managing and analyzing hospital-to-patient communications. It automates both inbound and outbound calls using AI (Vapi.ai, LiveKit, OpenAI) to generate transcripts, summaries, and structured feedback for hospitals.

## 🚀 Technologies & Architecture

-   **Framework:** Django (Python) with Django Rest Framework (DRF).
-   **Authentication:** JWT (SimpleJWT).
-   **Database:** PostgreSQL (AWS RDS).
-   **Async Tasks:** Celery with Redis as the message broker.
-   **AI & Communication:** 
    -   **OpenAI:** For call analysis, summarization, and sentiment extraction.
    -   **Vapi.ai:** For automated outbound calling.
    -   **LiveKit:** For real-time voice agents (`agent_dispatch`).
    -   **CloudConnect:** For SIP telephony and Indian DIDs.
-   **Storage:** AWS S3 for audio files and transcripts.
-   **Data Processing:** `pandas` (reporting), `python-docx` (document generation), `docx2pdf`.

## 📁 Directory Structure

-   `project/`: Core Django configuration (`settings.py`, `urls.py`, `celery.py`).
-   `app/`: Core domain models (Hospital, Patient, Admin) and general dashboard APIs.
-   `phone_calling/`: Management of call tasks (inbound/outbound), LiveKit integration, and SIP orchestration.
-   `inbound_dashboard/`: Specialized views and analytics for inbound call performance.
-   `env/`: Python virtual environment (standard location).

## 🛠️ Commands

### Development
-   **Run Server (HTTP):** `python manage.py runserver`
-   **Run Server (HTTPS):** `python manage.py runsslserver` (required for some webhooks)
-   **Migrations:** `python manage.py migrate`
-   **Create Superuser:** `python manage.py createsuperuser`

### Background Tasks (Celery)
-   **Run Worker:** `celery -A project worker -l info -P gevent`
-   **Run Beat (Scheduler):** `celery -A project beat -l info`

### Testing
-   **Run Tests:** `python manage.py test`

## 📝 Development Conventions

-   **API First:** All new functionality should be exposed via DRF views in the `api/` namespace.
-   **Task Offloading:** Any operation involving external AI APIs (OpenAI, LiveKit) or document generation must be handled asynchronously via Celery.
-   **Environment Variables:** Sensitive keys (AWS, OpenAI, CloudConnect, LiveKit) are managed via `.env`. Do not hardcode secrets.
-   **Timezone:** The project uses `Asia/Kolkata` as the primary timezone, though Celery is configured for `Australia/Tasmania` (verify if this discrepancy is intentional).
-   **SSL:** Use `sslserver` for local development to ensure compatibility with real-time communication protocols.

## 🚨 DevOps & LiveKit SIP Lessons Learned

-   **Docker `--remove-orphans` & Redis Data:** LiveKit stores its entire state (including SIP Trunks and Dispatch Rules) in Redis. If Redis is deployed via Docker Compose without a mapped data volume (`volumes: - redisdata:/data`) and `--save` parameters, running `docker compose down` or `docker compose up -d --remove-orphans` will destroy the container and **permanently delete all SIP trunks and rules.** A `redisdata` volume must always be mounted in production.
-   **Agent Naming (`agent_name`):** 
    -   When using the `@server.rtc_session()` decorator, an empty agent name defaults to handling any dispatched job for that agent type.
    -   If you define `agent_name="my-agent"` in the `agent_v2.py` decorator, you **must** also pass `"my-agent"` in both the outbound `CreateAgentDispatchRequest` and the inbound `CreateSIPDispatchRule` (inside `room_config.agents`).
    -   Mismatches will result in "no worker available" errors, or conversely, leaving it empty everywhere can cause multiple agent workers to pick up the same job simultaneously, resulting in overlapping voices.
-   **SIP Trunk Passwords:** When creating trunks with passwords containing special characters (like `$`), passing them inline in bash can cause escaping bugs. Always prefer using the LiveKit Go API, Python SDK, or passing a structured JSON file to `lk sip outbound create` to ensure correct string literals.
-   **Docker Networking & SIP:** When `livekit-server` and `livekit-sip` run with `network_mode: host`, ensure `livekit.yaml` and `sip.yaml` have perfectly aligned `rtp_port` ranges (e.g., 50000-60000). Mismatched RTP ports result in signaling succeeding (`Status: 200`) but media timing out (`connect timeout after ICE connected`).
-   **Inbound Call Configuration:** To allow inbound calls to actually bridge to an agent, the SIP Dispatch Rule **must** contain a `room_config` block that explicitly defines the agent name. Otherwise, the call will sit in a ringing state in an empty room until the provider times out.
