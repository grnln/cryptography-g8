from django.http import HttpResponse
from django.shortcuts import render, redirect
from .emr_parser import parse_csv_to_emr_list
from .partitioning import vertical_partition
from .merging import *
from .models import *

def home(request):
    return render(request, 'home.html')

def database(request):
    context = {
        "tp": EncryptedID.objects.order_by("id"),
        "te": AnonQID.objects.order_by("id"),
        "ta": MedicalInfo.objects.order_by("id"),
    }
    return render(request, "database.html", context)

def load_dataset(request):
    emrs = parse_csv_to_emr_list('../dataset/sample_dataset.csv')
    (tp, te, ta) = vertical_partition(emrs)
    tp.sort(key=lambda x: x.id)
    te.sort(key=lambda x: x.id)
    ta.sort(key=lambda x: x.id)

    return redirect('database')

def erase_dataset(request):
    EncryptedID.objects.all().delete()
    AnonQID.objects.all().delete()
    MedicalInfo.objects.all().delete()

    return redirect('database')

def merge(request):
    tp = MedicalInfo.objects.all()
    ta = AnonQID.objects.all()
    te = EncryptedID.objects.all()

    tm1 = data_merging_anon(list(tp), list(ta))
    tm2 = data_merging(list(tp), list(te))

    output = "<h1>Tm1</h1>" + "<br>".join([str(p) for p in tm1])
    output = "<h1>Tm2</h1>" + "<br>".join([str(p) for p in tm2])
    return HttpResponse(output)
