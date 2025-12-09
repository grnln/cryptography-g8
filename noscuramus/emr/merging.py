from .models import *

def data_merging(tp, ta):
    t = []

    for i in range(len(tp)):
        merged_data = MergedData(
            sex = ta[i].sex,
            postal_code = ta[i].postal_code,
            birth_date = ta[i].birth_date,
            hospitalization_date = ta[i].hospitalization_date,
            diagnosis = tp[i].diagnosis,
            treatment = tp[i].treatment,
            results = tp[i].results
        )
        t.append(merged_data)
    return t