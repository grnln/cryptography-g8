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

class EMR(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=12, unique=True)
    social_security_number = models.CharField(max_length=20, unique=True)
    sex = models.CharField(max_length=1, choices=[('M','Male'),('F','Female')])
    postal_code = models.CharField(max_length=10)
    birth_date = models.DateField()
    hospitalization_date = models.DateField()
    diagnosis = models.CharField(max_length=255)
    treatment = models.TextField()
    results = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nombre} - {self.dni}"
