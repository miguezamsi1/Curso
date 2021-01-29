# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import unicode_literals

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import *
from django.db.models import *
from django.utils.encoding import python_2_unicode_compatible
from geoposition.fields import GeopositionField
from image_cropping import ImageRatioField


@python_2_unicode_compatible
class Menu(models.Model):
    id_tags = models.AutoField(primary_key=True)
    habilitado = models.BooleanField(verbose_name="Habilitar el Menú")
    nombre_menu = models.CharField(max_length=200, verbose_name="Nombre del Menú")
    contenido = RichTextUploadingField(max_length=6000)
    texto_lateral = BooleanField(verbose_name="Habilitar el Teto Lateral Izquierdo")
    izq_titulo = CharField(max_length=6000)
    izq_contenido = TextField(max_length=6000)

    class Meta:
        db_table = 'menu_adicional'
        verbose_name = 'Nuevo menú'
        verbose_name_plural = 'Nuevos menús'

    def __str__(self):
        return u'%s' % self.nombre_menu


@python_2_unicode_compatible
class TagsNoticia(models.Model):
    id_tags = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)

    class Meta:
        db_table = 'tags_noticia'
        verbose_name = 'Tags de las noticia'
        verbose_name_plural = 'Tags de las noticias'

    def __str__(self):
        return u'%s' % self.nombre


