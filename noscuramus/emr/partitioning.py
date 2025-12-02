from models import *

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

aes = AES.new(get_random_bytes(32), AES.MODE_ECB)

def cypher_text(t):
    return aes.encrypt(bytearray(t))

def vertical_partition(t):
    tp, te, ta = []

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
            hospitalization_date = cypher_text(str(emr.hospitalization_datae))
        )
        te.append(encrypted_id)
    
        # Add all medical information to Tp, verbatim
        medical_info = MedicalInfo(
            diagnosis = emr.diagnosis,
            treatment = emr.treatment,
            results = emr.results
        )
        tp.append(medical_info)

    

    return (tp, te, ta)