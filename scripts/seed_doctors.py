import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from app.models import Hospital_model, Doctor_model  # noqa: E402


def seed_doctors():
    # 1. Get or create a Hospital
    hospital, created = Hospital_model.objects.get_or_create(
        name="Amor Hospitals", defaults={"reception_email": "reception@amor.com"}
    )
    if created:
        print(f"Created Hospital: {hospital.name}")

    # 2. Create Doctors
    doctors_data = [
        {
            "name": "Dr. Sumanth",
            "email": "sumanth@amor.com",
            "department": "Cardiology",
        },
        {"name": "Dr. Pranay", "email": "pranay@amor.com", "department": "Neurology"},
        {"name": "Dr. Kavya", "email": "kavya@amor.com", "department": "Dermatology"},
    ]

    for doc_data in doctors_data:
        doctor, d_created = Doctor_model.objects.get_or_create(
            email=doc_data["email"],
            defaults={
                "hospital": hospital,
                "name": doc_data["name"],
                "password_hash": "doctor123",  # Will be hashed on save
                "department": doc_data["department"],
                "availability": {
                    "Monday": "9 AM - 5 PM",
                    "Wednesday": "9 AM - 5 PM",
                    "Friday": "9 AM - 2 PM",
                },
            },
        )
        if d_created:
            print(f"Created Doctor: {doctor.name} ({doctor.department})")

    print("Doctor seeding completed successfully!")


if __name__ == "__main__":
    seed_doctors()
