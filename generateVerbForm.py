#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Funktion  : Generiert altgriechische Verbformen
#             Liefert eine Liste aus vier Ziffern die eine Form eindeutig
#             bestimmt. Als zweiten Rueckabewert wird die Form geliefert.
# Version   : 0.2.0
#
# Datum     : 2008-08-05
# Autor     : JS
#-------------------------------------------------------------------------------

#--- Include -------------------------------------------------------------------
import random as rand
import xmlparser
import sys

import quelle as q

#--- Global --------------------------------------------------------------------

VERSION = '0.2.0-0000'

LIST_MODUS = [0, 1, 2, 3,]
LIST_TEMPUS = []
LIST_GENUS = []
LIST_PERSON = []


def reverse_str(string):
    """ Dreht eine Variable vom Typ String string um. """
    out = ''

    for i in range(1, len(string)):
        out += string[-i]

    return out+string[0]

class VerbForm(object):
    """
    Erstellt eine altgriechische Verbform.

    Die Function 'generateForm()' liefert folgende Werte:
        [0] = eindeutige Zahlenkombination der Form in einer Liste
              ( zB [0, 0, 1, 4] fuer Indikativ Praesens Medium/Passiv 2. Pl.)
        [1] = die Form selbst ( zB paideuesJe )
        [2] = das Verb von der die Form gebildet wurde in der 1. Sg. Ind. Prae.
              ( zB peideuw )
    """
    def __init__(self):
        self.modus   = None      # der Modus der Form
        self.tempora = None      # Tempussystem der Form
        self.person  = None      # die Person der Form
        self.genus   = None      # Genus der Form

        self.verbalstock = self.prepairVST()


    def prepairVST(self):
        """ Bereitet die Verbalstoecke vor. """
        out = xmlparser.ParseXMLResource().getVerbalstock(q.VERBALSTOCK_FILE)
        if not out:
            out = ['paideuw']
        return out

    def generateForm(
                         self,
                         fontflag=0,
                         modus=666,
                         tempora=666,
                         genus=666,
                         person=666,
                         verb="no",
                         noAmb=0):

        if (modus != 666) and (tempora != 666) and (genus != 666) and (person != 666):
            self.modus = modus
            self.tempora = tempora
            self.genus = genus
            self.person = person
        else:
            self.modus = self.getModus()
            self.tempora = self.getTempora()
            self.genus = self.getGenus()
            self.person = self.getPerson()

        if verb != "no":
            self.form = self.killErstePerson(verb)
        else:
            self.form = self.getVerb()
            #self.form = 'paideu'


        self.fontflag = fontflag    # Welche Schriftart verwendet werden soll.
                                    # 0 = Symbol
                                    # 1 = Griech2 ( mit Akzenten )

        self.vals = [self.modus, self.tempora, self.genus, self.person]

        self.endung = q.endungen[self.modus][self.tempora][self.genus][self.person]



        verb = self.form

        self.getAugment()

        self.TempusSign = self.getTempusSign()

        self.checkTempusSign()

        if self.genus == 0:    # Fuegt  1.Per.Sg. hinzu
            verb += 'w'
        else:
            verb += 'omai'

        if verb != 'w' or 'omai':
            if self.fontflag == 1:
                if noAmb==0:
                    return (self.findAmbiguities(self.form, verb), self.makeGriech2(self.form), self.makeGriech2(verb))
                else:
                    return ([self.vals], self.makeGriech2(self.form), self.makeGriech2(verb))
            else:
                if noAmb==0:
                    return (self.findAmbiguities(self.form, verb), self.form, verb)
                else:
                    return ([self.vals], self.form, verb)

        else:
            # Wenn die resource.xml nicht vorhanden ist.
            return ([[0, 0, 0, 0]], self.verbalstock, self.verbalstock)

    def checkTempusSign(self):
        """
Prueft wie der Stamm und die Endung (TempusSign+Endung) verknuepft werden muessen,
ruft dafuer entsprechende Funktionen auf, die dies dann durchfuehren.
        """

        if self.checkContracta():
            return
        elif self.checkMuta():
            return
        else:
            self.form = self.form + self.TempusSign + self.endung
            return

    def starkesPerfekt(self, form):
        """ Entfernt das k aus der Bildung des (Plusquam)Perfekt. """
        if self.tempora in [4, 5]:
            return form[1:]
        else:
            return form


    def checkMuta(self):
        """ Pruft ob die Form ein Verba muta ist. """
        stammauslaut = self.form[-2:]
        status = 0 # Dieser Wert gibt an ob die Funktion eine weitere aufgerufen hat (1)

        if stammauslaut in ['tt'] or stammauslaut[-1] in ['g', 'k', 'c']: # c = Chie (x)
            status = 1
            self.setKStaemme() # Gutteral- oder K-Stamme
        elif stammauslaut in ['pt'] or stammauslaut[-1] in ['p', 'b', 'j']: # j = Phie
            status = 1
            self.setPStaemme() # Labial- oder P-Staemme
        elif stammauslaut[-1] in ['d', 't', 'J', 'x']: # J = Theta, x = Xi
            status = 1
            self.setTStaemme() # Dental- oder T-Staemme

        return status

    def setKStaemme(self):
        """ Fuegt form und Endung (TempusSign+Endung) unter beruecksichtigung
            der Regeln der Gutteral- / K-Staemme zusammen. """
        endung = self.starkesPerfekt(self.TempusSign) + self.endung
        form = self.form[:-1]
        if self.form[-2:] in ['tt']:
            form = self.form[:-2]

        if endung[:2] in ['sJ']:
            self.form = form + 'cJ' + endung[2:]
        elif endung[0] in ['s']:
            self.form = form + 'x' + endung[1:]
        elif endung[0] in ['m']:
            self.form = form + 'gm' + endung[1:]
        elif endung[0] in ['t']:
            self.form = form + 'kt' + endung[1:]
        elif endung[0] in ['J']:
            self.form = form + 'cJ' + endung[1:]
        else:
            self.form = self.form + self.starkesPerfekt(self.TempusSign) + self.endung

    def setPStaemme(self):
        """ Fuegt form und Endung (TempusSign+Endung) unter beruecksichtigung
            der Regeln der Labial- / P-Staemme zusammen. """
        endung = self.starkesPerfekt(self.TempusSign) + self.endung
        form = self.form[:-1]
        if self.form[-2:] in ['pt']:
            form = self.form[:-2]

        if endung[:2] in ['sJ']:
            self.form = form + 'jJ' + endung[2:]
        elif endung[0] in ['s']:
            self.form = form + 'y' + endung[1:]
        elif endung[0] in ['m']:
            self.form = form + 'mm' + endung[1:]
        elif endung[0] in ['t']:
            self.form = form + 'pt' + endung[1:]
        elif endung[0] in ['J']:
            self.form = form + 'jJ' + endung[1:]
        else:
            self.form = self.form + self.starkesPerfekt(self.TempusSign) + self.endung


    def setTStaemme(self):
        """ Fuegt form und Endung (TempusSign+Endung) unter beruecksichtigung
            der Regeln der Dental- / T-Staemme zusammen. """
        endung = self.TempusSign + self.endung
        form = self.form[:-1]

        if endung[:2] in ['sJ']:
            self.form = form + 'sJ' + endung[2:]
        elif endung[0] in ['s']:
            self.form = form + 's' + endung[1:]
        elif endung[0] in ['m']:
            self.form = form + 'sm' + endung[1:]
        elif endung[0] in ['k']:
            self.form = form + 'k' + endung[1:]
        elif endung[0] in ['t']:
            self.form = form + 'st' + endung[1:]
        elif endung[0] in ['J']:
            self.form = form + 'jJ' + endung[1:]
        else:
            self.form = self.form + self.TempusSign + self.endung

    def checkContracta(self):
        """ Prueft ob die Form ein Verba Contracta ist. Wenn nicht wird die
            Form mit der Endung zusammengesetzt. """
        last = self.form[-1] # get last char to determine the verba contracta
        status = 0 # Dieser Wert gibt an ob die Funktion eine weitere aufgerufen hat (1)
        if last == 'a':
            status = 1
            self.setAContracta()
        elif last == 'e':
            status = 1
            self.setEContracta()
        elif last == 'o':
            status = 1
            self.setOContracta()
