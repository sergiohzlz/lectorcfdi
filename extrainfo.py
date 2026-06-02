#coding:utf8

from bs4 import BeautifulSoup as Soup
#import pandas as pd
import glob
import os
import argparse

"""
Version xml de cfdi 3.3 y cfdi 4
"""

class CFDI(object):
    def __init__(self, f):
        """
        Constructor que requiere en el parámetro una cadena con el nombre del
        cfdi.


        """
        soup                 = Soup(open(f,'r').read(),'lxml')
        #============componentes del cfdi============
        emisor             = soup.find('cfdi:emisor')
        receptor           = soup.find('cfdi:receptor')
        comprobante        = soup.find('cfdi:comprobante')
        tfd                = soup.find('tfd:timbrefiscaldigital')
        self.__complemento = soup.find('cfdi:complemento')  
        self.__pago20      = False if soup.find('pago20:doctorelacionado') is None else True 
        
        #print(comprobante)
        self.__version        = comprobante['version']     # type: ignore
        try:
            self.__folio      = comprobante['folio']       # type: ignore
        except KeyError:
            self.__folio      = 'NA'

        self.__uuid           = tfd['uuid']                # type: ignore
        self.__fechatimbrado  = tfd['fechatimbrado']       # type: ignore
        
        #============emisor==========================
        self.__emisorrfc      = emisor['rfc']              # type: ignore
        try:    
            self.__emisornombre   = emisor['nombre']       # type: ignore
        except:    
            self.__emisornombre   = emisor['rfc']          # type: ignore
        #============receptor========================    
        self.__receptorrfc    = receptor['rfc']            # type: ignore
        try:    
            self.__receptornombre = receptor['nombre']     # type: ignore
        except:    
            self.__receptornombre = receptor['rfc']        # type: ignore
        #============comprobante=====================
        self.__certificado    = comprobante['certificado'] # type: ignore
        self.__sello          = comprobante['sello']       # type: ignore
        self.__total          = round(float(comprobante['total']),2)    # type: ignore
        self.__subtotal       = round(float(comprobante['subtotal']),2) # type: ignore
        # self.__fecha_cfdi     = comprobante['fecha']       # type: ignore
        self.__conceptos      = soup.find_all(lambda e: e.name=='cfdi:concepto')
        # print(f"==> {not self.__complemento is None}")
        self.__n_conceptos    = len(self.__conceptos)
        tipo = comprobante['tipodecomprobante']            # type: ignore
        #============pago20==========================
        
        impuestos = self.__obten_impuestos(soup)
        # print(f"Impuestos obtenidos\n{impuestos}")
        # self.__traslados      = soup.find_all(lambda e: e.name=='cfdi:traslado' and
        #                                                 sorted(e.attrs.keys())==['importe','impuesto','tasaocuota','tipofactor'])
        # self.__retenciones    = soup.find_all(lambda e: e.name=='cfdi:retencion' and 
        #                                                 sorted(e.attrs.keys())==['importe','impuesto'])
        self.__traslados = self.__get_traslados(impuestos)

        self.__retenciones = self.__get_retenciones(impuestos)
        
        if(float(self.__version)==3.2):
            self.__tipo       = tipo
        else:
            tcomprobantes = {'I':'Ingreso', 'E':'Egreso', 'N':'Nomina', 'P':'Pagado'}
            self.__tipo       = tcomprobantes[tipo]

        if(self.__pago20):
        # if(self.__tipo in ['Egreso','Pagado']): # prueba
            complemento = self.__complemento
            # print(f"{self.__tipo}")
            children = complemento.find_all(attrs={'iddocumento':True}) # type: ignore
            if(len(children)==1):
                print("Lonitud uno")
                node = children[0]
                self.__uuid_complemento = node['iddocumento']
            else:
                print("Longitud varios")
                self.__uuid_complemento = 'VARIOS'
        else:
            self.__uuid_complemento = ''
        

        #============metodo de pago===================
        try:
            self.__metodopago     = comprobante['metodopago'] # type: ignore
        except:
            self.__metodopago     = self.__tipo
        #============tipo de pago=====================
        try:
            self.__formapago      = comprobante['formapago'] # type: ignore
        except:
            self.__formapago      = self.__tipo

        try:
            self.__moneda     = comprobante['moneda']        # type: ignore
        except KeyError as k:
            self.__moneda     = 'MXN'

        try:
            self.__lugar      = comprobante['lugarexpedicion'] # type: ignore
        except KeyError as k:
            self.__lugar      = u'México'

        try:
            self.__tcambio    = float(comprobante['tipocambio']) # type: ignore
        except:
            self.__tcambio    = 1.

        triva, trisr, trieps  = self.__calcula_traslados() # type: ignore
        # print(f"Traslado iva {triva}, isr {trisr}, ieps {trieps}")
        self.__triva          = round(triva,2)
        self.__trieps         = round(trieps,2)
        self.__trisr          = round(trisr,2)
        retiva, retisr        = self.__calcula_retenciones()
        self.__retiva         = round(retiva,2)
        self.__retisr         = round(retisr,2)
        self.atributos = self.__get_dicc_cfdi()

    def __str__(self):
        """
        Imprime el cfdi en el siguiente orden
        emisor, fecha de timbrado, tipo de comprobante, rfc emisor, uuid,_
        receptor, rfc receptor, subtotal, ieps, iva, retiva, retisr, tc, total
        """
        respuesta = '\t'.join( map(str, self.lista_valores))
        return respuesta
    
    def __obten_impuestos(self, sopa):
        if(self.__pago20):
            print("Pago20")
            return list(sopa.find('pago20:impuestosp').children)
        else:
            print("CFDI normal")
            return list(sopa.find('cfdi:impuestos').children)

    def __get_traslados(self, impuestos):
        if(self.__pago20):
            attr_g = 'pago20:trasladosp'
            attr_s = 'pago20:trasladop'
        else:
            attr_g = 'cfdi:traslados'
            attr_s = 'cfdi:traslado'
        
        traslados = [
            traslado
            for cont in impuestos
            if getattr(cont, 'name', None) == attr_g
            for traslado in cont.find_all(attr_s, recursive=False)
            
        ]
        
        # print(f"get_tras {traslados}")
        return traslados

    def __get_retenciones(self, impuestos):
        
        attr_g, attr_s = ('pago20:retencionesp', 'pago20:retencionp') if self.__pago20 else ('cfdi:retenciones', 'cfdi:retencion')

        retenciones = [
            retencion
            for cont in impuestos
            if getattr(cont, 'name', None) == attr_g
            for retencion in cont.find_all(attr_s, recursive=False)
        ]

        # print(f"get_ret {retenciones} y pago20 {self.__pago20}")
        return retenciones
    
    def __calcula_traslados(self):

        ## definicion del diccinario de respuesta
        if(self.__version=='3.2'):
            k_iva, k_isr, k_ieps = 'IVA', 'ISR', 'IEPS'
        elif(self.__version in ['3.3', '4.0']):
            k_iva, k_isr, k_ieps = '001', '002', '003'
        else:
            raise "Version no soportada"
        
        rets = {k_iva : 0., k_isr : 0., k_ieps : 0.}
        
        if(self.__version == '3.2'):

            for t in self.__traslados: # pyright: ignore[reportOptionalIterable]
                impuesto = t['impuesto']
                importe  = float(t['importe'])
                rets[impuesto] += importe

        elif(self.__version in ['3.3', '4.0']):

            for t in self.__traslados:
                if(self.__pago20):
                    lbl_atrib_impto, lbl_atrib_importe, lbl_factor = 'impuestop', 'importep', 'tipofactorp'
                else:
                    lbl_atrib_impto, lbl_atrib_importe, lbl_factor  = 'impuesto', 'importe', 'tipofactor'

                impuesto = t[lbl_atrib_impto]
                importe  = float(t[lbl_atrib_importe]) if t[lbl_factor].lower() != "exento" else 0
                rets[impuesto] += importe
        
        return rets[k_iva], rets[k_isr], rets[k_ieps]

    def __calcula_retenciones(self):

        ## definicion del diccinario de respuesta
        if(self.__version=='3.2'):
            k_iva, k_isr = 'IVA', 'ISR'
        elif(self.__version in ['3.3', '4.0']):
            k_iva, k_isr = '001', '002'
        else:
            raise "Version no soportada"
        
        rets = {k_iva : 0., k_isr : 0.}
        
    
        for t in self.__retenciones:
            if(self.__pago20):
                lbl_atrib_impto, lbl_atrib_importe, lbl_factor = 'impuestop', 'importep', 'tipofactorp'
            else:
                lbl_atrib_impto, lbl_atrib_importe, lbl_factor  = 'impuesto', 'importe', 'tipofactor'

            
            impuesto = t[lbl_atrib_impto]
            importe  = float(t[lbl_atrib_importe]) if t[lbl_factor].lower() != "exento" else 0
            rets[impuesto] += importe

        return rets[k_iva], rets[k_isr]

    @property
    def lista_valores(self):
        """
        Lista de valores en el mismo orden que
        self.__get_dicc_cfdi()
        """
        v  = [self.__uuid,           self.__fechatimbrado, self.__tipo] 
        v += [self.__emisorrfc,      self.__emisornombre   ]
        v += [self.__receptorrfc,    self.__receptornombre  ]
        v += [self.__folio]
        v += [self.__total, self.__trieps, self.__retisr]
        v += [self.__total, self.__triva, self.__retiva,   ]
        v += [self.__formapago, self.__tcambio, self.__metodopago  ]
        return v

    def __get_dicc_cfdi(self) -> dict:
        """
        Almacena los valores del cfdi en un 
        diccionario 
        """

        d = {}
        d["Folio_fiscal"] = (self.__uuid            , "Folio")
        d["Fecha_CFDI"]   = (self.__fechatimbrado   , "Fecha_CFDI")
        d["Tipo"]         = (self.__tipo            , "Tipo")
        d["RFC_Emisor"]   = (self.__emisorrfc       , "RFC Emisor")
        d["Emisor"]       = (self.__emisornombre    , "Emisor")
        d["RFC_Receptor"] = (self.__receptorrfc     , "RFC Receptor")
        d["Receptor"]     = (self.__receptornombre  , "Receptor")
        d["Total"]        = (self.__total           , "Total")
        d["IVA"]          = (self.__triva           , "IVA")
        d["Ret IVA"]      = (self.__retiva          , "Ret IVA")  
        d["Forma_pago"]   = (self.__formapago       , "Forma de pago")
        d["Moneda"]       = (self.__moneda          , "Moneda")
        d["Complemento"]  = (self.__uuid_complemento, "Folio complemento")
        d["ISR"]          = (self.__trisr           , "ISR")
        d["Ret ISR"]      = (self.__retisr          , "Ret ISR")
        return d

    @property
    def version(self):
        return self.__version
        
    @property
    def dic_cfdi(self):
        d = self.__get_dicc_cfdi()
        return { k:v[0] for k,v in d.items()}        

    @property 
    def columnas(self) -> list:
        d = self.__get_dicc_cfdi()
        return [v[1] for v in d.values()]

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
    
    @property
    def metodopago(self):
        return self.__metodopago
    
    @property
    def formapago(self):
        return self.__formapago
    
    @property
    def uuid_complemento(self):
        return self.__uuid_complemento


    @staticmethod
    def imprime_reporte(nf, nr):
        """
        Metodo generar un reporte de todos los xmls pasados en los 
        atributos

        Params:
        -------
        nf:  Número de archivos procesaod 
        nr:  Número de filas
        """
        reporte  = f"Número de archivos procesados:\t {nf}\n"
        reporte += f"Número de filas en tsv:\t {nr}\n"
        if(nf!=nr):
            reporte += "\n\n**** Atención ****\n"

        return reporte



