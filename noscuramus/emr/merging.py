from .models import *
from .cipher import *
from datetime import datetime

def data_merging_anon(tp, ta):
    t = []

    for i in range(len(tp)):
        merged_data = AnonMergedData(
            id = ta[i].id,
            sex = ta[i].sex,
            postal_code = ta[i].postal_code,
            birth_date = ta[i].birth_date,
            hospitalization_date = ta[i].hospitalization_date,
            diagnosis = tp[i].diagnosis,
            treatment = tp[i].treatment,
            results = tp[i].results
        )
        t.append(merged_data)
        
    t.sort(key=lambda x: x.id)
    return t

def data_merging(tp, te):
    t = []
    
    for i in range(len(tp)):
        merged_data = MergedData(
            id = te[i].id,
            name = decipher_text(te[i].name),
            national_id = decipher_text(te[i].national_id),
            social_security_number = decipher_text(te[i].social_security_number),
            sex = decipher_text(te[i].sex),
            postal_code = decipher_text(te[i].postal_code),
            birth_date = datetime.strptime(decipher_text(te[i].birth_date), '%Y-%m-%d'),
            hospitalization_date = datetime.strptime(decipher_text(te[i].hospitalization_date), '%Y-%m-%d'),
            diagnosis = tp[i].diagnosis,
            treatment = tp[i].treatment,
            results = tp[i].results
        )
        t.append(merged_data)

    t.sort(key=lambda x: x.id)
    return t