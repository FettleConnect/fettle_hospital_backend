import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import Hospital_model, Doctor_model

def seed_doctors():
    hospitals = Hospital_model.objects.all()
    if not hospitals.exists():
        print("No hospitals found. Please seed hospitals first.")
        return

    hospital = hospitals.first()
    
    doctors = [
        {
            "name": "Kishore B Reddy",
            "email": "kishore@amor.com",
            "department": "Orthopedics Oncology",
            "password": "doctorpassword"
        },
        {
            "name": "Imran Ul Haq",
            "email": "imran@amor.com",
            "department": "Cardiology",
            "password": "doctorpassword"
        }
    ]

    for d in doctors:
        Doctor_model.objects.update_or_create(
            email=d['email'],
            defaults={
                "hospital": hospital,
                "name": d['name'],
                "department": d['department'],
                "password_hash": make_password(d['password'])
            }
        )
        print(f"Seeded doctor: {d['name']}")

if __name__ == "__main__":
    seed_doctors()
