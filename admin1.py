# vim: set fileencoding=utf-8 :
from django.contrib import admin

from . import models


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


class TagsNoticiaAdmin(admin.ModelAdmin):

    list_display = ('id_tags', 'nombre')


class NoticiaAdmin(admin.ModelAdmin):

    list_display = (
        'id_noticia',
        'titulo',
        'descripcion',
        'keywords',
        'imagen',
        'imagen_red1',
        'imagen_red2',
        'contenido',
        'fechap',
        'estado',
    )
    list_filter = ('fechap', 'estado')
    raw_id_fields = ('tags',)


class ProgramasServiciosAdmin(admin.ModelAdmin):

    list_display = (
        'id_programasservicios',
        'titulo',
        'descripcion',
        'keywords',
        'contenido',
        'fechap',
        'estado',
    )
    list_filter = ('fechap', 'estado')


class EnterateAdmin(admin.ModelAdmin):

    list_display = (
        'id_enterate',
        'titulo',
        'link',
        'imagen',
        'imagen_red1',
        'publicado',
    )
    list_filter = ('publicado',)


class InformaAdmin(admin.ModelAdmin):

    list_display = ('id_informa', 'titulo', 'link', 'publicado')
    list_filter = ('publicado',)


class InstitucionAdmin(admin.ModelAdmin):

    list_display = (
        'id_institucion',
        'titulo',
        'estado',
        'descripcion',
        'keywords',
        'contenido',
        'fechap',
    )
    list_filter = ('estado', 'fechap')


class ServiciosAdmin(admin.ModelAdmin):

    list_display = (
        'id_institucion',
        'titulo',
        'estado',
        'descripcion',
        'keywords',
        'contenido',
        'fechap',
    )
    list_filter = ('estado', 'fechap')


class CabeceraAdmin(admin.ModelAdmin):

    list_display = ('id_cabecera', 'titulo', 'imagen', 'referencia')


class IndexGeneralAdmin(admin.ModelAdmin):

    list_display = (
        'id_indexgeneral',
        'titulo',
        'logo',
        'facebook',
        'twitter',
        'instagram',
        'youtube',
        'flikr',
        'nombre_marcador',
        'zoom',
        'mapa',
        'piepagina',
    )


class IndexEnlacesInteresAdmin(admin.ModelAdmin):

    list_display = ('id_enlacesinteres', 'estado', 'titulo', 'url', 'imagen')
    list_filter = ('estado',)


class IndexServiciosAdmin(admin.ModelAdmin):

    list_display = ('id_serviciosindex', 'icono', 'titulo', 'url', 'estado')
    list_filter = ('estado',)


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


class ProcesosContratacionNivel1Admin(admin.ModelAdmin):

    list_display = ('id_procesos', 'tipo', 'titulo', 'contenido')


class ProcesosContratacionNivel2Admin(admin.ModelAdmin):

    list_display = (
        'id_procesos2',
        'tipo',
        'id_procesos',
        'titulo',
        'contenido',
    )
    list_filter = ('id_procesos',)


class ProcesosContratacionNivel3Admin(admin.ModelAdmin):

    list_display = (
        'id_procesos3',
        'tipo',
        'id_procesos2',
        'titulo',
        'contenido',
    )
    list_filter = ('id_procesos2',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Menu, MenuAdmin)
_register(models.TagsNoticia, TagsNoticiaAdmin)
_register(models.Noticia, NoticiaAdmin)
_register(models.ProgramasServicios, ProgramasServiciosAdmin)
_register(models.Enterate, EnterateAdmin)
_register(models.Informa, InformaAdmin)
_register(models.Institucion, InstitucionAdmin)
_register(models.Servicios, ServiciosAdmin)
_register(models.Cabecera, CabeceraAdmin)
_register(models.IndexGeneral, IndexGeneralAdmin)
_register(models.IndexEnlacesInteres, IndexEnlacesInteresAdmin)
_register(models.IndexServicios, IndexServiciosAdmin)
_register(models.transparencia_ano, transparencia_anoAdmin)
_register(models.transparencia_mes, transparencia_mesAdmin)
_register(models.transparencia_documentos, transparencia_documentosAdmin)
_register(models.ProcesosContratacionNivel1, ProcesosContratacionNivel1Admin)
_register(models.ProcesosContratacionNivel2, ProcesosContratacionNivel2Admin)
_register(models.ProcesosContratacionNivel3, ProcesosContratacionNivel3Admin)
