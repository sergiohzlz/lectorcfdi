#!/usr/bin/python
#-*-coding:utf8-*-

from bs4 import BeautifulSoup as Soup
#import pandas as pd
import glob
import sys
import re

"""
Version xml de cfdi 3.3
"""

class CFDI(object):
    def __init__(self, f):
        """
        Constructor que requiere en el parámetro una cadena con el nombre del
        cfdi.
        """
        fxml = open(f,'r').read()
        soup                 = Soup(fxml,'lxml')
        #============componentes del cfdi============
        emisor        = soup.find('cfdi:emisor')
        receptor      = soup.find('cfdi:receptor')
        comprobante   = soup.find('cfdi:comprobante')
        tfd           = soup.find('tfd:timbrefiscaldigital')
        self.__version        = comprobante['version']
        self.__uuid           = tfd['uuid']
        self.__fechatimbrado  = tfd['fechatimbrado']
        self.__traslados      = soup.find_all(lambda e: e.name=='cfdi:traslado')
        self.__retenciones    = soup.find_all(lambda e: e.name=='cfdi:retencion')
        #============emisor==========================
        self.__emisorrfc      = emisor['rfc']
        try:
            self.__emisornombre   = emisor['nombre'].encode('utf8')
        except:
            self.__emisornombre   = emisor['rfc']
        #============receptor========================
        self.__receptorrfc    = receptor['rfc']
        try:
            self.__receptornombre = receptor['nombre'].encode('utf8')
        except:
            self.__receptornombre = receptor['rfc']
        #============comprobante=====================
        self.__certificado    = comprobante['certificado']
        self.__sello          = comprobante['sello']
        self.__total          = round(float(comprobante['total']),2)
        self.__subtotal       = round(float(comprobante['subtotal']),2)
        self.__fecha_cfdi     = comprobante['fecha']
        try:
            self.__moneda     = comprobante['moneda']
        except KeyError as k:
            self.__moneda     = 'MXN'
        try:
            self.__lugar      = comprobante['lugarexpedicion']
        except KeyError as k:
            self.__lugar      = u'México'
        tipo = comprobante['tipodecomprobante']
        if(float(self.__version)==3.2):
            self.__tipo       = tipo
        else:
            tcomprobantes = {'I':'Ingreso', 'E':'Egreso', 'N':'Nomina', 'P':'Pagado'}
            self.__tipo       = tcomprobantes[tipo]
        try:
            self.__tcambio    = float(comprobante['tipocambio'])
        except:
            self.__tcambio    = 1.
        triva, trieps, trisr  = self.__calcula_traslados()
        self.__triva          = round(triva,2)
        self.__trieps         = round(trieps,2)
        self.__trisr          = round(trisr,2)
        retiva, retisr = self.__calcula_retenciones()
        self.__retiva         = round(retiva,2)
        self.__retisr         = round(retisr,2)
    def __str__(self):
        """
        Imprime el cfdi en el siguiente orden
        emisor, fecha de timbrado, tipo de comprobante, rfc emisor, uuid, receptor, rfc receptor, subtotal, ieps, iva, retiva, retisr, tc, total
        """
        # respuesta = ""
        # respuesta += self.__emisornombre.encode('utf8') + '\t'
        # respuesta += self.__fechatimbrado + '\t'
        # respuesta += self.__tipo + '\t'
        # respuesta += self.__emisorrfc + '\t'
        # respuesta += self.__uuid + '\t'
        # respuesta += self.__receptornombre.encode('utf8') + '\t'
        # respuesta += self.__receptorrfc + '\t'
        # respuesta += str(self.__subtotal) + '\t'
        # respuesta += str(self.__trieps) + "\t" + str(self.__triva) + '\t'
        # respuesta += str(self.__retiva) + "\t" + str(self.__retisr) + '\t'
        # respuesta += str(self.__tcambio) + '\t'
        # respuesta += str(self.__total)
        respuesta = '\t'.join( map(str, self.lista_valores))
        return respuesta
    def __calcula_traslados(self):
        triva, trieps, trisr = 0., 0., 0
        for t in self.__traslados:
            impuesto = t['impuesto']
            importe  = float(t['importe'])
            if(self.__version=='3.2'):
                if impuesto=='IVA':
                    triva += importe
                elif impuesto=='ISR':
                    trisr += importe
                elif impuesto=='IEPS':
                    trieps += importe
            elif(self.__version=='3.3'):
                try:
                    if(float(t['base'])): #no todos tienen este atributo
                        if impuesto=='002':
                            triva += importe
                        elif impuesto=='001':
                            trisr += importe
                        elif impuesto=='003':
                            trieps += importe
                except:
                    #print(t)
                    #en caso de que el traslado no tenga el atributo base
                    #entonces no hacemos nada
                    pass
        return triva, trieps, trisr
    def __calcula_retenciones(self):
        retiva, retisr = 0., 0.
        for t in self.__retenciones:
            if t['impuesto']=='ISR':
                retisr += float(t['importe'])
            elif t['impuesto']=='IVA':
                retiva += float(t['importe'])
        return retiva, retisr
    @property
    def lista_valores(self):
        v  = [self.__emisornombre,self.__fechatimbrado.encode('utf8'), self.__tipo, self.__emisorrfc ]
        v += [self.__uuid, self.__receptornombre, self.__receptorrfc ]
        v += [self.__subtotal, self.__trieps, self.__triva]
        v += [self.__retiva, self.__retisr, self.__tcambio, self.__total]
        return v
    @property
    def certificado(self):
        return self.__certificado
    @property
    def sello(self):
        return self.__sello
    @property
    def total(self):
        return self.__total
    @property
    def subtotal(self):
        return self.__subtotal
    @property
    def fechatimbrado(self):
        return self.__fechatimbrado
    @property
    def tipodecambio(self):
        return self.__tcambio
    @property
    def lugar(self):
        return self.__lugar
    @property
    def moneda(self):
        return self.__moneda
    @property
    def traslado_iva(self):
        return self.__triva
    @property
    def traslado_isr(self):
        return self.__trisr
    @property
    def traslado_ieps(self):
        return self.__trieps