get_listado_de_archivos = lambda direc : glob.glob(f"{os.path.join(direc, '*.xml')}")
#R = [ patt[1:].strip().lower() for patt in re.findall('(<cfdi:[A-z]*\s|<tfd:[A-z]*\s)',fxml)]


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Ejecucion de extractor')
    parser.add_argument ('--dir_salida', help='Directorio salida')
    parser.add_argument ('--archivo_salida', help='Archivo de salida')
    args = parser.parse_args()



    # directorio actual
    s_dir = os.path.dirname(os.path.realpath(__file__))
    # directorio de datos
    data_dir = os.path.join(s_dir, args.dir_salida)
    print(f"Procesando archivos de {data_dir}")
    # aquí deberían estar todos los cfdis
    listado_de_cfdis = get_listado_de_archivos(data_dir)

    archivo_salida = os.path.join(data_dir, args.archivo_salida)
    # donde se va a escribir el archivo de salida
    fout   = open(archivo_salida,'w')

    # columnas = CFDI.columnas
    # titulo   = '\t'.join(columnas)+'\n' # type : ignore
    # fout.write(titulo)
    
    nl = 0
    for f_cfdi in listado_de_cfdis:
        try:
            print(f"abriendo {f_cfdi}")
            rcfdi = CFDI(f_cfdi)
            vals = [v for k,v in rcfdi.dic_cfdi.items()]
            #vals = rcfdi.dic_cfdi
            strvals = ' \t '.join(map(str, vals))+'\n'
            fout.write(strvals)
            nl += 1
        except Exception as e:
            print(e)
            print(f"Error en archivo {f_cfdi}")
    fout.close()

    nr = len(listado_de_cfdis)
    rep = CFDI.imprime_reporte(nr, nl)
    print(rep)
