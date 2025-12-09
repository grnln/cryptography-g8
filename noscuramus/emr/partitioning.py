from .models import *
from .clustering import *
from .emr_parser import *

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

import anonypy, pandas

aes = AES.new(get_random_bytes(32), AES.MODE_EAX)

def cypher_text(t):
    return aes.encrypt(bytearray(t, encoding = 'utf-8'))

def vertical_partition(t):
    tp = []
    te = []
    ta = []

    # Obtain Te and Tp
    for i in range(len(t)):
        emr = t[i]

        # Add all AES-encrypted EIDs and QIDs to Te
        encrypted_id = EncryptedID(
            name = cypher_text(emr.name),
            national_id = cypher_text(emr.national_id),
            social_security_number = cypher_text(emr.social_security_number),
            sex = cypher_text(emr.sex),
            postal_code = cypher_text(emr.postal_code),
            birth_date = cypher_text(str(emr.birth_date)),
            hospitalization_date = cypher_text(str(emr.hospitalization_date))
        )
        te.append(encrypted_id)
    
        # Add all medical information to Tp, verbatim
        medical_info = MedicalInfo(
            diagnosis = emr.diagnosis,
            treatment = emr.treatment,
            results = emr.results
        )
        tp.append(medical_info)

    # clusters = create_clusters(create_semantic_entries(t))
    
    qids = [[t[i].sex, t[i].postal_code, t[i].birth_date, t[i].hospitalization_date] for i in range(len(t))]
    columns = ['sex', 'postal_code', 'birth_date', 'hospitalization_date']
    
    frame = pandas.DataFrame(data = qids, columns = columns)
    frame = frame.astype({'sex': 'category', 'postal_code': 'int', 'birth_date': 'datetime64[ns]', 'hospitalization_date': 'datetime64[ns]'})
    
    preserver = anonypy.Preserver(frame, columns, 'sex')
    anon_qids = preserver.anonymize_k_anonymity(k = 2)

    for qid in anon_qids:
        anon_qid = AnonQID(
            sex = qid['sex'],
            postal_code = qid['postal_code'][0],
            birth_date = qid['birth_date'][0],
            hospitalization_date = qid['hospitalization_date'][0]
        )

        for i in range(qid['count']):
            ta.append(anon_qid)

    MedicalInfo.objects.bulk_create(tp)
    EncryptedID.objects.bulk_create(te)
    AnonQID.objects.bulk_create(ta)

    return (tp, te, ta)