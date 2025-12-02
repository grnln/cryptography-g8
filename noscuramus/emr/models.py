from django.db import models

# Create your models here.

class MedicalInfo(models.Model):
    id = models.BigAutoField(primary_key=True)

    diagnosis = models.CharField(max_length=255)
    treatment = models.TextField()
    results = models.TextField()

    def __str__(self):
        return f'{{}}'

class AnonQID(models.Model):
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f'{{}}'

class EncryptedID(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.BinaryField()
    national_id = models.BinaryField()
    social_security_number = models.BinaryField()
    sex = models.BinaryField()
    postal_code = models.BinaryField()
    birth_date = models.BinaryField()
    hospitalization_date = models.BinaryField()
    
    def __str__(self):
        return f'{{}}'

from dataclasses import dataclass
from datetime import date

@dataclass
class EMR:
    id: int
    name: str
    national_id: str
    social_security_number: str
    sex: str
    postal_code: str
    birth_date: date
    hospitalization_date: date
    diagnosis: str
    treatment: str
    results: str

    def __str__(self):
        return f"{self.name} - {self.national_id}"
