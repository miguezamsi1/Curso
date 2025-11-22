# vim: set fileencoding=utf-8 :
from django.contrib import admin
from image_cropping import ImageCroppingMixin
from import_export.admin import ImportExportModelAdmin
from . import models

admin.site.site_title = "Empresa Eléctrica Azogues C.A."
admin.site.site_header = 'Administración Página Web EEA'


class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'id_tags',
        'habilitado',
        'nombre_menu',
        'contenido',
        'texto_lateral',
        'izq_titulo',
        'izq_contenido',
    )
    list_filter = ('habilitado', 'texto_lateral')


class CabeceraAdmin(ImportExportModelAdmin):
    list_display = ('id_cabecera', 'titulo', 'imagen')
    search_fields = ('titulo',)


class IndexGeneralAdmin(admin.ModelAdmin):
    list_display = (
        'id_indexgeneral',
        'titulo',
        'logo',
        'facebook',
        'twitter',
        'instagram',
        'youtube',
    )


class IndexEnlacesInteresAdmin(admin.ModelAdmin):
    list_display = ('id_enlacesinteres', 'titulo', 'url', 'estado')


class IndexServiciosAdmin(admin.ModelAdmin):
    list_display = ('id_serviciosindex', 'icono', 'titulo', 'url', 'estado')


class TagsNoticiaAdmin(admin.ModelAdmin):
    list_display = ('id_tags', 'nombre')


class NoticiaAdmin(ImageCroppingMixin, ImportExportModelAdmin):
    list_display = (
        'id_noticia',
        'titulo',
        'descripcion',
        'keywords',
        'imagen',
        'fechap',
        'estado',
    )
    list_filter = ('fechap', 'estado')
    filter_horizontal = ('tags',)


class EnterateAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('id_enterate', 'titulo', 'link', 'imagen', 'imagen_red1')


class EmpresaInformaAdmin(admin.ModelAdmin):
    list_display = ('id_informa', 'titulo', 'link')


class InformaAdmin(admin.ModelAdmin):
    list_display = ('id_informa', 'titulo', 'link')


class InstitucionAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = (
        'id_institucion',
        'titulo',
        'descripcion',
        'keywords',
        # 'imagen',
        'fechap',
        'estado',
    )
    list_filter = ('fechap', 'estado')


class transparencia_anoAdmin(admin.ModelAdmin):
    list_display = ('id_transparenciaano', 'nombre_ano', 'contenido')


class transparencia_mesAdmin(admin.ModelAdmin):
    list_display = ('id_transparenciames', 'nombre_mes')


class transparencia_documentosAdmin(admin.ModelAdmin):
    list_display = (
        'id_tags',
        'nombre_documento',
        'subir_documento',
        'id_transparenciaano',
        'id_transparenciames',
    )
    list_filter = ('id_transparenciaano', 'id_transparenciames')


class RendicionAnoAdmin(admin.ModelAdmin):
    list_display = ('id_rendicionano', 'nombre_ano', 'contenido')


class RendicionFaseAdmin(admin.ModelAdmin):
    list_display = ('id_rendicionfase', 'nombre_fase')


class RendicionDocumentosAdmin(admin.ModelAdmin):
    list_display = (
        'id_tags',
        'nombre_documento',
        'subir_documento',
        'id_rendicionano',
        'id_rendicionfase',
    )
    list_filter = ('id_rendicionano', 'id_rendicionfase')


class ServiciosAdmin(admin.ModelAdmin):
    list_display = (
        'id_institucion',
        'titulo',
        'estado',
        'descripcion',
        'keywords',
        # 'imagen',
        # 'imagen_red1',
        # 'imagen_red2',
        'fechap',
    )
    list_filter = ('estado', 'fechap')


class ProcesosContratacionNivel1Admin(admin.ModelAdmin):
    list_display = ('id_procesos', 'titulo', 'contenido')


class ProcesosContratacionNivel2Admin(admin.ModelAdmin):
    list_display = ('id_procesos2', 'id_procesos', 'titulo', 'contenido')
    list_filter = ('id_procesos',)


class ProcesosContratacionNivel3Admin(admin.ModelAdmin):
    list_display = ('id_procesos3', 'id_procesos2', 'titulo')
    list_filter = ('id_procesos2',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Menu, MenuAdmin)
_register(models.TagsNoticia, TagsNoticiaAdmin)
_register(models.Noticia, NoticiaAdmin)
_register(models.Enterate, EnterateAdmin)
_register(models.Informa, InformaAdmin)
_register(models.EmpresaInforma, EmpresaInformaAdmin)
_register(models.Institucion, InstitucionAdmin)
_register(models.Cabecera, CabeceraAdmin)
_register(models.IndexGeneral, IndexGeneralAdmin)
_register(models.IndexEnlacesInteres, IndexEnlacesInteresAdmin)
_register(models.IndexServicios, IndexServiciosAdmin)
_register(models.transparencia_ano, transparencia_anoAdmin)
_register(models.transparencia_mes, transparencia_mesAdmin)
_register(models.transparencia_documentos, transparencia_documentosAdmin)
_register(models.RendicionAno, RendicionAnoAdmin)
_register(models.RendicionFase, RendicionFaseAdmin)
_register(models.RendicionDocumentos, RendicionDocumentosAdmin)
_register(models.Servicios, ServiciosAdmin)
_register(models.ProcesosContratacionNivel1, ProcesosContratacionNivel1Admin)
_register(models.ProcesosContratacionNivel2, ProcesosContratacionNivel2Admin)
_register(models.ProcesosContratacionNivel3, ProcesosContratacionNivel3Admin)
