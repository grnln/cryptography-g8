from django.db import models

class EMR(models.Model):
    id = models.BigAutoField(primary_key = True)

    name = models.CharField(max_length = 255)
    national_id = models.CharField(max_length = 255)
    social_security_number = models.CharField(max_length = 255)

    sex = models.CharField(max_length = 255)
    postal_code = models.CharField(max_length = 255)
    birth_date = models.DateField()
    hospitalization_date = models.DateField()

    diagnosis = models.CharField(max_length = 255)
    treatment = models.TextField()
    results = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.national_id}"

class MedicalInfo(models.Model):
    id = models.BigAutoField(primary_key=True)

    diagnosis = models.CharField(max_length=255)
    treatment = models.TextField()
    results = models.TextField()

    def __str__(self):
        return f'{self.diagnosis} - {self.treatment}'

class AnonQID(models.Model):
    id = models.BigAutoField(primary_key=True)
    
    sex = models.CharField(max_length=1)
    postal_code = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=255)
    hospitalization_date = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.sex} - {self.postal_code} - {self.birth_date} - {self.hospitalization_date}'

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
        return f'{self.name} - {self.national_id}'

from dataclasses import dataclass
from datetime import date

@dataclass
class AnonMergedData:
    sex: str
    postal_code: str
    birth_date: str
    hospitalization_date: str

    diagnosis: str
    treatment: str
    results: str

    def __str__(self):
        return f"{self.sex} - {self.postal_code} - {self.diagnosis}"

@dataclass
class MergedData:
    sex: str
    postal_code: str
    birth_date: date
    hospitalization_date: date

    diagnosis: str
    treatment: str
    results: str

    def __str__(self):
        return f"{self.sex} - {self.birth_date} - {self.diagnosis}"
