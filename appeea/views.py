from __future__ import unicode_literals

# Login required
# Correo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import *

# consultas a servicios soap
import base64
from .servicios_consultas import obtener_servicio, obtener_documentos
from django.http import JsonResponse, HttpResponse
import requests
import xml.etree.ElementTree as ET

# recaptcha


def index(request):
    menus = Menu.objects.filter(habilitado=True)
    menu = ProcesosContratacionNivel1.objects.all()
    basic = IndexGeneral.objects.latest('id_indexgeneral')
    iei = IndexEnlacesInteres.objects.filter(estado=True)
    iservicios = IndexServicios.objects.filter(estado=True)
    noticias = Noticia.objects.filter(estado=True).order_by('-id_noticia')[:10]
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
    cabecera = ""
    try:
        cabecera = Cabecera.objects.get(pk=1)
    except:
        cabecera = Cabecera.objects.latest()
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
    paginator = Paginator(noticias, 12)
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
    #programas = ProgramasServicios.objects.latest(id_programasservicios)
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
    cabecera = Cabecera.objects.get(pk=7)
    page = request.GET.get('page', 1)
    paginator = Paginator(lista_noticias, 12)
    try:
        lista_noticias = paginator.page(page)
    except PageNotAnInteger:
        lista_noticias = paginator.page(1)
    except EmptyPage:
        lista_noticias = paginator.page(paginator.num_pages)

    ctx = {'lista_noticias': lista_noticias, 'lista_recomendaciones': lista_recomendaciones, 'cabecera': cabecera}
    return render(request, 'prueba.html', ctx)

def obtener_factura(request, num_doc):
    url = 'http://p36sapdbpo.redenergia.gob.ec:8000/XISOAPAdapter/MessageServlet?senderParty=&senderService=BS_ESB_PRD&receiverParty=&receiverService=&interface=SI_genfactxdoc_Sync_Out&interfaceNamespace=urn:cisnergia.gob.ec:esb:sap:genfactxdoc'
    headers = {'Content-Type': 'text/xml;charset=UTF-8', 'SOAPAction': 'http://sap.com/xi/WebService/soap1.1'}

    cuerpo_soap = f'''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:urn="urn:cisnergia.gob.ec:esb:sap:genfactxdoc">
       <soapenv:Header/>
       <soapenv:Body>
          <urn:MT_genfactxdoc_Out>
             <!--Optional:-->
             <Num_Doc>{num_doc}</Num_Doc>
          </urn:MT_genfactxdoc_Out>
       </soapenv:Body>
    </soapenv:Envelope>
    '''
    response = requests.post(url, data=cuerpo_soap, headers=headers, auth=('consultasw02', 'BEK~Gc]%rC7]8HZPU#F%2%vNjUWL=>Al(8JFxTeY'))

    # Parsear la respuesta XML
    root = ET.fromstring(response.content)

    factura_elem = root.find('.//Factura')
    if factura_elem is not None:
        factura_base64 = factura_elem.text
        # Decodificar la factura base64
        factura_bytes = base64.b64decode(factura_base64)

        # Crear una respuesta HTTP con el contenido del archivo PDF
        response = HttpResponse(factura_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=factura_{num_doc}.pdf'
        return response
    else:
        # Manejar el caso en el que no se encuentra el elemento 'Factura'
        # Puede ser que se quiera mostrar un mensaje de error o redirigir a una página de error.
        return render(request, 'consultas.html')

def info_cuenta(request):
    # Aquí se consume el servicio SOAP para obtener los detalles de la cuenta
    # utilizando el número de cédula o el número de cuenta
    error = None
    details = None

    if request.method == 'POST':
        try:
            tipo = request.POST.get('tipo')
            valor = request.POST.get('valor')
            page_size = request.POST.get('page_size')
            skip = request.POST.get('skip')
            details = obtener_servicio(tipo, valor, page_size, skip)

            if not details:
                error = "No se encontraron resultados para la consulta realizada."

            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'details': details, 'error': error})
            else:
                return render(request, "consultas.html", {'details': details, 'error': error})

        except Exception as e:
            #logger.error(f"Error en la vista info_cuenta: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'formulario_consultas.html')

def documentos(request):
    if request.method == 'POST':
        ctacontrato = request.POST.get('ctacontrato')
        anio = request.POST.get('anio')
        documentos = obtener_documentos(ctacontrato, anio)
        return JsonResponse(documentos)
    else:
        # Si la petición no es POST, renderizar la plantilla del formulario
        return render(request, 'consultas.html')

def servicioseea(request):
    return render(request, 'servicioseea.html')


def sgda_eea(request):
    """Render the SGDA page for Empresa Eléctrica Azogues."""
    return render(request, 'SGDA_EEA.html')