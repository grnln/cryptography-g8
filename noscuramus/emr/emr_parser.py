import csv
from datetime import datetime
from .models import EMR, Checksum
from .integrity import hash_emr

def parse_csv_to_emr_list(csv_path):
    emr_list = []
    checksum_list = []
    Checksum.objects.all().delete()
    EMR.objects.all().delete()

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            birth_date = datetime.strptime(row['Fecha Nacimiento'], '%Y-%m-%d').date()
            hospitalization_date = datetime.strptime(row['Fecha Ingreso'], '%Y-%m-%d').date()

            emr_obj = EMR(
                id=idx,
                name=row['Nombre'],
                national_id=row['DNI'],
                social_security_number=row['NSS'],
                sex=row['Género'],
                postal_code=row['Código Postal'],
                birth_date=birth_date,
                hospitalization_date=hospitalization_date,
                diagnosis=row['Diagnóstico'],
                treatment=row['Tratamiento'],
                results=row['Resultados']
            )

            checksum = Checksum(
                id=idx,
                checksum=hash_emr(emr_obj).hex()
            )

            emr_list.append(emr_obj)
            checksum_list.append(checksum)
    EMR.objects.bulk_create(emr_list)
    Checksum.objects.bulk_create(checksum_list)
    return emr_list
