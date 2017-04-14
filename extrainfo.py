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
    resumen = "{0} \t {1} \t {2} \t {3} \t {4} \t {5} \t {6} \t{7} \t {8} \t {9} \t {10}".format(\
                emisor['nombre'].encode('utf8'),emisor['rfc'].encode('utf8'),tfd['uuid'].encode('utf8'), \
                receptor['nombre'].encode('utf8'),receptor['rfc'].encode('utf8'), \
                comprobante['total'].encode('utf8'), \
                str(ieps),str(iva),str(retiva),str(retisr), str(tc))
    return resumen


L = glob.glob('./*.xml')
#R = [ patt[1:].strip().lower() for patt in re.findall('(<cfdi:[A-z]*\s|<tfd:[A-z]*\s)',fxml)]

if __name__=='__main__':
    print("Emisor \t Emisor_RFC \t Folio fiscal \t Receptor \t Receptor_RFC \t Total \t IEPS \t IVA \t Ret IVA \t Ret ISR \t TC")
    for f in L[:15]:
        rcfdi = extraeinfo(f)
        print(rcfdi)

