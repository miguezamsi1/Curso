from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('', views.index, name='index'),
                  path(r'^noticias/$', views.noticias, name='noticias'),
                  path(r'^programasservicios/$', views.programasservicios, name='programasservicios'),
                  path(r'^noticias/(?P<ide>\d+)/(?P<url>[\w\-]+)/$', views.noticias_cat, name='noticias_cat'),
                  path(r'^noticias/detalle/(?P<ide>\d+)/(?P<url>[\w\-]+)/$', views.noticia_individual,
                       name='noticia_individual'),
                  path(r'^la-institucion/$', views.institucion, name='institucion'),
                  path(r'^la-institucion/(?P<ide>\d+)/(?P<url>[\w\-]+)/$', views.institucion_individual,
                       name='institucion_individual'),
                  # Menu Adicional
                  path(r'^eea/(?P<ide>\d+)/$', views.menu, name='eea'),
                  # Transparencia
                  path(r'^transparencia/$', views.transparencia, name='transparencia'),
                  path(r'^transparencia_anio/(?P<ide>\d+)/$', views.transparenciaanio, name='transparenciaanio'),
                  # Rendicion
                  path(r'^rendicion_de_cuentas/$', views.rendicion, name='rendicion'),
                  path(r'^rendicion_de_cuentas_por_anio/(?P<ide>\d+)/$', views.rendicionanio, name='rendicionanio'),
                  # Servicios
                  path(r'^servicios/$', views.servicios, name='servicios'),
                  path(r'^servicios/(?P<ide>\d+)/(?P<url>[\w\-]+)/$', views.servicios_individual,
                       name='servicios_individual'),
                  # Procesos de contratacion
                  path(r'^procesoscontratacion/(?P<ide>\d+)/$', views.procesoscontratacion1,
                       name='procesoscontratacion'),
                  path(r'^procesoscontratacion/(?P<ide>\d+)/(?P<ide2>\d+)/$', views.procesoscontratacion2,
                       name='procesoscontratacion'),
                  path(r'^procesoscontratacion/(?P<ide>[\w\-]+)/(?P<ide2>[\w\-]+)/(?P<ide3>\d+)/$',
                       views.procesoscontratacion3, name='procesoscontratacion'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
