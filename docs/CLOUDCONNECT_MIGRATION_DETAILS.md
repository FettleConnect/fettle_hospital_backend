# Fettle Backend: CloudConnect SIP Migration Documentation

## 1. Executive Summary
The Fettle platform has migrated its voice telephony layer from **LiveKit (WebRTC)** to **CloudConnect (SIP)** using **Vapi.ai** as an orchestration bridge. This transition provides high-fidelity PSTN connectivity via an Indian static IP, ensuring regulatory compliance and reduced latency.

The system now operates on a **webhook-driven architecture**, where call initiation is triggered via API, and post-call processing (transcription, recording sync, AI analysis) is handled automatically upon call completion.

---

## 2. Architectural Overview

### **Old Flow (LiveKit)**
1.  Backend dispatches an agent into a WebRTC room.
2.  Audio/Transcripts are written to a LiveKit-specific S3 bucket.
3.  Admin manually triggers "Process Calls" to pull data and run analysis.

### **New Flow (CloudConnect + Vapi)**
1.  **Initiation:** Backend calls Vapi API with `VAPI_SIP_TRUNK_ID`.
2.  **Telephony:** Vapi routes the call through CloudConnect's SIP Trunk.
3.  **Real-time Logic:** Vapi manages the voice agent (STT/TTS/LLM) based on the configured Assistant.
4.  **Completion:** Once the call ends, Vapi sends an `end-of-call-report` webhook to the backend.
5.  **Automation:** The backend automatically:
    *   Downloads the `.wav` recording.
    *   Uploads transcript and audio to the standard `fettle-audio-transcript` S3 bucket.
    *   Triggers GPT-4o analysis (`json_audio`) to update feedback and escalations.

---

## 3. Configuration & Environment Settings

### **New Environment Variables (.env)**
Ensure the following keys are populated on the production server:
*   `VAPI_TOKEN`: Your Vapi.ai private API key.
*   `VAPI_SIP_TRUNK_ID`: The UUID of the CloudConnect SIP Trunk configured in the Vapi dashboard.
*   `SECRET_KEY`: Now supports a fallback to prevent initialization errors.

### **AWS Security Groups**
Since we use Vapi as a bridge, your server only needs to allow standard `HTTPS (443)` for webhooks. **UDP 5060 is not required** on the EC2 instance unless you choose to host your own SIP signaling server.

---

## 4. Modified Components

### **Backend (Django)**
*   **`phone_calling/views.py`**:
    *   `Outbound_call`: Updated to send `phoneNumberId` (SIP ID) and `language_policy` metadata.
    *   `VapiWebhook`: A new public endpoint that receives the call report and initiates the Celery task.
*   **`phone_calling/tasks.py`**:
    *   `process_vapi_webhook_task`: A robust new task that handles the "Surgical Sync." It mimics the previous manual process but runs automatically. It uses `pytz` for accurate IST timestamping.
*   **`app/models.py`**:
    *   Added `Campaign` model to persist batch metadata.
    *   Added `in_progress` to call status choices.

### **Frontend (React)**
*   **`AgentControl.tsx`**: A dedicated "Segment & Launch" interface.
*   **`CampaignManagement.tsx`**: A persistent CRUD manager for batches.
*   **`HospitalDashboard.tsx`**: Centralized state management for the global `DateRange` filter.

---

## 5. Guidance for Voice Agent Developers
If you are the developer of `voice_agent_code.py`, follow these steps to integrate your layer with the new CloudConnect backend:

### **Transitioning from LiveKit to Vapi**
Your LiveKit code (`AgentSession`, `rtc.connect`) is now handled by Vapi's infrastructure. To port your logic:

1.  **Assistant Definition:** Copy your `instructions` string into the **Vapi Assistant System Prompt**.
2.  **Provider Mapping:**
    *   **STT:** Set Vapi to use **Soniox** (as seen in your code).
    *   **TTS:** Set Vapi to use **Cartesia (Sonic-3)** with your specific `voiceId`.
3.  **Language Handling:** Your code uses `MultilingualModel`. In Vapi, you can use **Transcriber Languages** (English, Hindi, Telugu). 
    *   *Note:* The backend now passes a `language_policy` in the call metadata. Your Vapi Assistant should be configured to read `{{language_policy}}` to enforce the trilingual rule.
4.  **Metadata Loopback:** Ensure your Vapi Assistant configuration **forwards metadata**. The backend relies on `patient_id` and `hospital` being returned in the webhook to link the feedback to the correct record.
5.  **Tools:** If you add `@function_tool` in LiveKit, you must recreate them as **Vapi Tools** (Functions) and point the `Server URL` to your backend if they need to fetch real-time hospital data.

---

## 6. Verification Checklist
1.  [ ] **SIP Whitelisting:** Confirm CloudConnect has whitelisted your AWS Static IP.
2.  [ ] **Webhook URL:** Ensure Vapi Dashboard -> Settings -> Server URL is set to `https://hospital.fettleconnect.com:8000/api/vapi_webhook/`.
3.  [ ] **Migrations:** Run `python manage.py migrate` to create the `Campaign` tables.
4.  [ ] **Celery:** Restart the worker to enable the `process_vapi_webhook_task`.

*Documentation generated on February 24, 2026.*
