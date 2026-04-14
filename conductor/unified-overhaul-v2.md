# Unified Platform Overhaul V2

## Objective
Address persistent UI bugs, implement dual-key doctor auth, overhaul metrics reporting, integrate WhatsApp BSP, and enable call recordings with S3 storage.

## Key Changes

### 1. Frontend: Engagement & Staff UI (`frontend_fettel`)
- **CommunityEngagementMetrics.tsx**: Remove all charts (Growth, Department, Intents, Metrics) for both inbound and outbound to resolve the persistent "4 cards" bug.
- **PatientEngagementMetrics.tsx**: Remove the "Engagement Summary" card from the bottom.
- **StaffManagement.tsx**:
    - Add `email` input field to the "Add New Doctor" form.
    - Logic: Ensure either `mobile_no` OR `email` is provided.
    - Make `password` optional (default to system placeholder).
    - Display email in the staff table.

### 2. Backend: Clinical Reporting & Data Integrity (`fettle_backend`)
- **Doctor Model & View**:
    - Ensure `Doctor_model` enforces uniqueness for both email and phone.
    - Update `DoctorManagementView` to handle dual-key lookup and creation.
    - Populate PWA MongoDB `doctors` collection during CRUD.
- **Metrics Report Overhaul**:
    - Rewrite `PdfView` logic to strictly follow `docs/instructions.md` formulas.
    - Implement calculations for:
        - Total Interactions (Inbound + Outbound + Chat).
        - Avg Resolution Time.
        - Revenue Influenced (Appointments * ₹850).
        - Operational Efficiency (Staff hours saved).
- **Report Template**: Overhaul `report_template.html` to match the 8 sections defined in the instructions.

### 3. Backend: WhatsApp & Campaign Integration
- **Vobiz WhatsApp BSP**:
    - Implement REST API calls to `https://api.vobiz.ai/v1/messaging/send`.
    - Use `X-Auth-ID` and `X-Auth-Token` from env.
- **Prompt Injection**:
    - Modify `call_outbound_task` to fetch campaign templates.
    - Inject the template prompt/variables into the LiveKit Agent's room metadata.
- **Voice Agent Update**:
    - Update `docs/agent_v2.py` to read custom prompts from room metadata and override default instructions.

### 4. Backend: Call Recordings & S3
- **LiveKit Recording**: Update `dispatch_call` to trigger room recordings in MP3/OGG format.
- **S3 Lifecycle**: Configure S3 bucket naming and implement a 30-day refresh/cleanup task for recordings.

### 5. PWA API: CORS Final Fix
- **app.ts**: Refine the CORS middleware to explicitly handle `OPTIONS` preflights and ensure `hospital.fettleconnect.com` is permanently whitelisted.

## Verification
- **Outbound Test**: Call `+919003037804` using different campaign types.
- **Report Test**: Generate and verify the "Only Metrics" PDF against manual calculations.
- **Download Test**: Confirm "Download Prescription" and "Download Transcript" buttons resolve CORS.
- **Auth Test**: Log into PWA using email-only and phone-only accounts.