#===============================================================================
#        else: # no contracta
#            self.form = self.form + self.TempusSign + self.endung
#===============================================================================

        return status

    def getContractaEndung(self):
        """
Gibt die Endung fuer die Verba Contrata zurueck, unter Beachtung der
Sonderregel, dass der Optativ Singular Aktiv auf -ih- gebildet wird.
        """
        if self.modus == 2 and self.person in [0, 1, 2] and self.genus == 0:
            return 'oih' + self.endung
        else:
            return self.TempusSign + self.endung


    def setAContracta(self):
        """ Kontrahiert die Form mit der Endung fuer A-Contracta. """
        endung = self.getContractaEndung()

        form = self.form[:-1]

        if endung[:2] in ['oi']:
            if self.fontflag != 1:
                self.form = form+'w'+endung[2:]
            else:
                self.form = form+'w#'+endung[2:] # Iotasubscriptum (#) if fontflag is 1 (Griech2)

        elif endung[:2] in ['ou']:
            self.form = form+'w'+endung[2:]

        elif endung[:2] in ['ei', 'h#']: # the 'h#' if  self.form is generated with Grich2 (not implemented yet)
            if self.fontflag != 1:
                self.form = form+'a'+endung[2:]
            else:
                self.form = form+'a#'+endung[2:] # Iotasubscriptum (#) if fontflag is 1 (Griech2)

        elif endung[:1] in ['o', 'w']:
            self.form = form+'w'+endung[1:]

        elif endung[:1] in ['e', 'h']:
            self.form = form+'a'+endung[1:]

        else:
            if form[-1] in ['i', 'a', 'e']: # Eier - Regel
                self.form = form+'a'+endung
            else:
                self.form = form+'h'+endung

    def setEContracta(self):
        """ Kontrahiert die Form mit der Endung fuer E-Contracta. """
        #endung = self.TempusSign + self.endung
        endung = self.getContractaEndung()

        form = self.form[:-1]

        if endung[:2] in ['oi', 'ei', 'ai', 'h#']:
            self.form = form+endung
        elif endung[:1] in ['w']:
            self.form = form+endung
        elif endung[:1] in ['e']:
            self.form = form+'ei'+endung[1:]

        elif endung[:1] in ['o']:
            self.form = form+'ou'+endung[1:]
        else:
            self.form = form+'h'+endung

    def setOContracta(self):
        """ Kontrahiert die Form mit der Endung fuer O-Contracta. """
        #endung = self.TempusSign + self.endung
        endung = self.getContractaEndung()
        form = self.form[:-1]

        if endung[:2] in ['ou']:
            self.form = form+'ou'+endung[2:]

        elif endung[:2] in ['ei', 'oi', 'h#']:
            self.form = form+'oi'+endung[2:]

        elif endung[:1] in ['o', 'e']:
            self.form = form+'ou'+endung[1:]

        elif endung[:1] in ['h', 'w']:
            self.form = form+'w'+endung[1:]

        else:
            self.form = form+'w'+endung

    def makeGriech2(self, word):
        word = word.replace('w', 'v')    # Omega
        word = word.replace('J', 'j')    # Theta
        word = word.replace('V', 'w')    # das Sigma am Ende einer Form
        word = word.replace('c', 'x')

        if word[0] in ['e', 'a', 'v', 'h']:
            word = word[0]+chr(0xf6)+word[1:] # spiritus: 0xf6 = oe


        if word.find(' (iotasub.!)') != -1:
            word = reverse_str(word)
            word = word.replace('h', '#h', 1)   # Das '#' (iotasub.) muss vor dem h stehen
                                                # da der String wieder umegedreht wird.
            word = reverse_str(word)

            word = word.replace(' (iotasub.!)', '')

        return word


    def getVerb(self):
        """
Waehlt ein Verb aus.
        """
        return self.killErstePerson(self.verbalstock[rand.randint(0, len(self.verbalstock)-1)])


    def getModus(self):
        """
Bestimmt einen Modus (Indikativ, Konjunktiv, Optativ, Imperativ).
        """
        modus = rand.sample([0, 1, 2, 3,],1)[0]
        return modus

    def getTempora(self):
        """ Bestimmt das Tempus der Form. """
        if self.modus == 0:      # Indikativ
            tempora = rand.sample([0, 1, 2, 3, 4, ], 1)[0]
            #tempora = rand.sample([0, 1, 2, 3, 4, 5, ], 1)[0]
        elif self.modus == 1:    # Konjunktiv
            tempora = rand.sample([0, 3], 1)[0]
            #tempora = rand.sample([0, 3], 1)[0]
        elif self.modus == 2:    # Optativ
            tempora = rand.sample([0, 2, 3], 1)[0]
            #tempora = rand.sample([0, 2, 3], 1)[0]
        elif self.modus == 3:    # Imperativ
            tempora = rand.sample([0, 3], 1)[0]
            #tempora = rand.sample([0, 3], 1)[0]