@python_2_unicode_compatible
class Noticia(models.Model):
    id_noticia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500)
    keywords = models.CharField(max_length=500)
    imagen = models.ImageField(upload_to='noticia')
    imagen_red1 = ImageRatioField('imagen', '640x383')
    imagen_red2 = ImageRatioField('imagen', '250x143')
    contenido = RichTextUploadingField(max_length=9999999)
    fechap = models.DateField(auto_now_add=True)
    estado = models.BooleanField(verbose_name="Publicar este item")
    tags = models.ManyToManyField(TagsNoticia)

    class Meta:
        db_table = 'noticia'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class ProgramasServicios(models.Model):
    id_programasservicios = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=500)
    keywords = models.CharField(max_length=500)
    contenido = RichTextUploadingField(max_length=9999999)
    fechap = models.DateField(auto_now_add=True)
    estado = models.BooleanField(verbose_name="Publicar este item")

    class Meta:
        db_table = 'programasservicios'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class Enterate(models.Model):
    id_enterate = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    imagen = models.ImageField(upload_to='enterate')
    imagen_red1 = ImageRatioField('imagen', '443x281')
    publicado = models.BooleanField(verbose_name="Publicar este item")

    class Meta:
        db_table = 'enterate'
        verbose_name = 'Enterate'
        verbose_name_plural = 'Imágenes de Entérate'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class Informa(models.Model):
    id_informa = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    publicado = models.BooleanField(verbose_name="Publicar este item")

    class Meta:
        db_table = 'informa'
        verbose_name = 'Informate'
        verbose_name_plural = 'Videos de Informate'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class EmpresaInforma(models.Model):
    id_informa = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    link = models.CharField(max_length=300)
    publicado = models.BooleanField(verbose_name="Publicar este item")

    class Meta:
        db_table = 'empresainforma'
        verbose_name = 'Video de la empresa informa'
        verbose_name_plural = 'Videos de la empresa informa'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class Institucion(models.Model):
    id_institucion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    estado = models.BooleanField()
    descripcion = models.TextField(max_length=500)
    keywords = models.CharField(max_length=500)
    # imagen = models.ImageField(upload_to='institucion')
    # imagen_red1 = ImageRatioField('imagen', '640x383')
    # imagen_red2 = ImageRatioField('imagen', '250x143')
    contenido = RichTextUploadingField(max_length=10000)
    fechap = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'institucion'
        verbose_name = 'Institución'
        verbose_name_plural = 'Items Institución'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class Servicios(models.Model):
    id_institucion = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    estado = models.BooleanField()
    descripcion = models.TextField(max_length=500)
    keywords = models.CharField(max_length=500)
    # imagen = models.ImageField(upload_to='institucion')
    # imagen_red1 = ImageRatioField('imagen', '640x383')
    # imagen_red2 = ImageRatioField('imagen', '250x143')
    contenido = RichTextUploadingField(max_length=10000)
    fechap = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios de la Institución'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class Cabecera(models.Model):
    id_cabecera = models.AutoField(primary_key=True)
    paginas_select = (
        ('1', 'index'), ('2', 'institucion'), ('3', 'noticias'), ('4', 'transparencia'), ('5', 'noticia detalle'),
        ('6', 'detalle institución'))
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='cabecera')
    referencia = models.CharField(max_length=150, choices=paginas_select)

    class Meta:
        db_table = 'cabecera'
        verbose_name = 'Cabecera'
        verbose_name_plural = 'Imagenes cabecera'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class IndexGeneral(models.Model):
    id_indexgeneral = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='logo')
    facebook = models.CharField(max_length=200)
    twitter = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200)
    youtube = models.CharField(max_length=200)
    flikr = models.CharField(max_length=200)
    popup = models.ImageField(verbose_name="Suba la imagen del popup")
    popup_tiempo = models.IntegerField(verbose_name="Cerrar el popup despues de n segundos")
    popup_habilitar = models.BooleanField(verbose_name="Haga clic aquí para habilitar el popup")
    nombre_marcador = models.CharField(max_length=200, verbose_name="Nombre del marcador en el mapa")
    zoom = models.IntegerField(verbose_name="Zoom mapa")
    mapa = GeopositionField()
    piepagina = RichTextUploadingField(max_length=10000, verbose_name="Pie de página")

    class Meta:
        db_table = 'indexgeneral'
        verbose_name = 'Configuración básica del sitio'
        verbose_name_plural = 'Configuración básica del sitio'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class IndexEnlacesInteres(models.Model):
    id_enlacesinteres = models.AutoField(primary_key=True)
    estado = models.BooleanField(verbose_name="Publicar este item")
    titulo = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    imagen = models.ImageField(upload_to='cabecera')

    class Meta:
        db_table = 'indexenlacesinteres'
        verbose_name = 'Enlace'
        verbose_name_plural = 'Index Enlaces de interés'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class IndexServicios(models.Model):
    id_serviciosindex = models.AutoField(primary_key=True)
    icono = models.CharField(max_length=100)
    titulo = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    estado = models.BooleanField(verbose_name="Publicar este item")

    class Meta:
        db_table = 'indexservicios'
        verbose_name = 'Servicio del index'
        verbose_name_plural = 'Index Servicios'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class transparencia_ano(models.Model):
    id_transparenciaano = models.AutoField(primary_key=True)
    nombre_ano = models.CharField(max_length=50)
    contenido = RichTextUploadingField(max_length=3000)

    class Meta:
        db_table = 'transparencia_ano'
        verbose_name = 'Año de Transparencia'
        verbose_name_plural = 'Transparencia Lista de Años'

    def __str__(self):
        return u'%s' % self.nombre_ano


@python_2_unicode_compatible
class transparencia_mes(models.Model):
    id_transparenciames = models.AutoField(primary_key=True)
    nombre_mes = models.CharField(max_length=50)

    class Meta:
        db_table = 'transparencia_mes'
        verbose_name = 'Mes de Transparencia'
        verbose_name_plural = 'Transparencia Lista de Meses'

    def __str__(self):
        return u'%s' % self.nombre_mes


@python_2_unicode_compatible
class transparencia_documentos(models.Model):
    id_tags = models.AutoField(primary_key=True)
    nombre_documento = models.CharField(max_length=200)
    subir_documento = models.FileField(max_length=200)
    nro_descargas = models.IntegerField()
    id_transparenciaano = models.ForeignKey(transparencia_ano, models.DO_NOTHING, db_column='id_transparenciaano')
    id_transparenciames = models.ForeignKey(transparencia_mes, models.DO_NOTHING, db_column='id_transparenciames')

    class Meta:
        db_table = 'transparencia_documentos'
        verbose_name = 'Transparencia Documento'
        verbose_name_plural = 'Transparencia Documentos'

    def __str__(self):
        return u'%s' % self.nombre_documento


