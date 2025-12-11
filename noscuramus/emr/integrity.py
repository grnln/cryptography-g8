import hashlib
from .models import Checksum, BlockTag
import random
import math
import hmac

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

def tag_gen(N, g, m_list):
    BlockTag.objects.all().delete()
    # m_list of the form [(index, m)]
    D_list = []
    for m in m_list:
        D_list.append(BlockTag(id=m[0], tag=int(pow(g, m[1], N))))

    tagList = BlockTag.objects.bulk_create(D_list)
    return tagList

def get_prf_value(random_seed, x, total_blocks):
    k_bytes = random_seed.to_bytes((random_seed.bit_length() + 7) // 8 or 1, "big")
    x_bytes = x.to_bytes((x.bit_length() + 7) // 8 or 1, "big")

    digest = hmac.new(k_bytes, x_bytes, hashlib.sha256).digest()

    return int.from_bytes(digest, "big") % total_blocks

def genIndices(total_blocks, num_to_check, random_seed):
    indices = set()
    i = 0
    
    while len(indices) < num_to_check:
        idx = get_prf_value(random_seed, i, total_blocks)
        indices.add(idx)
        i += 1

    print(list(indices))
    return list(indices)

def challenge(g, N, s):
    gS = pow(g, s, N)
    return gS

def genProof(nBlocks, randomSeed, m_list, N, gS, total_blocks):
    indices = genIndices(total_blocks, nBlocks, randomSeed)
    R = pow(gS, sum([m_list[i][1] for i in indices]), N)
    return R

def checkProof(nBlocks, randomSeed, N, s, total_blocks):
    indices = genIndices(total_blocks, nBlocks, randomSeed)
    tags = BlockTag.objects.order_by('id')
    P = math.prod([(tags[i].tag % N) for i in indices]) % N
    R = pow(P, s, N)
    return R

def remoteIntegrityCheck(nBlocks, randomSeed):
    # SETUP

    p = 1019  # 1019 ≡ 3 (mod 4), SECRET TO CLIENT
    q = 2027  # 2027 ≡ 3 (mod 4), SECRET TO CLIENT
    N = p * q # PUBLIC
    g = 2 # PUBLIC

    m_list = [(i, random.randint(1, 1000)) for i in range(1200)] # TO BE OBTAINED FROM EMR DATABASE

    # TAG GEN

    tag_gen(N, g, m_list)

    s = random.randint(1, N - 1) # SECRET TO SERVER
    gS = challenge(g, N, s) # GEN BY CLIENT. PUBLIC

    R_server = genProof(nBlocks, randomSeed, m_list, N ,gS, len(m_list)) # FROM GS AND M_LIST (current)
    R_client = checkProof(nBlocks, randomSeed, N, s, len(m_list)) # FROM S AND TAGS (original m_list)

    return R_server == R_client