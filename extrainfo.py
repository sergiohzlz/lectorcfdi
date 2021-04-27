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
        self.__folio          = comprobante['folio']
        self.__uuid           = tfd['uuid']
        self.__fechatimbrado  = tfd['fechatimbrado']
        self.__traslados      = soup.find_all(lambda e: e.name=='cfdi:traslado' and
                                                        sorted(e.attrs.keys())==['importe','impuesto','tasaocuota','tipofactor'])
        self.__retenciones    = soup.find_all(lambda e: e.name=='cfdi:retencion' and 
                                                        sorted(e.attrs.keys())==['importe','impuesto'])
        #============emisor==========================
        self.__emisorrfc      = emisor['rfc']
        try:
            self.__emisornombre   = emisor['nombre']
        except:
            self.__emisornombre   = emisor['rfc']
        #============receptor========================
        self.__receptorrfc    = receptor['rfc']
        try:
            self.__receptornombre = receptor['nombre']
        except:
            self.__receptornombre = receptor['rfc']
        #============comprobante=====================
        self.__certificado    = comprobante['certificado']
        self.__sello          = comprobante['sello']
        self.__total          = round(float(comprobante['total']),2)
        self.__subtotal       = round(float(comprobante['subtotal']),2)
        self.__fecha_cfdi     = comprobante['fecha']
        self.__conceptos      = soup.find_all(lambda e: e.name=='cfdi:concepto')
        self.__n_conceptos    = len(self.__conceptos)

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
        retiva, retisr        = self.__calcula_retenciones()
        self.__retiva         = round(retiva,2)
        self.__retisr         = round(retisr,2)

    def __str__(self):
        """
        Imprime el cfdi en el siguiente orden
        emisor, fecha de timbrado, tipo de comprobante, rfc emisor, uuid,_
        receptor, rfc receptor, subtotal, ieps, iva, retiva, retisr, tc, total
        """
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
                if impuesto=='002':
                    triva += importe
                elif impuesto=='001':
                    trisr += importe
                elif impuesto=='003':
                    trieps += importe
        return triva, trieps, trisr

    def __calcula_retenciones(self):
        retiva, retisr = 0., 0.
        for t in self.__retenciones:
            impuesto = t['impuesto']
            importe  = float(t['importe'])
            if(self.__version=='3.2'):
                if(impuesto=='ISR'):
                    retisr += importe
                elif(impuesto=='IVA'):
                    retiva += importe
            elif(self.__version=='3.3'):
                if(impuesto=='002'):
                    retiva += importe
                elif(impuesto=='001'):
                    retisr += importe
         
        return retiva, retisr

    @property
    def lista_valores(self):
        v  = [self.__emisornombre,self.__fechatimbrado, self.__tipo, self.__emisorrfc ]
        v += [self.__uuid, self.__folio, self.__receptornombre, self.__receptorrfc ]
        v += [self.__subtotal, self.__trieps, self.__triva]
        v += [self.__retiva, self.__retisr, self.__tcambio, self.__total]
        return v

    @property
    def dic_cfdi(self):
        d = {}
        d["Emisor"]       = self.__emisornombre
        d["Fecha_CFDI"]   = self.__fechatimbrado
        d["Tipo"]         = self.__tipo
        d["RFC_Emisor"]   = self.__emisorrfc
        d["Folio_fiscal"] = self.__uuid
        d["Folio"]        = self.__folio
        d["Receptor"]     = self.__receptornombre
        d["RFC_Receptor"] = self.__receptorrfc
        d["Subtotal"]     = self.__subtotal
        d["IEPS"]         = self.__trieps
        d["IVA"]          = self.__triva
        d["Ret IVA"]      = self.__retiva
        d["Ret ISR"]      = self.__retisr
        d["TC"]           = self.__tcambio
        d["Total"]        = self.__total
        return d

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

    @property
    def n_conceptos(self):
        return self.__n_conceptos

    @property
    def conceptos(self):
        return self.__conceptos

    @property
    def folio(self):
        return self.__folio

    @staticmethod
    def columnas():
        return ["Emisor","Fecha_CFDI","Tipo","RFC_Emisor","Folio_fiscal","Folio","Receptor",
                "RFC_Receptor", "Subtotal","IEPS","IVA","Ret IVA","Ret ISR","TC","Total"]

    @staticmethod
    def imprime_reporte(nf, nr):
        reporte  = "Número de archivos procesados:\t {}\n".format(nf)
        reporte += "Número de filas en tsv:\t {}\n".format(nr)
        if(nf!=nr):
            reporte += "\n\n**** Atención ****\n"

        return reporte



L = glob.glob('./*.xml')
#R = [ patt[1:].strip().lower() for patt in re.findall('(<cfdi:[A-z]*\s|<tfd:[A-z]*\s)',fxml)]


if __name__=='__main__':
    salida = sys.argv[1]
    fout   = open(salida,'w')
    columnas = CFDI.columnas()
    titulo   = '\t'.join(columnas)+'\n'
    fout.write(titulo)
    nl = 0
    for f in L:
        try:
            #print("abriendo {0}".format(f))
            rcfdi = CFDI(f)
            dic = rcfdi.dic_cfdi
            vals = [dic[c] for c in columnas]
            strvals = ' \t '.join(map(str, vals))+'\n'
            fout.write(strvals)
            nl += 1
        except:
            assert "Error en archivo {0}".format(f)
    fout.close()

    nr = len(L)
    rep = CFDI.imprime_reporte(nr, nl)
    print(rep)
