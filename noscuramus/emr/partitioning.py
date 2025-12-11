from .models import *
from .clustering import *
from .emr_parser import *
from .cipher import *
from .anonypy_custom import Preserver
from noscuramus.settings import ENCRYPTED_INDEX_DIR, PLAIN_INDEX_DIR

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.qparser.dateparse import DateParserPlugin
from whoosh import qparser, query

import pandas, shutil

def add_eid_to_index(eid):
    with open(os.path.join(ENCRYPTED_INDEX_DIR, f'{eid[0]:04}.eid'), mode = 'w') as f:
        for word in eid[1].split(' '):
            f.write(f'{str(hash_word(word.lower()))}\n')

        f.write(f'{str(hash_word(eid[2].lower()))}\n')
        f.write(f'{str(hash_word(eid[3].lower()))}\n')
        f.write(f'{str(hash_word(eid[4].lower()))}\n')
        f.write(f'{str(hash_word(eid[5].lower()))}\n')

        for word in str(eid[6]).split('-'):
            f.write(f'{str(hash_word(word.lower()))}\n')

        for word in str(eid[7]).split('-'):
            f.write(f'{str(hash_word(word.lower()))}\n')

def create_indices(te, tp):
    if not os.path.exists(ENCRYPTED_INDEX_DIR):
        os.mkdir(ENCRYPTED_INDEX_DIR)

    for eid in te:
        add_eid_to_index(eid)

    if not os.path.exists(PLAIN_INDEX_DIR):
        os.mkdir(PLAIN_INDEX_DIR)

    schema = Schema(
        id = ID(stored = True),
        diagnosis = TEXT(stored = True, phrase = False),
        treatment = TEXT(stored = True, phrase = False),
        results = TEXT(stored = True, phrase = False)
    )
    index = create_in(PLAIN_INDEX_DIR, schema)
    writer = index.writer()

    for mi in tp:
        writer.add_document(
            id = str(mi.id),
            diagnosis = mi.diagnosis,
            treatment = mi.treatment,
            results = mi.results
        )
    writer.commit()

def vertical_data_partitioning(t):
    tp = []
    te = []
    ta = []

    te_index = []

    MedicalInfo.objects.all().delete()
    EncryptedID.objects.all().delete()
    AnonQID.objects.all().delete()

    if os.path.exists(ENCRYPTED_INDEX_DIR):
        shutil.rmtree(ENCRYPTED_INDEX_DIR, ignore_errors = True)

    if os.path.exists(PLAIN_INDEX_DIR):
        shutil.rmtree(PLAIN_INDEX_DIR, ignore_errors = True)

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
    
        te_index.append((
            int(emr.id),
            emr.name,
            emr.national_id,
            emr.social_security_number,
            emr.sex,
            emr.postal_code,
            str(emr.birth_date),
            str(emr.hospitalization_date)
        ))

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

    create_indices(te_index, tp)
    return (tp, te, ta)