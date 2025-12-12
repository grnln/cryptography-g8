import csv
from datetime import datetime
from .models import EMR, Checksum, BlockTag
from .integrity import hash_emr, compute_emr_string_hash, tag_gen

p = 1019  # 1019 ≡ 3 (mod 4), SECRET TO CLIENT
q = 2027  # 2027 ≡ 3 (mod 4), SECRET TO CLIENT
N = p * q # PUBLIC
g = 2 # PUBLIC

def parse_csv_to_emr_list(csv_path):
    emr_list = []
    checksum_list = []
    emr_string_list = []
    Checksum.objects.all().delete()
    EMR.objects.all().delete()
    BlockTag.objects.all().delete()

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

            emr_string_list.append((idx, compute_emr_string_hash(emr_obj)))
            emr_list.append(emr_obj)
            checksum_list.append(checksum)
    EMR.objects.bulk_create(emr_list)
    Checksum.objects.bulk_create(checksum_list)
    tag_gen(N, g, emr_string_list)
    return emr_list
