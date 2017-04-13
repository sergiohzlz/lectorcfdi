# coding: utf-8
import glob
from xml.etree import ElementTree as ET
class CFDIElems(object):
    def __init__(self, elem):
        self.etElem = elem
    def __getitem__(self,name):
        res = self._getattr(name)
        if res is None:
            raise AttributeError, "Sin atributo '%s'" % name
        return res
    def __getattr__(self,name):
        res = self._getelem(name)
        if res is None:
            raise AttributeError, "Sin elemento '%s'" % name
        return res
    def _getelem(self,name):
        res = self.etElem.find(name)
        if res is None:
            return None
        return CFDIElems(res)
    def _getattr(self, name):
        return self.etElem.get(name)
    
class CFDITree(object):
    def __init__(self, fname):
        self.doc = ET.parse(fname)
    def __getattr__(self, name):
        if self.doc.getroot().tag != name:
            raise IndexError, "No hay elemento '%s'" % name
        