##        elif modus == 4:    # Partizip
##            tempora = rand.sample([1], 1)[0]

        return tempora

    def getGenus(self):
        """ Bestimmt das Genus der Form. """
        genus = rand.sample([0, 1], 1)[0] # aktiv oder passive/medium
        if self.modus == 3 and self.tempora == 4: # if Imperativ Perfect is selected,
            genus = 1                   # the genus hase to be passiv ( 1 ).
        if self.tempora  in [2, 3]:  # Anemerkung [4]
            genus = rand.sample([0, 1, 2], 1)[0]

        return genus

    def getPerson(self):
        """ Bestimmt die Person / Endung der Form. """
        if self.modus in [0, 1, 2]:  # Endung: Ind., Konj., Opt.
            person = rand.randint(0, 5)
        elif self.modus == 3:        # Imp.
            person = rand.sample([1,2,4,5], 1)[0]
##        elif self.modus == 4:        # Partizip
##            person = rand.randint(0, 7)
        return person

    def setSpecialAugment(self):
        """ Prueft die Art des Augments. """
        status = 0     # 0 wenn die Func. nichts veraendert hat, andernfalls 1
        newaugment = ''
        if self.form[0:2] in ['ai', 'au', 'ei', 'eu', 'oi']:
            augment = self.form[0:2]    # Augment ist zwei Zeichen lang
            form = self.form[2:]
        else:
            augment = self.form[0:1]    # Augment ist nur ein Zeichen lang
            form = self.form[1:]

        # replace the first chars with the augment
        if augment in ['ai', 'ei']:
            if self.fontflag == 1: # Wenn schriftart mit augment -> IotaSub (#)
                newaugment = 'h#'
            else:
                newaugment = 'h'
            status = 1
        elif augment in ['au', 'eu']:
            newaugment = 'hu'
            status = 1
        elif augment in ['oi']:
            if self.fontflag == 1:
                newaugment = 'w#'
            else:
                newaugment = 'w'
            status = 1
        elif augment in ['a', 'e']:
            newaugment = 'h'
            status = 1
        elif augment in ['o']:
            newaugment = 'w'
            status = 1
        elif augment in ['r']:
            newaugment = 'err'
            status = 1

        if augment in ['i', 'u']:
            status = 1

        # renew the form, now with the augment
        if len(newaugment) > 1:
            self.form = newaugment + form

        return status

    def getAugment(self):
        """ Prueft ob die Form ein Augment benoetigt. """
        augment = ''
        if self.modus == 0 and self.tempora in [1, 3]:    # tempora == Ind. Impf or Ind. Aor.?
            if self.setSpecialAugment() == 0:    # Fals kein unregelmaessiges Augment vorlieht
                augment = q.augmente[0]
        elif self.tempora in [4, 6]:     # if Perfekt or Futurum perfecti
            self.setReduplikation()
        elif self.tempora == 5:          # if plusquamperfekt
            self.setReduplikation(modus='plusquamperf')
        else:
            augment = ''

        self.form = augment+self.form

    def setReduplikation(self, modus='perf'):
        """ Fuegt self.form die Reduplikation an. """
        first = self.form[0] # get first char of the form to determine the reduplikation
        form = self.form[1:]
        redu = ''

        if first in ['k', 'p', 't', 'l', 'm', 'n', 'b', 'd']:
            redu = first+'e'+first
        elif first in ['s', 'r', 'z']: # eta als reduplikation
            redu = 'e'+first
        elif first in ['a']: # alpha -> eta
            redu = 'h'
        elif first in ['o']: # omikron -> omega
            redu = 'w'
        elif first in ['c']: # xie -> k + e + xie
            redu = 'ke'+first
        elif first in ['j']: # phie -> p + e + phie
            redu = 'pe'+first
        elif first in ['J']: # theta -> t + e + theat
            redu = 'te'+first
        elif first in ['r']:
            redu = 'err'

        if modus != 'plusquamperf':
            self.form = redu+form
        else:
            self.form = 'e'+redu+form

    def getTempusSign(self):
        """ Bestimmt das q.tempuszeichen der Form. """
        tempusSign = ''

        if (self.tempora in [2,3] and self.genus in [0, 1]): # Anmerk. [1]
            tempusSign += q.tempuszeichen[0]    # 's' als q.tempuszeichen hinzufuegen
            if self.modus == 2:      # if Opt.
                if self.tempora == 2:    #if Futur
                    tempusSign += 'oi'
                elif self.tempora == 3:  # if Aorist
                    tempusSign += 'ai'
        elif self.tempora in [2,3] and self.genus == 2:
            tempusSign += q.tempuszeichen[1]    # 'J'
            if self.tempora == 3:    # if Aorist
                if self.modus == 0:      # if Ind.
                    tempusSign += 'h'
                elif self.modus == 2:    # if Opt.
                    tempusSign += 'eih'
                elif self.modus == 4:
                    tempusSign += 'e'
            else:               # if Futur
                if self.modus == 0:      # if Ind.
                    tempusSign += 'hs'
                elif self.modus == 2:    # if Opt.
                    tempusSign += 'hsoi'
        elif self.modus == 2 and self.tempora == 0:   # Optativ Preasens
            tempusSign += q.tempuszeichen[3]
        elif self.tempora in [4, 5] and self.genus == 0:
            tempusSign += q.tempuszeichen[2]

        return tempusSign

    def getAllForms(self, grVerb):
        """ Bildet alle Formen von grVerb, und gibt diese in einer Dictionary zurueck. """

        allforms = []

        gen = VerbForm()    # Neue Instanz um das ueberschreiben der Variablen
                            # zu verhindern. (self.form, etc.)

