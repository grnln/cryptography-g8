from django.http import HttpResponse

from .emr_parser import parse_csv_to_emr_list
from .partitioning import vertical_partition
from .merging import *
from .models import *

def load_dataset(request):
    emrs = parse_csv_to_emr_list('../dataset/sample_dataset.csv')
    (tp, te, ta) = vertical_partition(emrs)
    tp.sort(key=lambda x: x.id)
    te.sort(key=lambda x: x.id)
    ta.sort(key=lambda x: x.id)

    output = "<h1>Tp</h1>" + "<br>".join([str(p) for p in tp[:10]])
    output += "<h1>Te</h1>" + "<br>".join([str(p) for p in te[:10]])
    output += "<h1>Ta</h1>" + "<br>".join([str(p) for p in ta[:10]])
    
    return HttpResponse(output)

def merge(request):
    tp = MedicalInfo.objects.all()
    ta = AnonQID.objects.all()
    te = EncryptedID.objects.all()

    tm1 = data_merging_anon(list(tp), list(ta))
    tm2 = data_merging(list(tp), list(te))

    output = "<h1>Tm1</h1>" + "<br>".join([str(p) for p in tm1])
    output = "<h1>Tm2</h1>" + "<br>".join([str(p) for p in tm2])
    return HttpResponse(output)
