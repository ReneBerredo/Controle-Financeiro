from django.contrib import admin
from django.urls import path, include
from financas import views as financas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', financas_views.home, name='home'),
    path('financas/', include('financas.urls')),
]
