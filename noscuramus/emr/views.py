from django.shortcuts import render, redirect
from .emr_parser import parse_csv_to_emr_list
from .partitioning import vertical_data_partitioning
from .search import hybrid_search
from .merging import *
from .models import *
from .integrity import hash_emr, remoteIntegrityCheck
from django.http import JsonResponse, HttpResponse

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
    return redirect('load_csv')

def loaded_dataset(request):
    emrs = EMR.objects.order_by('id')
    context = {'emrs': emrs}
    return render(request, 'load_csv.html', context)

def vertical_partition(request):
    emrs = EMR.objects.order_by('id')

    (tp, te, ta) = vertical_data_partitioning(emrs)
    tp.sort(key=lambda x: x.id)
    te.sort(key=lambda x: x.id)
    ta.sort(key=lambda x: x.id)

    return redirect('database')

def erase_dataset(request):
    EncryptedID.objects.all().delete()
    AnonQID.objects.all().delete()
    MedicalInfo.objects.all().delete()

    return redirect('database')

def search(request):
    context = dict()
    return render(request, 'search.html', context)

def search_results(request):
    keywords = request.POST.get('search', None)

    if keywords != None and keywords != 'null':
        keywords = keywords.split(' ')

    ids_scores = hybrid_search(keywords)
    results = list(EMR.objects.filter(id__in = ids_scores.keys()))
    results.sort(key = lambda emr: ids_scores[emr.id])

    context = {
        'results': results
    }
    return render(request, 'search_results.html', context)

def merge(request):
    return render(request, 'choose_merge.html')

def merge_anon(request):
    tp = MedicalInfo.objects.order_by("id")
    ta = AnonQID.objects.order_by("id")

    tm1 = data_merging_anon(list(tp), list(ta))

    context = {
        'merged_data': tm1
    }
    return render(request, 'anon_merge.html', context)

def merge_full(request):
    tp = MedicalInfo.objects.order_by("id")
    te = EncryptedID.objects.order_by("id")

    tm2 = data_merging(list(tp), list(te))

    context = {
        'merged_data': tm2
    }
    return render(request, 'full_merge.html', context)

def check_integrity(request, id):
    try:
        emr = EMR.objects.get(id=id)
        computed_hash = hash_emr(emr).hex()
        stored_checksum = Checksum.objects.get(id=id).checksum
        
        return JsonResponse({
            'id': id,
            'valid': computed_hash == stored_checksum,
            'computed': computed_hash,
            'stored': stored_checksum
        })
    except EMR.DoesNotExist:
        return JsonResponse({'error': 'EMR no encontrado'}, status=404)
    except Checksum.DoesNotExist:
        return JsonResponse({'error': 'Checksum no encontrado'}, status=404)

def remote_integrity_check(request):
    nBlocks = EMR.objects.count() // 4
    randomSeed = 12345
    res = remoteIntegrityCheck(nBlocks, randomSeed)
    return HttpResponse("Remote Integrity Check Placeholder. Res = " + str(res))