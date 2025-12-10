from .models import *
from .clustering import *
from .emr_parser import *
from .cipher import *

import pandas
from .anonypy_custom import Preserver

def vertical_partition(t):
    tp = []
    te = []
    ta = []

    MedicalInfo.objects.all().delete()
    EncryptedID.objects.all().delete()
    AnonQID.objects.all().delete()

    # Obtain Te and Tp
    for i in range(len(t)):
        emr = t[i]

        # Add all AES-encrypted EIDs and QIDs to Te
        encrypted_id = EncryptedID(
            id = emr.id,
            name = cipher_text(emr.name),
            national_id = cipher_text(emr.national_id),
            social_security_number = cipher_text(emr.social_security_number),
            sex = cipher_text(emr.sex),
            postal_code = cipher_text(emr.postal_code),
            birth_date = cipher_text(str(emr.birth_date)),
            hospitalization_date = cipher_text(str(emr.hospitalization_date))
        )
        te.append(encrypted_id)
    
        # Add all medical information to Tp, verbatim
        medical_info = MedicalInfo(
            id = emr.id,
            diagnosis = emr.diagnosis,
            treatment = emr.treatment,
            results = emr.results
        )
        tp.append(medical_info)

    cluster_assignment, clustered_sentences = create_clusters(create_semantic_entries(t))

    for emr in t:
        emr.cluster_id = int(cluster_assignment[emr.id - 1])

    qids = [[t[i].id, t[i].sex, t[i].postal_code, t[i].birth_date, t[i].hospitalization_date, t[i].cluster_id] 
            for i in range(len(t))]
    columns = ['id', 'sex', 'postal_code', 'birth_date', 'hospitalization_date', 'cluster_id']

    frame = pandas.DataFrame(data=qids, columns=columns)
    frame = frame.astype({
        'id': 'int',
        'sex': 'category',
        'postal_code': 'int',
        'birth_date': 'datetime64[ns]',
        'hospitalization_date': 'datetime64[ns]',
        'cluster_id': 'int'
    })

    preserver = Preserver(
        frame,
        ['postal_code', 'birth_date', 'hospitalization_date'],
        'cluster_id',
        ['sex', 'id']
    )
    anon_qids = preserver.anonymize_t_closeness(k=10, p=0.2)

    for qid in anon_qids:
        for i in range(0, len(qid['id'])):
            anon_qid = AnonQID(
                id = qid['id'][i],
                sex = qid['sex'][i],
                postal_code = qid['postal_code'][0],
                birth_date = qid['birth_date'][0],
                hospitalization_date = qid['hospitalization_date'][0]
            )
            ta.append(anon_qid)

    MedicalInfo.objects.bulk_create(tp)
    EncryptedID.objects.bulk_create(te)
    AnonQID.objects.bulk_create(ta)

    return (tp, te, ta)