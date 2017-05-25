#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Funktion  : Hier werden alle mehrfach genutzten Variablen gloabl definiert.
# Version   : 0.1.0
#
# Datum     : 2008-08-05
# Autor     : JS
#-------------------------------------------------------------------------------

VERSION = 'ALPHA 0.3.4'
NAME = 'Griechisch'
VERBALSTOCK_FILE = "resource.xml"

solve_modus   = ['Indikativ', 'Konjunktiv', 'Optativ', 'Imperativ']
solve_tempora = ['Praesens', 'Impf.', 'Futur', 'Aorist', 'Pefekt',
                 'Plusquamperfekt', 'Futurum perfecti']
solve_person  = ['1. Per. Sg.', '2. Per. Sg.', '3. Per. Sg.',
                 '1. Per. Pl.', '2. Per. Pl.', '3. Per. Pl.']
solve_genus   = ['Aktiv', 'Medium / Passiv', 'Passiv']
solve_genusWeb= ['Aktiv', 'Medium', 'Passiv']
endungen =[
         [ # Indikativ
          [ # Praesens
           ['w', 'eiV','ei','omen', 'ete','ousi(n)'], # Aktiv
           ['omai', 'h (iotasub.!)', 'etai', 'omeJa', 'esJe', 'ontai'],
          ],
          [ # Imperfekt
           ['on', 'eV', 'e(n)', 'omen', 'ete', 'on'],          # Aktiv
           ['omhn', 'ou', 'eto', 'omeJa', 'esJe', 'onto'],  # Medium/Passiv
          ],
          [ # Futur
           ['w', 'eiV', 'ei', 'omen', 'ete', 'ousi(n)'], # Aktiv
           ['omai', 'h (iotasub.!)', 'etai', 'omeJa', 'esJe', 'ontai'],# Medium
           ['omai', 'h (iotasub.!)', 'etai', 'omeJa', 'esJe', 'ontai'],# Passiv
          ],
          [ # Aorist
           ['a', 'aV', 'e(n)', 'amen', 'ate', 'an'],        # Aktiv
           ['amhn', 'w', 'ato', 'ameJa', 'asJe', 'anto'],   # Medium
           ['n', 'V', '', 'men', 'te', 'san'],              # Passiv
          ],
          [ # Pefekt
           ['a', 'aV', 'e(n)', 'amen', 'ate', 'asi(n)'],
           ['mai', 'sai', 'tai', 'meJa', 'sJe', 'ntai'],
          ],
          [ # Plusquamperfekt
           ['ein', 'eiV', 'ei', 'emen', 'ete', 'esan'],
           ['mhn', 'so', 'to', 'meJa', 'sJe', 'nto'],
          ],
          [ # Futurum perfecti
           ['', '', '', '', '', ''],
           ['omai', 'h (iotasub.!)', 'etai', 'omeJa', 'esJe', 'ontai'],
          ],
         ],

         [ # Konjunktiv
          [ # Praesens
           ['w', 'hV (iotasub.!)', 'h (iotasub.!)', 'wmen', 'hte', 'wsi(n)'],
           ['wmai', 'h (iotasub.!)', 'htai', 'wmeJa', 'hsJe', 'wntai'],
          ],
          [],   # Dummy
          [],   # Dummy
          [ # Aorist
           ['w','hV (iotasub.!)','h (iotasub.!)','wmen','hte','wsi(n)'],# Aktiv
           ['wmai', 'h (iotasub.!)', 'htai', 'wmeJa', 'hsJe', 'wntai'], #Medium
           ['w','hV (iotasub.!)','h (iotasub.!)','wmen','hte','wsi(n)'],#Passiv
          ],
          [ # Perfekt
           ['', '', '', '', '', ''],# Aktiv
           ['', '', '', '', '', ''],# Medium/Passiv
          ],
         ],

         [ # Optativ
          [ # Praesens
           ['mi', 'V', '', 'men', 'te', 'en'],# Aktiv
           ['mhn', 'o', 'to', 'meJa', 'sJe', 'nto'],# Medium/Passiv
          ],
          [],   # Dummy
          [ # Futur
           ['mi', 'V', '', 'men', 'te', 'en'],      # Aktiv
           ['mhn', 'o', 'to', 'meJa', 'sJe', 'nto'],# Medium
           ['mhn', 'o', 'to', 'meJa', 'sJe', 'nto'],# Passiv
          ],
          [ # Aorist
           ['mi', 'V', '', 'mhn', 'te', 'en'],      # Aktiv
           ['mhn', 'o', 'to', 'meJa', 'sJe', 'nto'],# Medium
           ['n', 'V', '', 'men', 'te', 'san'],      # Passiv
          ],
          [ # Perfekt
           ['', '', '', '', '', ''],
           ['', '', '', '', '', ''],
          ],
         ],

         [ # Imperativ
          [ # Praesens
           ['', 'e', 'etw', '', 'ete', 'ontwn'],        # Aktiv
           ['', 'ou', 'esJw', '', 'esJe', 'esJwn'],     # Medium/Passiv
          ],
          [],   # Dummy
          [],   # Dummy
          [ # Aorist
           ['', 'on', 'atw', '', 'ate', 'antwn'],   # Aktiv
           ['', 'ai', 'asJw', '', 'asJe', 'asJwn'], # Medium
           ['', 'hti', 'htw', '', 'hte', 'entwn'],  # Passiv
          ],
          [ # Perfekt
           [],  # Dummy
           ['', 'so', 'sJw', '', 'sJe', 'sJwn'],#Medium/Passiv, ein Aktiv gibt es nicht
          ],
         ],
        ]

tempuszeichen = ['s', 'J', 'k', 'oi'] # Anmerkung [2]
augmente = ['e', 'pe', 'epe']   # Anmerkung [3]

#===============================================================================
#     E X P O R T
#===============================================================================

htmlhead = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
        <title>%s Endungen &bull; %s %s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <style type="text/css">
        <!--
            body {
                    font-family: Verdana;
            }
            .row0 {
                background-color: #ddd;
            }
            .row1 {
                background-color: #eee;
            }
            tbody {
                color: #000;
            }
            th, td {
                padding: 2px;
            }
            td.person {
                text-align: right;
            }
        -->
        </style>
</head>"""

htmlbody = """<body>
<div id="container">
    <p>
        %s
    </p>
    <ul>
        <li><a href=\"#Aktiv\">Aktiv</a></li>
        <li><a href=\"#Medium\">Medium</a></li>
        <li><a href=\"#Passiv\">Passiv</a></li>
    </ul>
    %s
</div>
</body>
</html>
"""

discr = "Folgende Endungen werden momentan vom Programm (Version: %s) verwendet." % (VERSION)

htmltable = """    <table>
    <thead>
        <tr>
                <th></th>
                <th></th>
                <th>Indikativ</th>
                <th>Konjunktiv</th>
                <th>Optativ</th>
                <th>Imperativ</th>
                <th class="inactiv">Infinitiv</th>
                <th class="inactiv">Partizip</th>
        </tr>
    </thead>
    <tbody>
%s
        </tbody>
    </table>
"""

