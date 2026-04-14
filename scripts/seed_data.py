import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from app.models import (  # noqa: E402
    Hospital_model,
    Patient_model,
    EscalationModel,
    Patient_date_model,
    CallFeedbackModel,
    Hospital_user_model,
)
from datetime import date, timedelta  # noqa: E402
import random  # noqa: E402


def seed_data():
    # 1. Create a Hospital
    hospital, created = Hospital_model.objects.get_or_create(
        name="Apollo Hospital", defaults={"reception_email": "reception@apollo.com"}
    )
    if created:
        print(f"Created Hospital: {hospital.name}")

    # Ensure a hospital user exists with all permissions enabled
    hospital_user, user_created = Hospital_user_model.objects.get_or_create(
        name="hospital_user",
        defaults={
            "hospital": hospital,
            "password_hash": "hospital123",  # Will be hashed on save
            "patient_engagement": True,
            "community_egagement": True,
            "revisit_engagement": True,
            "escalation_engagement": True,
            "calllog_engagement": True,
            "upload_engagement": True,
            "pdf_engagement": True,
        },
    )
    if user_created:
        print(f"Created Hospital User: {hospital_user.name}")

    # 2. Create Patients
    departments = ["Cardiology", "Neurology", "Orthopedics", "Dermatology"]
    patient_names = [
        "John Doe",
        "Jane Smith",
        "Robert Brown",
        "Emily Davis",
        "Michael Wilson",
    ]

    patients = []
    for i, name in enumerate(patient_names):
        patient, p_created = Patient_model.objects.get_or_create(
            hospital=hospital,
            mobile_no=f"987654321{i}",
            department=random.choice(departments),
            defaults={
                "patient_name": name,
                "age": random.randint(20, 70),
                "serial_no": f"SR{100+i}",
            },
        )
        patients.append(patient)
        if p_created:
            print(f"Created Patient: {patient.patient_name}")

    # 3. Create Patient Date Records (History)
    today = date.today()
    for patient in patients:
        for d in range(1, 5):
            past_date = today - timedelta(days=d * 10)
            Patient_date_model.objects.get_or_create(
                hospital=hospital,
                mobile_no=patient.mobile_no,
                department=patient.department,
                date=past_date,
                defaults={
                    "patient_name": patient.patient_name,
                    "age": patient.age,
                    "serial_no": patient.serial_no,
                },
            )

    # 4. Create Call Feedback
    outcomes = ["positive", "negative", "escalated", "no_feedback"]
    for patient in patients:
        CallFeedbackModel.objects.create(
            patient=patient,
            call_status="connected",
            call_outcome=random.choice(outcomes),
            remarks="Follow up call completed.",
            community_added=random.choice([True, False]),
            revisit_encouraged=random.choice([True, False]),
            escalation_required=False,
            call_duration="5",
            called_by="AI Assistant",
        )

    # 5. Create Escalations
    for patient in patients[:2]:
        EscalationModel.objects.create(
            patient=patient,
            issue_description="Patient reported severe pain after medication.",
            status="pending",
            department=patient.department,
        )

    print("Seeding completed successfully!")


if __name__ == "__main__":
    seed_data()
