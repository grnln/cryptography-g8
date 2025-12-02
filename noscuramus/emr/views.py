from django.http import HttpResponse
from .emr_parser import parse_csv_to_emr_list

def load_dataset(request):
    lista_emr = parse_csv_to_emr_list('../dataset/sample_dataset.csv')

    output = "<br>".join([str(p) for p in lista_emr])

    return HttpResponse(output)
