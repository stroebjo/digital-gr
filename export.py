#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Funktion  : Stellt Funktionen zum Exportieren der erstellten Formen bereit.
# Version   : 0.1.0
#
# Datum     : 2008-08-3
# Autor     : JS
#-------------------------------------------------------------------------------

#--- Include -------------------------------------------------------------------
import quelle as q
import generateVerbForm as newForm

class html(object):
    def __init__(self):
        pass

    def endungen(self, save=0, modus=0):
        """
Gibt eine valide XHTML 1.0 Transitional Seite zurueck, in der die Endungen des
Formenprogramms stehen. Unterstuetzt zwei Modi (default=0):
    0 = die Endungen werden so ausegegeben wie sie in der Liste stehen
    1 = die Endungen werden in &alpha; etc. umgewandelt (HTML)
Des weiteren kann die Ausgabe in einer Datei geseichert werden:
    save != 0 bedeutet speichern, aus dem Wert von save ergibt sich der Dateiname.
        """

        row   = "row0"  # tr-Klasse -> CSS
        html  = ""      # Beinhaltet alle Tabellen (Aktiv, Medium, Passiv)
        table = ""      # Beinhaltet die aktuell zu bearbeitende Tabelle.
                        # Entweder Aktiv, Medium oder Passiv.

        for genus in  range(0, 3):
            table = "" # Reset table
            for i in range(0, 7):
                table += "\t\t<tr class=\"%s\">\n" % (row)
                row = self.changeRow(row)    # wechsel die tr-Klasse

                a = 1

                for j in range(len(q.endungen)): # -1 da Partizip nicht mitinbegriffen

                    # tds fuer Tempus und Person
                    if a:
                        table += "\t\t\t<td>" + q.solve_tempora[i] + "</td>\n"

                        table += "\t\t\t<td class=\"person\">\n"
                        try:
                            for k in range(len(q.endungen[j][i][genus])):
                                table += "\t\t\t\t" + q.solve_person[k] + "<br />\n"
                        except:
                            for loop in range(0, 6):
                                table += "\t\t\t\t" + q.solve_person[loop] + "<br />\n"
                        table += "\t\t\t</td>\n"

                        #Kontrollvariable, damit die td mit der Tempus Benennung nicht doppelt ist
                        a = 0

                    # td fuer Endungen
                    table += "\t\t\t<td class=\"endungen\">\n"
                    try:
                        for k in range(len(q.endungen[j][i][genus])):
                            table += "\t\t\t\t"
                            if modus:
                                table += self.encodeHTLM_dict(q.endungen[j][i][genus][k])
                            else:
                               table += q.endungen[j][i][genus][k]
                            table += "<br />\n"
                    except:
                        for loop in range(0, 6):
                            table += "\t\t\t\t<br />\n"
                    table += "\t\t\t</td>\n"

                table += "\t\t</tr>\n"
            html += "<h1 id=\"%(genus)s\">%(genus)s</h1>" % ({"genus":q.solve_genus[genus]})
            html += q.htmltable % (table)

        html = q.htmlhead + q.htmlbody %( q.discr, html )

        if save:
            try:
                f = file(str(save)+".html", 'w')
                f.write(html)
                f.close()
                return "Speichern erfolgreich!"
            except:
                return "Es trat ein Fehler auf!"
        else:
            return html

    def changeRow(self, row):
        if row == "row0":
            return "row1"
        else:
            return "row0"

    def encodeHTLM_dict(self, form):
        chars = {'a':'&alpha;',
                 'b':'&beta;',
                 'g':'&gamma;',
                 'd':'&delta;',
                 'e':'&epsilon;',
                 'z':'&zeta;',
                 'h':'&eta;',
                 'J':'&thetasym;',
                 'i':'&iota;',
                 'k':'&kappa;',
                 'l':'&lambda;',
                 'm':'&mu;',
                 'n':'&nu;',
                 'x':'&xi;',
                 'o':'&omicron;',
                 'p':'&pi;',
                 'r':'&rho;',
                 'V':'&sigmaf;',
                 's':'&sigma;',
                 't':'&tau;',
                 'u':'&upsilon;',
                 'f':'&phi;',
                 'c':'&chi;',
                 'y':'&psi;',
                 'w':'&omega;',
                 }
        neueform = ""
        for i in form:
            if i in chars:
                neueform += chars[i]
            else:
                neueform += i
        return neueform

    def formen(self, verb, save=0, modus=0):
        """
Gibt eine valide XHTML 1.0 Transitional Seite zurueck, in der alle Formen eines
Verbs stehen. Unterstuetzt zwei Modi (default=0):
    0 = die Endungen werden so ausegegeben wie sie in der Liste stehen
    1 = die Endungen werden in &alpha; etc. umgewandelt (HTML)
Des weiteren kann die Ausgabe in einer Datei geseichert werden:
    save != 0 bedeutet speichern, aus dem Wert von save ergibt sich der Dateiname.
        """

        row   = "row0"  # tr-Klasse -> CSS
        html  = ""      # Beinhaltet alle Tabellen (Aktiv, Medium, Passiv)
        table = ""      # Beinhaltet die aktuell zu bearbeitende Tabelle.
                        # Entweder Aktiv, Medium oder Passiv.

        for genus in  range(0, 3):
            table = "" # Reset table
            for i in range(0, 7):
                table += "\t\t<tr class=\"%s\">\n" % (row)
                row = self.changeRow(row)    # wechsel die tr-Klasse

                #Kontrollvariable, damit die td mit der Tempus Benennung nicht doppelt ist
                a = 1

                for j in range(len(q.endungen)): # -1 da Partizip nicht mitinbegriffen

                    # tds fuer Tempus und Person
                    if a:
                        table += "\t\t\t<td>" + q.solve_tempora[i] + "</td>\n"

                        table += "\t\t\t<td class=\"person\">\n"