def extraeinfo(f):
    fxml = open(f,'r').read()
    soup = Soup(fxml,"lxml")
    comprobante = soup.find('cfdi:comprobante')
    emisor      = soup.find('cfdi:emisor')
    domfiscal   = soup.find('cfdi:domiciliofiscal')
    regfiscal   = soup.find('cfdi:regimenfiscal')
    receptor    = soup.find('cfdi:receptor')
    domicilio   = soup.find('cfdi:domicilio')
    conceptos   = soup.find_all(lambda e: e.name=='cfdi:concepto')
    impuestos   = soup.find('cfdi:impuestos')
    traslados   = soup.find_all(lambda e: e.name=='cfdi:traslado')
    retenciones = soup.find_all(lambda e: e.name=='cfdi:retencion')
    tfd = soup.find('tfd:timbrefiscaldigital')

    iva, isr, ieps = 0.,0.,0.
    for t in traslados:
        if t['impuesto'] in ('IVA','002'):
            iva += float(t['importe'])
        elif t['impuesto'] in ('ISR','001'):
            isr += float(t['importe'])
        elif t['impuesto'] in ('IEPS','003'):
            ieps += float(t['importe'])

    retiva, retisr = 0., 0.
    for t in retenciones:
        if t['impuesto']=='ISR':
            retisr += float(t['importe'])
        elif t['impuesto']=='IVA':
            retiva += float(t['importe'])

    tc = comprobante.get('tipocambio',1.)

    try:
        emisornombre = emisor['nombre'].encode('utf8')
    except:
        emisornombre = emisor['rfc'].encode('utf8')

    try:
        receptornombre = receptor['nombre'].encode('utf8')
    except:
        receptornombre = receptor['rfc'].encode('utf8')

    tcomprobantes = {'I':'Ingreso', 'E':'Egreso', 'N':'Nomina', 'P':'Pagado'}
    tipocomprobante = comprobante['tipodecomprobante'].encode('utf8')
    if(len(tipocomprobante)==1):
        tipocomprobante = tcomprobantes[tipocomprobante]

    try:
        resumen = "{0} \t {1} \t {2} \t {3} \t {4} \t {5} \t {6} \t{7} \t {8} \t {9} \t {10} \t {11} \t {12} \t {13} ".format(\
                emisornombre, \
                tfd['fechatimbrado'].encode('utf8'), \
                tipocomprobante,\
                emisor['rfc'].encode('utf8'), \
                tfd['uuid'].encode('utf8'), \
                receptornombre, \
                receptor['rfc'].encode('utf8'), \
                comprobante['subtotal'].encode('utf8'), \
                str(ieps),str(iva),str(retiva),str(retisr), str(tc), \
                comprobante['total'].encode('utf8'))
    except KeyError as k:
        print("Error en {0}".f)
    return resumen


L = glob.glob('./*.xml')
#R = [ patt[1:].strip().lower() for patt in re.findall('(<cfdi:[A-z]*\s|<tfd:[A-z]*\s)',fxml)]

if __name__=='__main__':
    print("Emisor \t Fecha_CFDI \t Tipo \t  RFC_Emisor \t Folio_fiscal \t Receptor \t RFC_Receptor \t Subtotal \t  IEPS \t IVA \t Ret IVA \t Ret ISR \t TC \t Total")
    for f in L:
        try:
            #print("abriendo {0}".format(f))
            rcfdi = CFDI(f)
        except:
            assert "Error en archivo {0}".format(f)
        print(rcfdi)
