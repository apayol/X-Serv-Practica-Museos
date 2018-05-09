#!/usr/bin/python

from xml.sax.handler import ContentHandler
from xml.sax import make_parser, SAXParseException
import sys
from urllib import request
from .models import Museo

class myContentHandler(ContentHandler):


    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.nombre = ""
        self.accesibilidad = ""
        self.via_clase = ""
        self.via_nombre = ""
        self.via_numero = ""
        self.postal = ""
        self.localidad = ""
        self.barrio = ""
        self.distrito = ""
        self.enlace = ""
        self.descripcion = ""
        self.horario = ""
        self.telefono = ""
        self.email = ""
        

    def startElement (self, name, attrs):
        if name == "atributo":
            self.inItem = attrs.get("nombre")
        if attrs.get("nombre") in ["NOMBRE","ACCESIBILIDAD","CLASE-VIAL",
                                    "NOMBRE-VIA","NUM","CODIGO-POSTAL",
                                    "LOCALIDAD","BARRIO","DISTRITO",
                                    "CONTENT-URL","DESCRIPCION-ENTIDAD",
                                    "HORARIO","TELEFONO","EMAIL"]:
            self.inContent = True
            
    def endElement (self, name):
        if self.inItem == "NOMBRE":
            self.nombre = self.theContent
        elif self.inItem == "ACCESIBILIDAD":
            self.accesibilidad = self.theContent
        elif self.inItem == "CLASE-VIAL":
            self.via_clase = self.theContent
        elif self.inItem == "NOMBRE-VIA":
            self.via_nombre = self.theContent
        elif self.inItem == "NUM":
            self.via_numero = self.theContent
        elif self.inItem == "CODIGO-POSTAL":
            self.postal = self.theContent
        elif self.inItem == "LOCALIDAD":
            self.localidad = self.theContent
        elif self.inItem == "BARRIO":
            self.barrio = self.theContent
        elif self.inItem == "DISTRITO":
            self.distrito = self.theContent
        elif self.inItem == "CONTENT-URL":
            self.enlace = self.theContent
        elif self.inItem == "DESCRIPCION-ENTIDAD":
            self.descripcion = self.theContent
        elif self.inItem == "HORARIO":
            self.horario = self.theContent
        elif self.inItem == "TELEFONO":
            self.telefono = self.theContent
        elif self.inItem == "EMAIL":
            self.email = self.theContent
        self.inContent = False
        self.theContent = ""
        self.inItem = ""
        if name == "contenido":
            museo = Museo(nombre = self.nombre,
                        accesibilidad = self.accesibilidad,
                        via_clase = self.via_clase,
                        via_nombre = self.via_nombre,
                        via_numero = self.via_numero,
                        postal = self.postal,
                        localidad = self.localidad,
                        barrio = self.barrio,
                        distrito = self.distrito,
                        enlace = self.enlace,
                        descripcion = self.descripcion,
                        horario = self.horario,
                        telefono = self.telefono,
                        email = self.email)
            museo.save()

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def link_parse():
    link = 'https://datos.madrid.es/portal/site/egob/menuitem.'
    link += 'ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=0014'
    link += '9033f2201410VgnVCM100000171f5a0aRCRD&format=xml'
    link += '&file=0&filename=201132-0-museos&mgmtid=118f2fdb'
    link += 'ecc63410VgnVCM1000000b205a0aRCRD&preview=full'

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    xmlFile = request.urlopen(link)
    theParser.parse(xmlFile)

    print("Parse complete")
