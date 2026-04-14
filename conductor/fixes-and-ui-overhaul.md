# Plan: CI/CD Restoration, Networking Fixes, and UI/UX Overhaul

## Objective
Restore CI/CD functionality, fix production networking for Redis, ensure data integrity for doctor accounts, and upgrade the frontend UI/UX for the Transcripts tab.

## Key Files & Context
- **Backend**: `docker-compose.yml`, `scripts/reconstruct_sip.py`, `app/models.py`, `app/views.py`, `project/urls.py`, `run_tests.py` (to be created).
- **Frontend**: `src/components/dashboard/StaffManagement.tsx`, `src/components/dashboard/DoctorTranscripts.tsx`.

## Implementation Steps

### 1. Backend: CI/CD and Networking Fixes
- **Root Test Wrapper**: Create `run_tests.py` at the root as a compatibility wrapper for `tests/run_tests.py`. This ensures `.github/workflows/continuous-testing.yml` still works.
- **Redis Networking**: Update `docker-compose.yml` to attach `db`, `web`, `celery`, and `celery-prod` to the `main-network`. This allows all services to resolve the `redis` service name.
- **SIP Script Guard**: Modify `scripts/reconstruct_sip.py` to check for `None` results from `run_lk` before string concatenation in the cleanup phase.

### 2. Backend: Data Integrity & New Endpoints
- **Doctor Uniqueness**:
    - Update `Doctor_model` in `app/models.py` to make `mobile_number` unique and non-nullable (aligning with PWA primarily phone-keyed login).
    - Update `DoctorManagementView.post` in `app/views.py` to handle `get_or_create` logic using `mobile_no` as the primary unique key.
- **Transcript Download API**:
    - Implement `MediVoiceTranscriptDownloadView` in `app/views.py` to allow downloading raw transcripts as `.txt` files.
    - Register the endpoint in `project/urls.py` as `/api/medivoice/transcript/<uuid:session_id>/`.

### 3. Frontend: Bug Fixes & UI/UX Upgrade
- **StaffManagement Crash**: Fix the `availability.map` error by adding an `Array.isArray()` check before rendering availability details.
- **Transcripts Tab Overhaul**:
    - **Doctor List**: Replace the "Recent Consultations" sidebar with an "Available Doctors" list, styled like the current recent consultations cards. Clicking a doctor filters the sessions on the right.
    - **Patient Session List**: Redesign the right side to show a list of patient sessions for the selected doctor.
    - **Expand/Collapse**: Implement an intuitive expand/collapse UI for each session to reveal essential details (Diagnosis, Revisit Date).
    - **Download Buttons**: Add prominent buttons for "Download Transcript" and "Download Prescription" for each session, linking to the corresponding backend endpoints.
    - **Consistency**: Match the styling and color palette of the `pwa-plan` application.

## Verification & Testing
- **Local Tests**: Run `python run_tests.py` to verify CI/CD wrapper.
- **Linting**: Run `ruff check` and `black --check` to ensure all changes pass project standards.
- **Manual Verification**:
    - Check `hospital.fettleconnect.com` dashboard functionality.
    - Verify Doctor creation with unique phone numbers.
    - Test "Download Transcript" and "Download Prescription" buttons in the new Transcripts tab.
    - Verify that `nginx_static` can still reach the backend after network changes.
