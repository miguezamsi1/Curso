import requests
import xml.etree.ElementTree as ET
import datetime
#
# # Autor: Beatriz Flores
# # Fecha: 03/04/2023
# # Descripción: Metodos para consumir servicios SOAP
#
# #Actualizacion Miguel Zambrano
# #Fecha: 10/07/2024
# # Actualizacion del consumo del web service
#
#
def formatoFecha(fecha_str):
    # Convertir el string en un objeto de fecha
     fecha = datetime.datetime.strptime(fecha_str, "%Y%m%d").date()

     # Darle formato a la fecha
     fecha_formateada = fecha.strftime("%d/%m/%Y")

     return fecha_formateada # Devuelve "28/03/2023"

# def obtener_servicio(tipo, valor):
#     #url = 'http://p14sapisu04.redenergia.gob.ec:8040/sap/bc/srt/rfc/sap/zws_obtieneservicios/310/zws_obtieneservicios/zws_obtieneservicios'   Esto estaba anterior hasta el aprostrofe"""
#     url = 'http://p8sapisu01r.redenergia.gob.ec:8010/sap/bc/srt/rfc/sap/zws_obtieneservicios/310/zws_obtieneservicios/zws_obtieneservicios'
#
#     headers = {'Content-Type': 'application/soap+xml;charset=UTF-8', 'SOAPAction': ''}
#
#     data = f'''
#         <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:sap-com:document:sap:rfc:functions">
#             <soap:Header/>
#             <soap:Body>
#                 <urn:ZBI_OBTIENESERVICIOS>
#                     <DIVISION>0802</DIVISION>
#                     <PAGE_SIZE></PAGE_SIZE>
#                     <SKIP></SKIP>
#                     <TIPO>{tipo}</TIPO>
#                     <VALOR>{valor}</VALOR>
#                 </urn:ZBI_OBTIENESERVICIOS>
#             </soap:Body>
#         </soap:Envelope>
#     '''
#     #response = requests.post(url, data=data, headers=headers, auth=('consultasw02', 'Azsw.2023'))  Esto estaba anterior"""
#     response = requests.post(url, data=data, headers=headers, auth=('CONSUPLANI', 'C0n5u1123**@'))
#
#     # Parsear la respuesta del servicio SOAP
#     root = ET.fromstring(response.content)
#     print('valorres devuelve servicio', root)
#     # Obtener los datos de la respuesta y almacenarlos en un diccionario
#     vacio = False
#     apellidos = root.find('.//APELLIDOS').text
#     cedula = root.find('.//CEDRUC').text
#     celular = root.find('.//CELULAR').text
#     email = root.find('.//EMAIL').text
#     nombres = root.find('.//NOMBRES').text
#     telefono = root.find('.//TELEFONO').text
#
#
#     # validar resultados
#     if telefono is None:
#         telefono = ''
#     if celular is None:
#         celular = ''
#     if email is None:
#         email = ''
#     if (cedula is None) or (nombres is None):
#         vacio = True
#
#     response_data = {
#         'APELLIDOS': apellidos,
#         #'APELLIDOS': root.find('.//APELLIDOS').text,
#         'CEDRUC': cedula,
#         'CELULAR': celular,
#         'EMAIL': email,
#         'NOMBRES': nombres,
#         'TELEFONO': telefono,
#         'SERVICIOS': [],
#     }
#     for item in root.findall('.//item'):
#         if item.find('.//VKONT') is not None:  # Se incluyo esta validacion para evitar el error por la paginacion
#             servicio = {
#                 'VKONT': item.find('.//VKONT').text,
#                 'MEDIDOR': item.find('.//MEDIDOR').text,
#                 'CUEN': item.find('.//CUEN').text,
#                 'DIRECCION': item.find('.//DIRECCION').text,
#                 'DEUDA': item.find('.//DEUDA').text,
#                 'ESTADOCONTRATO': item.find('.//ESTADOCONTRATO').text,
#                 'MESES': item.find('.//MESES').text,
#             }
#             response_data['SERVICIOS'].append(servicio)
#
#     # Validar el resultado y devolverlo
#     if vacio:
#         return {}
#     else:
#         return response_data


