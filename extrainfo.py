#!/usr/bin/python
#-*-coding:utf8-*-

from bs4 import BeautifulSoup as Soup
import pandas as pd
import glob
import sys
import re

def extraeinfo(f):
    fxml = open(f,'r').read()
    soup = Soup(fxml,"lxml")
    comprobante = soup.find('cfdi:comprobante')
    emisor      = soup.find('cfdi:emisor')
    domfiscal   = soup.find('cfdi:domiciliofiscal')
    regfiscal   = soup.find('cfdi:regimenfiscal')
    receptor    = soup.find('cfdi:receptor')
    domicilio   = soup.find('cfdi:domicilio')
    conceptos   = soup.find_all('cfdi:concepto')
    impuestos   = soup.find('cfdi:impuestos')
    traslado    = soup.find('cfdi:traslado')
    traslados   = soup.find_all('cfdi:traslado')
    retenciones = soup.find_all('cfdi:retencion')
    tfd = soup.find('tfd:timbrefiscaldigital')

    iva, isr, ieps = 0.,0.,0.
    for t in traslados:
        if t['impuesto']=='IVA':
            iva += float(t['importe'])
        elif t['impuesto']=='ISR':
            isr += float(t['importe'])
        elif t['impuesto']=='IEPS':
            ieps += float(t['importe'])

    retiva, retisr = 0., 0.
    for t in retenciones:
        if t['impuesto']=='ISR':
            retisr += float(t['importe'])
        elif t['impuesto']=='IVA':
            retiva += float(t['importe'])

    tc = float(comprobante.get('tipocambio',1.))

    try:
        emisornombre = emisor['nombre'].encode('utf8')
    except:
        emisornombre = emisor['rfc'].encode('utf8')

    try:
        receptornombre = receptor['nombre'].encode('utf8')
    except:
        receptornombre = receptor['rfc'].encode('utf8')

    try:
        resumen = "{0} \t {1} \t {2} \t {3} \t {4} \t {5} \t {6} \t{7} \t {8} \t {9} \t {10} \t {11} \t {12}".format(\
                emisornombre, \
                comprobante['fecha'].encode('utf8'), \
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
    print("Emisor \t Fecha_CFDI \t RFC_Emisor \t Folio_fiscal \t Receptor \t RFC_Receptor \t Subtotal \t  IEPS \t IVA \t Ret IVA \t Ret ISR \t TC \t Total")
    for f in L:
        try:
            rcfdi = extraeinfo(f)
        except:
            assert "Error en archivo {0}".format(f)
        print(rcfdi)

