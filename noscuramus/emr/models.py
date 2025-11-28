from django.db import models

# Create your models here.

class MedicalInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f'{{}}'

class AnonQID(models.Model):
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f'{{}}'

class EncryptedID(models.Model):
    id = models.BigAutoField(primary_key=True)
    def __str__(self):
        return f'{{}}'

class EMR(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{{}}'
