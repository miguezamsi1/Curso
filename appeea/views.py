from __future__ import unicode_literals

# Login required
# Correo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import *


# recaptcha


def index(request):
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    iei = IndexEnlacesInteres.objects.filter(estado=True)
    iservicios = IndexServicios.objects.filter(estado=True)
    noticias = Noticia.objects.filter(estado=True).order_by('-id_noticia')[:5]
    enterate = Enterate.objects.filter(publicado=True).order_by('-id_enterate')
    # videos
    informa = Informa.objects.filter(publicado=True).order_by('-id_informa')
    einforma = EmpresaInforma.objects.filter(publicado=True).order_by('-id_informa')
    elista = []
    lista = []
    for c in informa:
        enlace = c.link.split('=')
        lista.append({'link': enlace[1], 'titulo': c.titulo})
    for c in einforma:
        enlace = c.link.split('=')
        elista.append({'link': enlace[1], 'titulo': c.titulo})
    cabecera = Cabecera.objects.filter(referencia='1').order_by('-pk')[:1]
    ctx = {'menus': menus, 'menu': menu, 'basic': basic, 'iei': iei, 'iservicios': iservicios, 'noticias': noticias,
           'enterate': enterate, 'informa': lista, 'einforma': elista, 'cabecera': cabecera}
    return render(request, 'index.html', ctx)


def noticias(request):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    search = ""
    if request.method == "POST":
        search = request.POST["search"]
        qset = (Q(descripcion__icontains=search) | Q(contenido__icontains=search))
        noticias = Noticia.objects.filter(qset)
    else:
        noticias = Noticia.objects.all()
    cabecera = Cabecera.objects.get(referencia='5')
    page = request.GET.get('page', 1)
    paginator = Paginator(noticias, 6)
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        noticias = paginator.page(1)
    except EmptyPage:
        noticias = paginator.page(paginator.num_pages)
    categorias = TagsNoticia.objects.all()
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'basic': basic, 'cabecera': cabecera,
           'search': search, 'noticias': noticias, 'categorias': categorias, 'cabecera': cabecera}
    return render(request, 'noticias.html', ctx)


def noticias_cat(request, ide, url):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    # noticias = Noticia.objects.all()
    cabecera = Cabecera.objects.get(referencia='5')
    search = ""
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    noticias = Noticia.objects.filter(tags__id_tags=ide)

    page = request.GET.get('page', 1)
    paginator = Paginator(noticias, 6)
    try:
        noticias = paginator.page(page)
    except PageNotAnInteger:
        noticias = paginator.page(1)
    except EmptyPage:
        noticias = paginator.page(paginator.num_pages)
    categorias = TagsNoticia.objects.all()
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'noticias': noticias, 'categorias': categorias}
    return render(request, 'noticias.html', ctx)


def noticia_individual(request, ide, url):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    cabecera = Cabecera.objects.get(referencia='5')
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    noticias = Noticia.objects.get(id_noticia=ide)
    categorias = TagsNoticia.objects.all()
    enterate = Enterate.objects.all().order_by('-id_enterate')[:2]
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'noticias': noticias, 'categorias': categorias, 'enterate': enterate, }
    return render(request, 'noticia_individual.html', ctx)


def programasservicios(request):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    cabecera = get_or_none(Cabecera, referencia='5')
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    programas = ProgramasServicios.objects.latest(id_programasservicios)
    categorias = TagsNoticia.objects.all()
    enterate = Enterate.objects.all().order_by('-id_enterate')[:2]
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'categorias': categorias, 'enterate': enterate, }
    return render(request, 'programas_servicios.html', ctx)


def institucion(request):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    institucion = Institucion.objects.filter(estado=True)
    cabecera = get_or_none(Cabecera, referencia='2')
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'basic': basic, 'institucion': institucion,
           'cabecera': cabecera}
    return render(request, 'institucion.html', ctx)


def institucion_individual(request, ide, url):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    cabecera = get_or_none(Cabecera, referencia='6')
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    institucion = Institucion.objects.get(id_institucion=ide)
    enterate = Enterate.objects.all().order_by('-id_enterate')[:2]
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'institucion': institucion, 'enterate': enterate}
    return render(request, 'institucion_individual.html', ctx)


def servicios(request):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    servicios = Servicios.objects.filter(estado=True)
    cabecera = get_or_none(Cabecera, referencia='2')
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'basic': basic, 'servicios': servicios,
           'cabecera': cabecera}
    return render(request, 'servicios.html', ctx)


def servicios_individual(request, ide, url):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    cabecera = get_or_none(Cabecera, referencia='6')
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    servicios = Servicios.objects.get(id_institucion=ide)
    enterate = Enterate.objects.all().order_by('-id_enterate')[:2]
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'servicios': servicios, 'enterate': enterate}
    return render(request, 'servicios_individual.html', ctx)


from collections import defaultdict


def transparencia(request):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    cabecera = get_or_none(Cabecera, referencia='4')
    # anios = transparencia_ano.objects.all()
    # meses = transparencia_mes.objects.all()
    # documentos = transparencia_documentos.objects.all().annotate(dcount=Count('id_transparenciaano'))
    documentos = defaultdict(list)
    anios = transparencia_ano.objects.all()
    for result in transparencia_documentos.objects.values('id_transparenciames__nombre_mes',
                                                          'nombre_documento').order_by('id_transparenciaano',
                                                                                       'nombre_documento'):
        documentos[result['id_transparenciames__nombre_mes']].append(result['nombre_documento'])
    documentos = dict(documentos)
    # print(documentos)
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'basic': basic, 'cabecera': cabecera,
           'documentos': documentos, 'anios': anios}
    return render(request, 'transparencia.html', ctx)


