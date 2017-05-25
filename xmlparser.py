#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Funktion  : Dient zum Bearbeiten der XML - Resource Dateien.
# Version   : 0.2.0
#
# Datum     : 2008-08-05
# Autor     : JS
#-------------------------------------------------------------------------------

#--- Include -------------------------------------------------------------------
import xml.dom.minidom
import sys

#--- Global --------------------------------------------------------------------


class ParseXMLResource(object):
    def __init__(self):
        self.ret = []
        self.error = ''

    def getDOM(self, file):
        """ Oeffnet eine Datei (file) und gibt sie DOM Objekt zurueck. """

        try:
            dom = xml.dom.minidom.parse(file)
            return dom
        except IOError, (errno, strerror):
            self.error = "I/O error(%s): %s" % (errno, strerror)
        except:
            self.error = "Unexpected error:", sys.exc_info()[0]

    def getVerbalstock(self, file):
        """ Liefert eine Liste mit Verbalstoecken zurueck. """

        self.ret = []
        dom = self.getDOM(file)
        if dom:
            for vst in dom.getElementsByTagName("vst"):
                if vst.firstChild.nodeType == vst.TEXT_NODE:  # is TEXT_NODE?
                    self.ret += [str(vst.firstChild.nodeValue.strip())]
            if self.ret:
                return self.ret
            else:
                self.error = "I found NO vst nodes!"
        #else:
        #return self.error

    def getText(self, nodelist):
        rc = ""
        print nodelist
        #for node in nodelist:
        if nodelist.nodeType == nodelist.TEXT_NODE:
            rc = rc + nodelist.nodeValue.strip()
        return rc

    def getDifficultyLevels(self, file):
        """
Liefert eine Liste mit den Schwierigkeitsgraden.
        """

        dom = self.getDOM(file)
        self.level_d = {}

        level_list = ["name", "discr", "modus", "tempora", "genus", "person"]

        if dom:
            for root in dom.getElementsByTagName("griechisch"):
                for elem in root.getElementsByTagName("difficultylevels"):
                    for level in elem.getElementsByTagName("level"):
                        temp_list = []
                        for i in level_list:
                            for name in level.getElementsByTagName(i):
                                for k in name.childNodes:
                                    if k.nodeType == k.TEXT_NODE:
                                        temp_list += [str(k.nodeValue.strip())]
                        self.insertInLevelArray(temp_list)
        else:
            print "hoo? - getDifficultyLevels"

        return self.level_d

    def insertInLevelArray(self, level):
        """
Fuegt die von self.getDifficultyLevels() generierte Liste in self.level_d ein.
        """
        self.level_d[str(level[0])] = [
            str(level[1]),
            self.parseListe(list(level[2])),
            self.parseListe(list(level[3])),
            self.parseListe(list(level[4])),
            self.parseListe(list(level[5]))
        ]

    def parseListe(self, liste):
        """
Wandelt eine Liste von Numerischen-Strings in eine Liste von Integer um.
        """
        out = []
        for i in liste:
            out += [int(i)]
        return out


#--- Main ----------------------------------------------------------------------
if __name__ == "__main__":
    l = ParseXMLResource().getVerbalstock("resource.xml")
    print l
