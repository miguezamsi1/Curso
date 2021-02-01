from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import prueba

urlpatterns = [
                  path('', views.index, name='index'),
                  path('noticias/', views.noticias, name='noticias'),
                  path('programasservicios/', views.programasservicios, name='programasservicios'),
                  path('noticias/<slug:ide>/<slug:url>/', views.noticias_cat, name='noticias_cat'),
                  path('noticias/detalle/<slug:ide>/<slug:url>/', views.noticia_individual,
                       name='noticia_individual'),
                  path('la-institucion/', views.institucion, name='institucion'),
                  path('la-institucion/(?P<ide>\d+)/(?P<url>[\w\-]+)/', views.institucion_individual,
                       name='institucion_individual'),
                  # Menu Adicional
                  path('eea/<slug:ide>/', views.menu, name='eea'),
                  # Transparencia
                  path('transparencia/', views.transparencia, name='transparencia'),
                  path('transparencia_anio/<slug:ide>/', views.transparenciaanio, name='transparenciaanio'),
                  # Rendicion
                  path('rendicion_de_cuentas/', views.rendicion, name='rendicion'),
                  path('rendicion_de_cuentas_por_anio/<slug:ide>/', views.rendicionanio, name='rendicionanio'),
                  # Servicios
                  path('servicios/', views.servicios, name='servicios'),
                  path('servicios/<slug:ide>/<slug:url>/', views.servicios_individual,
                       name='servicios_individual'),
                  # Procesos de contratacion
                  path('procesoscontratacion/<slug:ide>/', views.procesoscontratacion1,
                       name='procesoscontratacion'),
                  path('procesoscontratacion/<slug:ide>/<slug:ide2>/', views.procesoscontratacion2,
                       name='procesoscontratacion'),
                  path('procesoscontratacion/<slug:ide>/<slug:ide2>/<slug:ide3>/',
                       views.procesoscontratacion3, name='procesoscontratacion'),
                  path('prueba', prueba, name="prueba")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