def obtener_servicio(tipo, valor, page_size, skip):
    #url = 'http://p8sapisu01r.redenergia.gob.ec:8010/sap/bc/srt/rfc/sap/zws_obtieneservicios/310/zws_obtieneservicios/zws_obtieneservicios'
    #url = 'http://p14sapisu04.redenergia.gob.ec:8040/sap/bc/srt/rfc/sap/zws_obtiene_documentos/310/zws_obtiene_documentos/zws_obtiene_documentos'
    url = 'http://p8sapisu01.redenergia.gob.ec:8010/sap/bc/srt/rfc/sap/zws_obtieneservicios/310/zws_obtieneservicios/zws_obtieneservicios'
    headers = {'Content-Type': 'application/soap+xml;charset=UTF-8', 'SOAPAction': ''}

    data = f'''
            <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:sap-com:document:sap:rfc:functions">
                <soap:Header/>
                <soap:Body>
                    <urn:ZBI_OBTIENESERVICIOS>
                        <DIVISION>0802</DIVISION>
                        <PAGE_SIZE>{page_size}</PAGE_SIZE>
                        <SKIP>{skip}</SKIP>
                        <TIPO>{tipo}</TIPO>
                        <VALOR>{valor}</VALOR>
                    </urn:ZBI_OBTIENESERVICIOS>
                </soap:Body>
            </soap:Envelope>
        '''
    #  response = requests.post(url, data=data, headers=headers, auth=('CONSUPLANI', 'C0n5u1123**@'))
    response = requests.post(url, data=data, headers=headers, auth=('EEAZOGUES', 'gXlCVE<eLUZxponeMiknLRsabRoAamtRoKZ3VgLF'))


    print(response.content)
    # Parsear la respuesta del servicio SOAP
    root = ET.fromstring(response.content)
    print('Valores devueltos por el servicio:', root)

    # Obtener los datos de la respuesta y almacenarlos en un diccionario
    vacio = False
    apellidos = root.find('.//APELLIDOS').text or ''
    cedula = root.find('.//CEDRUC').text or ''
    celular = root.find('.//CELULAR').text or ''
    email = root.find('.//EMAIL').text or ''
    nombres = root.find('.//NOMBRES').text or ''
    telefono = root.find('.//TELEFONO').text or ''


    # Validar resultados
    if not cedula or not nombres:
        vacio = True

    response_data = {
        'APELLIDOS': apellidos,
        'CEDRUC': cedula,
        'CELULAR': celular,
        'EMAIL': email,
        'NOMBRES': nombres,
        'TELEFONO': telefono,
        'SERVICIOS': [],
        'RESULT_SET': []
    }

    total_servicios = 0
    for item in root.findall('.//item'):
        if item.find('.//VKONT') is not None:
            servicio = {
                'VKONT': item.find('.//VKONT').text or '',
                'MEDIDOR': item.find('.//MEDIDOR').text or '',
                'CUEN': item.find('.//CUEN').text or '',
                'DIRECCION': item.find('.//DIRECCION').text or '',
                'DEUDA': item.find('.//DEUDA').text or '',
                'ESTADOCONTRATO': item.find('.//ESTADOCONTRATO').text or '',
                'MESES': item.find('.//MESES').text or ''
            }
            response_data['SERVICIOS'].append(servicio)
        if item.find('.//SIGUIENTE') is not None:
            result_set = {
                'ANTERIOR': item.find('.//ANTERIOR').text or '',
                'SIGUIENTE': item.find('.//SIGUIENTE').text or '',
                'TOTAL': item.find('.//TOTAL').text or '',
                'SKIP': item.find('.//SKIP').text or '',
                'PAGE_SIZE': item.find('.//PAGE_SIZE').text or ''
            }

            response_data['RESULT_SET'].append(result_set)


            total_servicios += 1


    # Actualizar el total de registros obtenidos
    response_data['TOTAL'] = total_servicios

    return response_data


def obtener_documentos(ctacontrato, anio):
    #  url = "http://p9sapisu02.redenergia.gob.ec:8020/sap/bc/srt/rfc/sap/zws_obtiene_documentos/310/zws_obtiene_documentos/zws_obtiene_documentos"
    #url = 'http://p14sapisu04.redenergia.gob.ec:8040/sap/bc/srt/rfc/sap/zws_obtiene_documentos/310/zws_obtiene_documentos/zws_obtiene_documentos'
    url = 'http://p8sapisu01.redenergia.gob.ec:8010/sap/bc/srt/rfc/sap/zws_obtiene_documentos/310/zws_obtiene_documentos/zws_obtiene_documentos'
    headers = {'Content-Type': 'application/soap+xml;charset=UTF-8', 'SOAPAction': 'urn:sap-com:document:sap:rfc:functions:ZWS_OBTIENE_DOCUMENTOS:ZBI_OBTIENE_DOCUMENTOSRequest'}

    cuerpo_soap = f'''
    <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:urn="urn:sap-com:document:sap:rfc:functions">
       <soap:Header/>
       <soap:Body>
          <urn:ZBI_OBTIENE_DOCUMENTOS>
             <CTACONTRATO>{ctacontrato}</CTACONTRATO>
             <YEAR>{anio}</YEAR>
          </urn:ZBI_OBTIENE_DOCUMENTOS>
       </soap:Body>
    </soap:Envelope>
    '''
    #   response = requests.post(url, data=cuerpo_soap, headers=headers, auth=('consultasw02', 'Azsw.2023'))
    response = requests.post(url, data=cuerpo_soap, headers=headers, auth=('EEAZOGUES', 'gXlCVE<eLUZxponeMiknLRsabRoAamtRoKZ3VgLF'))
    # Parsear la respuesta del servicio SOAP
    root = ET.fromstring(response.content)

    # Obtener los datos de la respuesta y almacenarlos en un diccionario
    response_data = {
        'DOCUMENTOS': [],
    }

    for item in root.findall('.//item'):
        documento = {
            'NUMDOCUMENTO': item.find('.//NUMDOCUMENTO').text,
            'FECDOC': formatoFecha(item.find('.//FECDOC').text),
            'NUMFAC': item.find('.//NUMFAC').text,
            'FECVEN': formatoFecha(item.find('.//FECVEN').text),
            'TIPDOC': item.find('.//TIPDOC').text,
            'VALORDOC': item.find('.//VALORDOC').text,
        }
        response_data['DOCUMENTOS'].append(documento)

    return response_data