def menu(request, ide):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    cont = Menu.objects.get(habilitado=True, id_tags=ide)

    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    cabecera = get_or_none(Cabecera, referencia='4')
    ctx = {'iservicios': iservicios, 'cont': cont, 'menus': menus, 'menu': menu, 'basic': basic, 'cabecera': cabecera}
    return render(request, 'menu.html', ctx)


def transparenciaanio(request, ide):
    iservicios = IndexServicios.objects.filter(estado=True)
    suma = 0
    if request.method == "POST":
        ide = request.POST['ide']
        suma = transparencia_documentos.objects.get(pk=ide).nro_descargas + 1
        transparencia_documentos.objects.filter(pk=ide).update(nro_descargas=suma)
        url = request.POST['url']
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    cabecera = get_or_none(Cabecera, referencia='4')
    # anios = transparencia_ano.objects.all()
    # meses = transparencia_mes.objects.all()
    # documentos = transparencia_documentos.objects.all().annotate(dcount=Count('id_transparenciaano'))
    documentos = defaultdict(list)
    anios = transparencia_ano.objects.all()
    for result in transparencia_documentos.objects.filter(id_transparenciaano=ide).values('pk',
                                                                                          'id_transparenciames__nombre_mes',
                                                                                          'nombre_documento',
                                                                                          'subir_documento',
                                                                                          'nro_descargas').order_by(
        'id_transparenciaano', 'nombre_documento'):
        documentos[result['id_transparenciames__nombre_mes']].append(
            {'nombre': result['nombre_documento'], 'documento': result['subir_documento'],
             'nro_descargas': result['nro_descargas'], 'pk': result['pk']})
    documentos = dict(documentos)
    # print(documentos)
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'basic': basic, 'cabecera': cabecera,
           'documentos': documentos, 'anios': anios}
    return render(request, 'transparencia_anio.html', ctx)


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def procesoscontratacion1(request, ide):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    cabecera = get_or_none(Cabecera, referencia='6')
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    proceso = ProcesosContratacionNivel1.objects.get(id_procesos=ide)
    enterate = Enterate.objects.all().order_by('-id_enterate')[:2]
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'proceso': proceso, 'enterate': enterate}
    return render(request, 'procesoscontratacion.html', ctx)


def procesoscontratacion2(request, ide, ide2):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    cabecera = get_or_none(Cabecera, referencia='6')
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    proceso = ProcesosContratacionNivel2.objects.get(id_procesos2=ide2)
    enterate = Enterate.objects.all().order_by('-id_enterate')[:2]
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'proceso': proceso, 'enterate': enterate}
    return render(request, 'procesoscontratacion.html', ctx)


def procesoscontratacion3(request, ide, ide2, ide3):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    cabecera = get_or_none(Cabecera, referencia='6')
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    proceso = ProcesosContratacionNivel3.objects.get(id_procesos3=ide3)
    enterate = Enterate.objects.all().order_by('-id_enterate')[:2]
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'cabecera': cabecera, 'basic': basic,
           'proceso': proceso, 'enterate': enterate}
    return render(request, 'procesoscontratacion.html', ctx)


def rendicion(request):
    iservicios = IndexServicios.objects.filter(estado=True)
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    cabecera = get_or_none(Cabecera, referencia='4')
    # anios = transparencia_ano.objects.all()
    # meses = transparencia_mes.objects.all()
    # documentos = transparencia_documentos.objects.all().annotate(dcount=Count('id_transparenciaano'))
    documentos = defaultdict(list)
    anios = RendicionAno.objects.all()
    for result in RendicionDocumentos.objects.values('id_rendicionfase__nombre_fase', 'nombre_documento').order_by(
            'id_rendicionano', 'nombre_documento'):
        documentos[result['id_rendicionfase__nombre_fase']].append(result['nombre_documento'])
    documentos = dict(documentos)
    # print(documentos)
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'basic': basic, 'cabecera': cabecera,
           'documentos': documentos, 'anios': anios}
    return render(request, 'rendicion.html', ctx)


def rendicionanio(request, ide):
    iservicios = IndexServicios.objects.filter(estado=True)
    suma = 0
    if request.method == "POST":
        ide = request.POST['ide']
        suma = RendicionDocumentos.objects.get(pk=ide).nro_descargas + 1
        RendicionDocumentos.objects.filter(pk=ide).update(nro_descargas=suma)
        url = request.POST['url']
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    cabecera = get_or_none(Cabecera, referencia='4')
    documentos = defaultdict(list)
    anios = RendicionAno.objects.all()
    for result in RendicionDocumentos.objects.filter(id_rendicionano=ide).values('pk', 'id_rendicionfase__nombre_fase',
                                                                                 'nombre_documento', 'subir_documento',
                                                                                 'nro_descargas').order_by(
        'id_rendicionano', 'nombre_documento'):
        documentos[result['id_rendicionfase__nombre_fase']].append(
            {'nombre': result['nombre_documento'], 'documento': result['subir_documento'],
             'nro_descargas': result['nro_descargas'], 'pk': result['pk']})
    documentos = dict(documentos)
    # print(documentos)
    ctx = {'iservicios': iservicios, 'menus': menus, 'menu': menu, 'basic': basic, 'cabecera': cabecera,
           'documentos': documentos, 'anios': anios}
    return render(request, 'rendicion_anio.html', ctx)


def prueba(request):
    lista_noticias = Noticia.objects.all()
    lista_recomendaciones = Noticia.objects.all().order_by('-fechap')[:6]
    ctx = {'lista_noticias': lista_noticias, 'lista_recomendaciones': lista_recomendaciones}
    return render(request, 'prueba.html', ctx)
