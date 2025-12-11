"""
URL configuration for noscuramus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from emr import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('database', views.database, name='database'),
    path('database/load', views.load_dataset, name='load_db'),
    path('database/erase', views.erase_dataset, name='erase_db'),
    path('load-csv', views.loaded_dataset, name='load_csv'),
    path('partition', views.vertical_partition, name='vertical_partition'),
    path('search/', views.search, name='search'),
    path('search-results/', views.search_results, name='search_results')
]
