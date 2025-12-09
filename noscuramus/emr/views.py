from django.http import HttpResponse

from .emr_parser import parse_csv_to_emr_list
from .partitioning import vertical_partition
from .merging import data_merging
from .models import *

def load_dataset(request):
    emrs = parse_csv_to_emr_list('../dataset/sample_dataset.csv')
    tp, te, ta = vertical_partition(emrs)
    
    output = "<h1>Tp</h1>" + "<br>".join([str(p) for p in tp])
    output += "<h1>Te</h1>" + "<br>".join([str(p) for p in te])
    output += "<h1>Ta</h1>" + "<br>".join([str(p) for p in ta])
    
    return HttpResponse(output)

def merge(request):
    tp = MedicalInfo.objects.all()
    ta = AnonQID.objects.all()
    tm = data_merging(list(tp), list(ta))

    output = "<h1>Tm</h1>" + "<br>".join([str(p) for p in tm])
    return HttpResponse(output)