#===============================================================================
#        for i in range(len(q.endungen)):
#            for j in range(len(q.endungen[i])):
#                for k in range(len(q.endungen[i][j])):
#                    for l in range(len(q.endungen[i][j][k])):
#                        allforms += [self.generateForm(modus=i, tempora=j, genus=k,
#                                                       person=l, verb=grVerb, noAmb=1)]
#===============================================================================

        for i in [0, 1, 2, 3]:
            if i in [0]:
                for j in [0, 1, 2, 3, 4,]:
                    for k in [0, 1]:
                        for l in [0, 1, 2, 3, 4, 5]:
                            allforms += [gen.generateForm(modus=i, tempora=j, genus=k,
                                                           person=l, verb=grVerb, noAmb=1)]
            elif i in [1]:
                for j in [0, 3, 4, ]:
                    for k in [0, 1]:
                        for l in [0, 1, 2, 3, 4, 5]:
                            allforms += [gen.generateForm(modus=i, tempora=j, genus=k,
                                                           person=l, verb=grVerb, noAmb=1)]
            elif i in [2]:
                for j in [0, 2, 3, 4, ]:
                    for k in [0, 1]:
                        for l in [0, 1, 2, 3, 4, 5]:
                            allforms += [gen.generateForm(modus=i, tempora=j, genus=k,
                                                           person=l, verb=grVerb, noAmb=1)]
            elif i in [3]:
                for k in [0, 1]:
                    if k in [0]:
                        for j in [0, 3, ]:
                            for l in [1, 2, 4, 5]:
                                allforms += [gen.generateForm(modus=i, tempora=j, genus=k,
                                                               person=l, verb=grVerb, noAmb=1)]
                    if k in [1, 2]:
                        for j in [0, 3, 4]:
                            for l in [1, 2, 4, 5]:
                                allforms += [gen.generateForm(modus=i, tempora=j, genus=k,
                                                               person=l, verb=grVerb, noAmb=1)]
        return allforms

    def killErstePerson(self, verb):
        """ Entfernt die Endung der ersten Person Singular im Indikativ Praesens,
aktiv und Medium. """
        if verb[-1] == 'w':
            return verb[:-1]
        elif verb[-3:] == 'mai':
            return verb[:-3]
        else:
            return verb

    def findAmbiguities(self, form, verb):
        """ Sucht nach Doppeldeutigkeiten (und vermerkt diese in der XML Datei.)
Gibt eine List mit Doppeldeutigkeiten zurueck. """



        allforms = self.getAllForms(self.killErstePerson(verb))

        #print allforms

        d = {}

        for i in allforms:
            if d.has_key(i[1]):
                temp = d[i[1]]
                new = i[0]


                for j in temp:
                    new += [j]
                d[i[1]] = new
            else:
                d[i[1]] = [i[0]][0]


#        try:
#            axxx = d[form]
#        except:
#            print 'error: ' + form + str(self.vals)

#        print d
#
#        if d[form]:
#            return d[form]

        #print d

        e = {}


        for (i, j) in d.iteritems():
            if len(j) != 1 and len(j) < 6:
                e[i] = j

        #print e

        if form in e:
            return e[form]
        else:
            return [self.vals]


#verbalstock = ['paideu', 'tima']



#===============================================================================
#         [ # Partizip ! not ! used
#          [],
#          [
#           ['as', 'antoV', '', '', '', '', '', ''],
#           ['is', 'ntos', 'nti', 'nta', 'ntes', 'ntwn', 'isin', 'ntas'],
#          ],
#          [],
#          []
#         ],
#===============================================================================
#        ]


#--- Main ----------------------------------------------------------------------

if __name__ == '__main__':
    v = VerbForm()
    for i in range(21):
        print v.generateForm()
#    print v.findAmbiguities("paideuw", "paideu")

