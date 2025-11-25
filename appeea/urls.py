from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import prueba
from . import views_auth

urlpatterns = [
                  path('', views.index, name='index'),
                  path('noticias/', views.noticias, name='noticias'),
                  path('programasservicios/', views.programasservicios, name='programasservicios'),
                  path('noticias/<slug:ide>/<slug:url>/', views.noticias_cat, name='noticias_cat'),
                  path('noticias/detalle/<slug:ide>/<slug:url>/', views.noticia_individual,
                       name='noticia_individual'),
                  path('la-institucion/', views.institucion, name='institucion'),
                  path('la-institucion/<int:ide>/<slug:url>/', views.institucion_individual,
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
                  path('servicioseea/', views.servicioseea, name='servicioseea'),
                  path('sgda-eea/', views.sgda_eea, name='sgda_eea'),
                  path('servicios/<slug:ide>/<slug:url>/', views.servicios_individual,
                       name='servicios_individual'),
                  # Procesos de contratacion
                  path('procesoscontratacion/<slug:ide>/', views.procesoscontratacion1,
                       name='procesoscontratacion'),
                  path('procesoscontratacion/<slug:ide>/<slug:ide2>/', views.procesoscontratacion2,
                       name='procesoscontratacion'),
                  path('procesoscontratacion/<slug:ide>/<slug:ide2>/<slug:ide3>/',
                       views.procesoscontratacion3, name='procesoscontratacion'),
                  path('prueba', prueba, name="prueba"),

                  path('obtener_factura/<str:num_doc>/', views.obtener_factura, name='obtener_factura'),
                  
                  # Ruta antigua redirigida a página de acceso restringido
                  path('consulta-planillas/', views.info_cuenta, name='info_cuenta_deprecated'),
                  
                  path('documentos/', views.documentos, name='documentos'),
                  
                  # Sistema de Autenticación y Registro
                  path('auth/verificar/', views_auth.verificar_usuario, name='verificar_usuario'),
                  path('auth/checking/', views_auth.proceso_checking, name='proceso_checking'),
                  path('auth/registro/', views_auth.registro_usuario, name='registro_usuario'),
                  path('auth/confirmacion-correo/', views_auth.confirmacion_correo, name='confirmacion_correo'),
                  path('auth/validacion-identidad/', views_auth.validacion_identidad, name='validacion_identidad'),
                  path('auth/login/', views_auth.login_usuario, name='login_usuario'),
                  path('auth/recuperacion/', views_auth.recuperacion_credenciales, name='recuperacion_credenciales'),
                  path('auth/verificar-recuperacion/', views_auth.verificar_codigo_recuperacion, name='verificar_codigo_recuperacion'),
                  path('auth/logout/', views_auth.logout_usuario, name='logout_usuario'),
                  path('auth/consultas/', views_auth.consulta_planillas, name='consulta_planillas'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