#===============================================================================
#                        try:
#                            for k in range(len(q.endungen[j][i][genus])):
#                                table += "\t\t\t\t" + q.solve_person[k].replace(" ", "") + "<br />\n"
#                        except:
#                            for loop in range(0, 6):
#                                table += "\t\t\t\t" + q.solve_person[loop].replace(" ", "") + "<br />\n"
#===============================================================================

                        for loop in range(0, 6):
                            table += "\t\t\t\t" + q.solve_person[loop].replace(" ", "") + "<br />\n"

                        table += "\t\t\t</td>\n"

                        a = 0

                    # td fuer fuer die Form
                    table += "\t\t\t<td class=\"endungen\">\n"
                    try:
                        if j == 3: # Imperativ
                            for k in [0, 1, 2, 3, 4, 5]:
                                if k in [0, 3]: # 1. Person Sg und Pl.
                                    table +="\t\t\t\t<br />\n"
                                else:
                                    table += "\t\t\t\t"
                                    form = newForm.VerbForm().generateForm(fontflag=0,
                                               modus = j,
                                               tempora = i,
                                               genus = genus,
                                               person = k,
                                               verb = verb,
                                               noAmb = 1,
                                               )[1]
                                    if modus:
                                        table += self.encodeHTLM_dict(form).replace(" ", "&nbsp;")
                                        #table += self.encodeHTLM_dict(q.endungen[j][i][genus][k])
                                    else:
                                       table += form
                                       #table += q.endungen[j][i][genus][k]
                                    table += "<br />\n"
                        else:
                            for k in range(6):
                                table += "\t\t\t\t"
                                form = newForm.VerbForm().generateForm(fontflag=0,
                                           modus = j,
                                           tempora = i,
                                           genus = genus,
                                           person = k,
                                           verb = verb,
                                           noAmb = 1,
                                           )[1]
                                if modus:
                                    table += self.encodeHTLM_dict(form).replace(" ", "&nbsp;")
                                    #table += self.encodeHTLM_dict(q.endungen[j][i][genus][k])
                                else:
                                   table += form.replace(" ", "&nbsp;")
                                   #table += q.endungen[j][i][genus][k]
                                table += "<br />\n"
                    except:
                        for loop in range(0, 6):
                            table += "\t\t\t\t<br />\n"
                    table += "\t\t\t</td>\n"

                table += "\t\t</tr>\n"
            html += "<h1 id=\"%(genus)s\">%(genus)s</h1>" % ({"genus":q.solve_genusWeb[genus]})
            html += q.htmltable % (table)

        html = q.htmlhead % (verb, q.NAME, q.VERSION) + q.htmlbody %( q.discr, html )

        if save:
            try:
                f = file(str(save), 'w')
                f.write(html)
                f.close()
                return "Speichern erfolgreich!"
            except:
                return "Es trat ein Fehler auf!"
        else:
            return html


#--- Main ----------------------------------------------------------------------
if __name__ == "__main__":
    print html().formen(verb="luw", save="test.html", modus=1)