@python_2_unicode_compatible
class ProcesosContratacionNivel1(models.Model):
    id_procesos = models.AutoField(primary_key=True)
    paginas_select = (('1', 'menú'), ('2', 'submenú'))
    tipo = models.CharField(max_length=150, choices=paginas_select)
    titulo = models.CharField(max_length=200)
    contenido = RichTextUploadingField(max_length=9999999, default="")

    class Meta:
        db_table = 'procesos1'
        verbose_name = 'Proceso Contratación Nivel 1'
        verbose_name_plural = 'Procesos Contratación Nivel 1'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class ProcesosContratacionNivel2(models.Model):
    id_procesos2 = models.AutoField(primary_key=True)
    paginas_select = (('1', 'menú'), ('2', 'submenú'))
    tipo = models.CharField(max_length=150, choices=paginas_select)
    id_procesos = models.ForeignKey(ProcesosContratacionNivel1, models.DO_NOTHING, db_column='id_procesos')
    titulo = models.CharField(max_length=200)
    contenido = RichTextUploadingField(max_length=9999999, default="")

    class Meta:
        db_table = 'procesos2'
        verbose_name = 'Proceso Contratación Nivel 2'
        verbose_name_plural = 'Procesos Contratación Nivel 2'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class ProcesosContratacionNivel3(models.Model):
    id_procesos3 = models.AutoField(primary_key=True)
    paginas_select = (('1', 'menú'), ('2', 'submenú'))
    tipo = models.CharField(max_length=150, choices=paginas_select)
    id_procesos2 = models.ForeignKey(ProcesosContratacionNivel2, models.DO_NOTHING, db_column='id_procesos2')
    titulo = models.CharField(max_length=200)
    contenido = RichTextUploadingField(max_length=9999999, default="")

    class Meta:
        db_table = 'procesos3'
        verbose_name = 'Proceso Contratación Nivel 3'
        verbose_name_plural = 'Procesos Contratación Nivel 3'

    def __str__(self):
        return u'%s' % self.titulo


@python_2_unicode_compatible
class RendicionAno(models.Model):
    id_rendicionano = models.AutoField(primary_key=True)
    nombre_ano = models.CharField(max_length=50)
    contenido = RichTextUploadingField(max_length=3000)

    class Meta:
        db_table = 'rendicionano'
        verbose_name = 'Rendición Año'
        verbose_name_plural = 'Rendición de cuenta años'

    def __str__(self):
        return u'%s' % self.nombre_ano


@python_2_unicode_compatible
class RendicionFase(models.Model):
    id_rendicionfase = models.AutoField(primary_key=True)
    nombre_fase = models.CharField(max_length=50)

    class Meta:
        db_table = 'rendicionfase'
        verbose_name = 'Rendición Fase'
        verbose_name_plural = 'Rendiciones de cuenta fases'

    def __str__(self):
        return u'%s' % self.nombre_fase


@python_2_unicode_compatible
class RendicionDocumentos(models.Model):
    id_tags = models.AutoField(primary_key=True)
    nombre_documento = models.CharField(max_length=200)
    subir_documento = models.FileField(max_length=200)
    nro_descargas = models.IntegerField()
    id_rendicionano = models.ForeignKey(RendicionAno, models.DO_NOTHING, db_column='id_rendicionano')
    id_rendicionfase = models.ForeignKey(RendicionFase, models.DO_NOTHING, db_column='id_rendicionfase')

    class Meta:
        db_table = 'rendiciondocumentos'
        verbose_name = 'Rendición de cuentas Documento'
        verbose_name_plural = 'Rendición de cuentas Documentos'

    def __str__(self):
        return u'%s' % self.nombre_documento


class Reclamos(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    reclamo = models.TextField(max_length=100)

    def __str__(self):
        return u'%s' % self.nombre
