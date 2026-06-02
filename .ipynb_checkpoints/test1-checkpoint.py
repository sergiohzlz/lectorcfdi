{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "1249644c",
   "metadata": {},
   "outputs": [],
   "source": [
    "import glob\n",
    "import json\n",
    "import extrainfo as C\n",
    "\n",
    "from importlib import reload"
   ]
  },
  {
   "cell_type": "raw",
   "id": "a080057a",
   "metadata": {},
   "source": [
    "Hacemos un par de ejemplos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "29f0d8ee",
   "metadata": {},
   "outputs": [],
   "source": [
    "# este es un cfdi normal\n",
    "# Traslados\n",
    "# <cfdi:Traslado Base=\"25000.000000\" Impuesto=\"002\" TipoFactor=\"Tasa\" TasaOCuota=\"0.160000\" Importe=\"4000.000000\"/>\n",
    "# Retenciones \n",
    "# <cfdi:Retencion Base=\"25000.000000\" Impuesto=\"002\" TipoFactor=\"Tasa\" TasaOCuota=\"0.106667\" Importe=\"2666.675000\"/>\n",
    "# <cfdi:Retencion Base=\"25000.000000\" Impuesto=\"001\" TipoFactor=\"Tasa\" TasaOCuota=\"0.100000\" Importe=\"2500.000000\"/>\n",
    "archivo_nrml = 'poncho/00f53dfe-fa00-4001-8786-f0596c4d6abe.xml'\n",
    "# este tiene pago_20\n",
    "# pago20:DoctoRelacionado IdDocumento=\"B442A737-D76C-490B-90FB-A8C247A9A0C9\" \n",
    "# <cfdi:Retencion Impuesto=\"002\" Importe=\"2666.68\"/>\n",
    "# <cfdi:Retencion Impuesto=\"001\" Importe=\"2500.00\"/>\n",
    "# <cfdi:Traslado Base=\"25000.00\" Impuesto=\"002\" TipoFactor=\"Tasa\" TasaOCuota=\"0.160000\" Importe=\"4000.00\"/>\n",
    "archivo_p20 = 'poncho/1f76c534-8559-427d-8bf3-a52fe0c3352c.xml'\n",
    "# varios conceptos y traslados\n",
    "archivo_v = 'poncho/5d811066-8720-4d85-ab63-fb09042082c1.xml'\n",
    "# archivo_v = 'poncho/8f9f345e-67dc-4053-9221-a04565b38ff4.xml\"'"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "34431f2a",
   "metadata": {},
   "source": [
    "Normal"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "c08ae9b4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<module 'extrainfo' from 'C:\\\\Users\\\\usuario\\\\Documents\\\\dev\\\\lectorcfdi\\\\extrainfo.py'>"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "reload(C)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "5fb829e4",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "CFDI normal\n",
      "<cfdi:traslado base=\"25000.000000\" importe=\"4000.000000\" impuesto=\"002\" tasaocuota=\"0.160000\" tipofactor=\"Tasa\"></cfdi:traslado>\n",
      "Traslado iva 0.0, isr 4000.0, ieps 0.0\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "{'Folio_fiscal': '00F53DFE-FA00-4001-8786-F0596C4D6ABE',\n",
       " 'Fecha_CFDI': '2026-03-19T17:37:58',\n",
       " 'Tipo': 'Ingreso',\n",
       " 'RFC_Emisor': 'COPL750415DR0',\n",
       " 'Emisor': 'LUIS EMILIO CORTES PIÃ‘ON',\n",
       " 'RFC_Receptor': 'CLM110216R54',\n",
       " 'Receptor': 'CONCEPTO LIBRE MEXICANO',\n",
       " 'Total': 23833.32,\n",
       " 'IVA': 0.0,\n",
       " 'Ret IVA': 0.0,\n",
       " 'Forma_pago': '03',\n",
       " 'Moneda': 'MXN',\n",
       " 'Complemento': '',\n",
       " 'ISR': 4000.0,\n",
       " 'Ret ISR': 0.0}"
      ]
     },
     "execution_count": 32,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cfdi = C.CFDI(archivo_nrml)\n",
    "cfdi.dic_cfdi"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "487ca234",
   "metadata": {},
   "source": [
    "Con varios conceptos"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "451b1c31",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "CFDI normal\n",
      "<cfdi:traslado base=\"14074.00\" importe=\"2251.84\" impuesto=\"002\" tasaocuota=\"0.160000\" tipofactor=\"Tasa\"></cfdi:traslado>\n",
      "Traslado iva 0.0, isr 2251.84, ieps 0.0\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "{'Folio_fiscal': '5D811066-8720-4D85-AB63-FB09042082C1',\n",
       " 'Fecha_CFDI': '2026-03-04T22:48:11',\n",
       " 'Tipo': 'Ingreso',\n",
       " 'RFC_Emisor': 'FCA130603EX5',\n",
       " 'Emisor': 'FIRMA CAR',\n",
       " 'RFC_Receptor': 'CLM110216R54',\n",
       " 'Receptor': 'CONCEPTO LIBRE MEXICANO',\n",
       " 'Total': 46089.36,\n",
       " 'IVA': 0.0,\n",
       " 'Ret IVA': 0.0,\n",
       " 'Forma_pago': '99',\n",
       " 'Moneda': 'MXN',\n",
       " 'Complemento': '',\n",
       " 'ISR': 2251.84,\n",
       " 'Ret ISR': 0.0}"
      ]
     },
     "execution_count": 36,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cfdi = C.CFDI(archivo_v)\n",
    "cfdi.dic_cfdi"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "077112a1",
   "metadata": {},
   "source": [
    "Con pago 20"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "id": "35e83fd2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Pago20\n",
      "Lonitud uno\n",
      "<pago20:trasladop basep=\"11859.88\" importep=\"1897.58\" impuestop=\"002\" tasaocuotap=\"0.160000\" tipofactorp=\"Tasa\"></pago20:trasladop>\n",
      "Traslado iva 0.0, isr 1897.58, ieps 0.0\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "{'Folio_fiscal': '1F76C534-8559-427D-8BF3-A52FE0C3352C',\n",
       " 'Fecha_CFDI': '2026-03-03T22:43:45',\n",
       " 'Tipo': 'Pagado',\n",
       " 'RFC_Emisor': 'VLE060918B86',\n",
       " 'Emisor': 'VOLKSWAGEN LEASING',\n",
       " 'RFC_Receptor': 'CLM110216R54',\n",
       " 'Receptor': 'CONCEPTO LIBRE MEXICANO',\n",
       " 'Total': 0.0,\n",
       " 'IVA': 0.0,\n",
       " 'Ret IVA': 0.0,\n",
       " 'Forma_pago': 'Pagado',\n",
       " 'Moneda': 'XXX',\n",
       " 'Complemento': 'B442A737-D76C-490B-90FB-A8C247A9A0C9',\n",
       " 'ISR': 1897.58,\n",
       " 'Ret ISR': 0.0}"
      ]
     },
     "execution_count": 33,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cfdi = C.CFDI(archivo_p20)\n",
    "cfdi.dic_cfdi"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2f41495d",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.18"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
