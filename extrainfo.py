#!/usr/bin/python
#-*-coding:utf8-*-

from bs4 import BeautifulSoup as Soup
import pandas as pd
import glob
import sys

L = glob.glob('./*.xml')



if __name__=='__main__':
    for f in L:
        soup = Soup(f)
        comprobante = soup.find('cfdi:comprobante')
        comprobantek = comprobante.attrs
        emisor = soup.find('cfdi:emisor')
        emisork = emisor.attrs
        receptor = soup.find('cfdi:receptor')
        receptork = receptor.attrs
        conceptos = soup.find('cfdi:conceptos')
        conceptosk = conceptos.attrs
        conceptosh = conceptos.find_all('cfdi:concepto')
        tfd = soup.find('tfd:timbrefiscaldigital')
        tfdk = tfd.attrs


