import hashlib
from .models import Checksum

def hash_emr(emr):
    x = compute_checksum_input(emr)
    return hashlib.sha256(x).digest()

def compute_checksum_input(emr):
    x = emr.id.to_bytes(8, byteorder='big')

    attributes = [
        emr.name,
        emr.national_id,
        emr.social_security_number,
        emr.sex,
        emr.postal_code,
        emr.birth_date.isoformat(),
        emr.hospitalization_date.isoformat(),
        emr.diagnosis,
        emr.treatment,
        emr.results
    ]

    for attr in attributes:
        attr_bytes = attr.encode('utf-8')
        
        if len(attr_bytes) > len(x):
            x = x + b'\x00' * (len(attr_bytes) - len(x))
        elif len(x) > len(attr_bytes):
            attr_bytes = attr_bytes + b'\x00' * (len(x) - len(attr_bytes))
        
        x = bytes(a ^ b for a, b in zip(x, attr_bytes))
    
    return x

def check_integrity(id, emr):
    computed_checksum = hash_emr(emr)
    stored_checksum = Checksum.objects.get(id=id).checksum
    return computed_checksum == stored_checksum