import os
import django
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.test import Client  # noqa: E402
from app.models import (  # noqa: E402
    Hospital_model,
    Doctor_model,
)
from project.jwt_auth import create_token  # noqa: E402


def run_e2e_tests():
    client = Client()

    print("--- Starting E2E Verification for Recent Fixes ---")

    # 1. Setup Test Data
    hospital, _ = Hospital_model.objects.get_or_create(
        name="Test Hospital", defaults={"reception_email": "test@reception.com"}
    )

    doctor, _ = Doctor_model.objects.get_or_create(
        email="testdoc@hospital.com",
        defaults={
            "hospital": hospital,
            "name": "Test Doctor",
            "password_hash": "testpass",
            "department": "General",
        },
    )

    # 2. Test Staff Availability Update (StaffManagement.tsx Fix)
    print("\n[TEST] Staff Availability API...")
    token = create_token(doctor.id, "doctor")
    availability_data = {"Monday": "10 AM - 4 PM", "Tuesday": "Off"}

    response = client.post(
        "/api/update_doctor_availability/",
        data={"availability": availability_data},
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    if response.status_code == 200:
        print("✅ Staff availability updated successfully.")
    else:
        print(f"❌ Staff availability update failed: {response.status_code}")

    # 3. Test Clinical Data Sync (MediVoice Sync Fix)
    print("\n[TEST] MediVoice Session Sync...")
    session_data = {
        "doctor_email": doctor.email,
        "patient_name": "E2E Patient",
        "patient_mobile": "1234567890",
        "diagnosis": "Fever",
        "medicines": [{"name": "Paracetamol", "dosage": "500mg"}],
        "revisit_date": "2026-05-01",
    }

    response = client.post(
        "/api/sync_medivoice_session/",
        data=session_data,
        content_type="application/json",
    )

    if response.status_code == 201:
        print("✅ MediVoice session synced successfully.")
        session_id = response.json()["session_id"]
        # Verify decouple (celery delay check placeholder)
        print(f"   (Session ID created: {session_id})")
    else:
        print(
            f"❌ MediVoice session sync failed: {response.status_code} - {response.content}"
        )

    # 4. Test PDF Generation (WeasyPrint Migration Fix)
    print("\n[TEST] PDF Generation View...")
    response = client.get(f"/api/generate_report_pdf/?hospital_name={hospital.name}")

    if response.status_code == 200 and response["Content-Type"] == "application/pdf":
        print("✅ PDF generated successfully via WeasyPrint.")
    else:
        print(f"❌ PDF generation failed: {response.status_code}")

    # 5. Test ROI Formula Fix
    print("\n[TEST] ROI Metrics Calculation...")
    # Seed a few calls and engagements for the hospital
    from app.models import CallFeedbackModel, Patient_model

    patient, _ = Patient_model.objects.get_or_create(
        hospital=hospital,
        mobile_no="9999999999",
        defaults={"patient_name": "ROI Patient", "department": "General"},
    )

    CallFeedbackModel.objects.create(
        patient=patient,
        call_status="connected",
        call_outcome="positive",
        revisit_encouraged=True,
    )

    response = client.get(f"/api/hospital_roi_metrics/?hospital_name={hospital.name}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ ROI Metrics retrieved: Conversions={data.get('total_conversions')}")
    else:
        print(f"❌ ROI Metrics failed: {response.status_code}")

    print("\n--- E2E Verification Complete ---")


if __name__ == "__main__":
    try:
        run_e2e_tests()
    except Exception as e:
        print(f"\nFATAL ERROR during E2E test: {e}")
        import traceback

        traceback.print_exc()
