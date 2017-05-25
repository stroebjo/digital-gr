#!/usr/bin/python

#-------------------------------------------------------------------------------
# Funktion  : Stellt eine GUI fuer generateVerbForm bereit. Ausserdem wandelt
#             es die Ausgabe von generateVerbForm in eine fuer Menschen
#             verstaendliche Form (umwandlung der Zahlen in Indikativ, Konjuktiv
#             , Person, etc.).
# Version   : 0.3.3
#
# Datum     : 2008-08-05
# Autor     : JS
#-------------------------------------------------------------------------------

#--- Include -------------------------------------------------------------------
import random as rand
import wx
#import os
#import sys

import xmlparser
import generateVerbForm as newForm
import quelle as q
import export

#--- Global --------------------------------------------------------------------

ID_STAT = 2
ID_DTERMINE = 3
ID_BUILD = 4
ID_VERSION = 5



#--- Func ----------------------------------------------------------------------

class MyPopupMenu(wx.Menu):
		""" Erstellt das PopUp-Meneu ( rechte Maustaste ). """
		def __init__(self, parent):
				wx.Menu.__init__(self)

				self.parent = parent

				minimize = wx.MenuItem(self, wx.NewId(), 'Minimize')
				self.AppendItem(minimize)
				self.Bind(wx.EVT_MENU, self.OnMinimize, id=minimize.GetId())

				close = wx.MenuItem(self, wx.NewId(), 'Close')
				self.AppendItem(close)
				self.Bind(wx.EVT_MENU, self.OnClose, id=close.GetId())

		def OnMinimize(self, event):
				self.parent.Iconize()

		def OnClose(self, event):
				self.parent.Close()

class Tools(wx.Panel):
	"""
Klasse die es ermoeglicht eine bestimmte Form vom Programm bilden zu lassen.
	"""

	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1)
		self.parent = parent
		self.fontmodus = 0

		sizer = wx.BoxSizer(wx.VERTICAL)

		radios = self.AddRadios()
		sizer.Add(radios, flag=wx.CENTER | wx.TOP, border=10)

		vonSizer = wx.BoxSizer(wx.HORIZONTAL)

		bold = wx.Font( 12,  wx.NORMAL, wx.NORMAL, wx.FONTWEIGHT_BOLD, False,)

# von text ------------------------------------------------------------------
		von = wx.StaticText(self, -1, "von:")
		von.SetFont(bold)

		vonSizer.Add(von, flag=wx.TOP, border=12)

		self.vonVerb = wx.TextCtrl(self, -1, size=(150, 28))
		vonSizer.Add(self.vonVerb, flag=wx.TOP | wx.LEFT, border=10)

		self.vonButton= wx.Button(self, -1, 'Bilde die eingestellte Form', size=(180, 23))
		vonSizer.Add(self.vonButton, flag=wx.TOP | wx.LEFT, border=12)


		sizer.Add(vonSizer, flag=wx.LEFT, border=10)

		self.output = wx.StaticText(self, -1, '\n\n')
		sizer.Add(self.output, flag=wx.TOP | wx.LEFT, border=10)

		self.allHTMLBtn = wx.Button(self, -1,
								    'Exportiere alle Formen in eine HTML Datei',
								    size=(220, 23))
		sizer.Add(self.allHTMLBtn, flag=wx.TOP | wx.CENTER, border=16)

		self.vonButton.Bind(wx.EVT_BUTTON, self.getThisForm)
		self.allHTMLBtn.Bind(wx.EVT_BUTTON, self.formen)

		sizer.Fit(self)
		self.SetSizer(sizer)

	def formen(self, event):
		if len(self.vonVerb.GetLabel().replace(" ","")) > 1:
			verb = self.vonVerb.GetLabel().replace(" ","")
			try:
				export.html().formen(verb =verb,
									 save="Alle-Formen-von-"+verb+".html",
									 modus=1)
				wx.MessageBox("Datei erfolgreich gespeichert!", "Info")
			except:
				error = wx.MessageDialog(None, "Es trat ein Fehler auf!", "Info", wx.ICON_ERROR)
				error.ShowModal()
		else:
			wx.MessageBox("Ein Verb muss schon eingegeben werden! :P", "Info")

	def getThisForm(self, event):
		if len(self.vonVerb.GetLabel().replace(" ","")) > 1:
			modusSelection = self.modus.GetSelection()
			temporaSelection = self.tempora.GetSelection()
			genusSelection = self.genus.GetSelection()
			personSelection = self.person.GetSelection()

			# Wenn Futur oder Aorist NICHT gewaehlt sind, aber der
			# Passiv -> setze den Tempus intern auf Medium / Passiv
			if temporaSelection not in [2, 3] and genusSelection == 2:
				genusSelection = 1
				self.genus.SetSelection(1)

			#Wenn der Konjunktiv gewaehlt ist, breche bei Impf, Futur, Plusqam,
			# Futur des Perfekt ab
			if modusSelection == 1 and temporaSelection in [1, 2, 5, 6]:
				wx.MessageBox("Den "+q.solve_tempora[temporaSelection]+\
							  " gibt es im Konjunktiv nicht!", "Info")
				return

			# Wenn der Optativ Aktiv  gewaehlt ist, breche bei Impf, Plusqam,
			# Futur des Perfekt ab
			if modusSelection == 2 and genusSelection == 0 and temporaSelection in [1, 5, 6] and  genusSelection == 0:
				wx.MessageBox("Den "+q.solve_tempora[temporaSelection]+\
							  " gibt es im Optativ Aktiv nicht!", "Info")
				return

			# Wenn der Optativ Medium / Passiv  gewaehlt ist, breche bei Impf, Plusqam ab
			if modusSelection == 2 and genusSelection == 1 and temporaSelection in [1, 5] and  genusSelection in [1, 2]:
				wx.MessageBox("Den "+q.solve_tempora[temporaSelection]+\
							  " gibt es im Optativ " +  q.solve_genus[genusSelection] +\
							  " nicht!", "Info")
				return

			# Wenn der Imperativ Aktiv gewaehlt ist, breche bei Impf,
			# Futur, Perfekt, Plusqam, Futur des Pefeky ab
			if modusSelection == 3 and temporaSelection in [1,2,4,5,6] and genusSelection ==0:
				wx.MessageBox("Den "+q.solve_tempora[temporaSelection]+\
							  " gibt es im Imperfekt Aktiv nicht!", "Info")
				return

			# Wenn der Imperativ Medium / Passiv  gewaehlt ist, breche bei Impf,
			# Futur, Plusqam, Futur des Pefeky ab
			if modusSelection == 3 and temporaSelection in [1,2,5,6]and genusSelection in [1,2]:
				wx.MessageBox("Den "+q.solve_tempora[temporaSelection]+\
							  " gibt es im Imperfekt "+ q.solve_genus[genusSelection] +\
							  " nicht!", "Info")
				return

			# Wenn der Imperativ gewaehlt ist, verweigere die Arbeit beu
			# personSelection in [0, 3]
			if modusSelection == 3 and personSelection in [0, 3]:
				wx.MessageBox("Im Imperativ gibt es die 1. Person Singular / Plural nicht!",
							  "Info")
				return

			form = newForm.VerbForm().generateForm(fontflag = self.fontmodus,
												   modus = modusSelection,
												   tempora = temporaSelection,
												   genus = genusSelection,
												   person = personSelection,
												   verb = self.vonVerb.GetLabel().replace(" ","")
												   )
			self.vonVerb.SetLabel(form[1])

			self.output.SetLabel('')
			temp = ""
			for i in range(len(form[0])):
					temp += q.solve_modus[form[0][i][0]] + ' ' +\
										   q.solve_tempora[form[0][i][1]] + ' '+\
										   q.solve_person[form[0][i][3]] + ' '+\
										   q.solve_genus[form[0][i][2]] + "\n"

			self.output.SetLabel(temp)
		else:
			wx.MessageBox("Ein Verb muss schon eingegeben werden! :P", "Info")

	def AddRadios(self):
		# RadioButtons zum Bestimmen
		determine_sizer = wx.GridBagSizer(0,6)
		self.modus = wx.RadioBox(self, -1, ' Modus ',size=(-1, 158),
														 choices=q.solve_modus,
														 majorDimension=len(q.solve_modus),
														 style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER)
		self.tempora = wx.RadioBox(self, -1, ' Tempora ',size=(-1, 158),
															 choices=q.solve_tempora,
															 majorDimension=len(q.solve_tempora),
															 style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER)
		self.person = wx.RadioBox(self, -1, ' Person ', size=(-1, 158),
															choices = q.solve_person,
															majorDimension=len(q.solve_person),
															style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER)
		self.genus = wx.RadioBox(self, -1, ' Genus ',size=(-1, 158),
														 choices = q.solve_genus,
														 majorDimension=len(q.solve_genus),
														 style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER |
														 wx.EXPAND)

		determine_sizer.Add(self.modus, (0, 0))
		determine_sizer.Add(self.tempora, (0, 1))
		determine_sizer.Add(self.person, (0, 2))
		determine_sizer.Add(self.genus, (0, 3))

		return determine_sizer

class BuildVerb(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent, -1)
		self.parent = parent
		self.fontmodus = 0

		self.values, self.form, self.verb = newForm.VerbForm().generateForm(self.fontmodus)
		self.form = self.form.split(' ')[0]
		self.input = None

		sizer = wx.BoxSizer(wx.VERTICAL)

		# Vorgabe
		self.target = wx.StaticText(self, -1,
									label=q.solve_modus[self.values[0][0]]+ ' ' +\
									q.solve_tempora[self.values[0][1]]+ ' '+\
									q.solve_person[self.values[0][3]]+ ' '+\
									q.solve_genus[self.values[0][2]]+' von '+
									self.verb)
		self.target.SetFont(wx.Font(10,  wx.NORMAL, wx.NORMAL, wx.NORMAL,
												False))
		sizer.Add(self.target, 0, wx.TOP|wx.LEFT|wx.ALIGN_LEFT, 11)

		box_target = wx.BoxSizer(wx.HORIZONTAL)

		self.newform = wx.Button(self, -1, 'Neu')
		self.newform.Bind(wx.EVT_BUTTON, self.OnNew)
		box_target.Add(self.newform, 0, wx.LEFT | wx.TOP, 11 )

		self.solve = wx.Button(self, -1, 'Aufloesen')
		self.solve.Bind(wx.EVT_BUTTON, self.OnSolve)
		box_target.Add(self.solve, 0, wx.LEFT | wx.TOP, 11)

		sizer.Add(box_target,  flag=wx.EXPAND)

		# Eingabe
		box_input = wx.StaticBox(self, -1)
		sizer_input = wx.StaticBoxSizer(box_input, wx.HORIZONTAL)
		inputGrid = wx.GridBagSizer(5, 5)
		self.input = wx.TextCtrl(self, -1, size=(300, 28))
		#self.input.SetFont(LearnGUI().page1.symbolFont)
		self.check = wx.Button(self, -1, 'Pruefen')
		self.check.Bind(wx.EVT_BUTTON, self.OnCheck)
		inputGrid.Add(self.input, (0, 0), flag=wx.TOP, border=2)
		inputGrid.Add(self.check, (0, 1), flag=wx.TOP | wx.ALIGN_LEFT,
									 border=4)
		sizer_input.Add(inputGrid)
		sizer.Add(sizer_input, 0, wx.ALIGN_LEFT| wx.EXPAND |wx.LEFT | wx.BOTTOM
							| wx.RIGHT, 9)

		# Ergebnis
		self.result = wx.StaticText(self, -1, '')
		font = wx.Font(11, wx.NORMAL, wx.NORMAL, wx.FONTWEIGHT_BOLD, False)
		self.result.SetFont(font)

		sizer.Add(self.result, 0, wx.EXPAND | wx.CENTER | wx.LEFT, 175)

		sizer.Fit(self)
		self.SetSizer(sizer)

	def OnNew(self, event):
		a = newForm.VerbForm()
		form = a.generateForm(self.fontmodus)
		self.values = form[0]
		self.target.SetLabel(q.solve_modus[self.values[0][0]]   + ' ' +\
							 q.solve_tempora[self.values[0][1]] + ' ' +\
							 q.solve_person[self.values[0][3]]  + ' ' +\
							 q.solve_genus[self.values[0][2]]   + ' von '+
							 form[2])
		self.form = form[1].split(' ')[0]
		self.input.SetLabel('')
		self.result.SetLabel('')

	def OnCheck(self, event):
		if self.input.GetLabel() ==  self.form:
			self.result.SetLabel('Richtig!')
		else:
			self.result.SetLabel('Falsch!')

	def OnSolve(self, event):
		self.input.SetLabel(self.form)

class DetermineVerb(wx.Panel):
		def __init__(self, parent):
				wx.Panel.__init__(self, parent, -1)
				self.parent = parent
				self.fontmodus = 0

				self.values, self.form, self.verb= newForm.VerbForm().generateForm(self.fontmodus)
				self.input = None

				sizer = wx.BoxSizer(wx.VERTICAL)

				self.symbolFont = wx.Font(13,  wx.NORMAL, wx.NORMAL, wx.NORMAL, False, 'Symbol')
				self.griechFont = wx.Font(16,  wx.NORMAL, wx.NORMAL, wx.NORMAL, False, 'Griech2')

				# Ausgabe
				box_output = wx.StaticBox(self, -1)
				sizer_output = wx.StaticBoxSizer(box_output, wx.HORIZONTAL)

				outputGrid = wx.GridBagSizer(5, 5)

				self.output = wx.TextCtrl(self, -1, size=(250, 28),style=wx.TE_READONLY)
				self.output.SetFont(self.symbolFont)

				self.output.SetLabel(self.form)

				self.generateNew = wx.Button(self, -1, 'Neue Form generieren')
				self.generateNew.Bind(wx.EVT_BUTTON, self.OnNew)

				outputGrid.Add(self.output, (0, 0), flag=wx.TOP, border=2)
				outputGrid.Add(self.generateNew, (0, 1), flag=wx.TOP | wx.ALIGN_LEFT,
											 border=4)

				sizer_output.Add(outputGrid, flag=wx.EXPAND)

				sizer.Add(sizer_output, 0, wx.ALIGN_LEFT| wx.EXPAND |wx.LEFT
									| wx.RIGHT, 9)

				# RadioButtons zum Bestimmen hinzugfuegen
				radios = self.AddRadios()
				sizer.Add(radios, flag=wx.CENTER | wx.TOP, border=10)

				# EvaluateBox
				box_eval = wx.StaticBox(self, -1)
				sizer_eval = wx.StaticBoxSizer(box_eval, wx.HORIZONTAL)

				panel_eval = wx.Panel(self, -1)



				self.evaluate = wx.Button(panel_eval, -1, 'Auswerten', (0, 3))
				self.evaluate.Bind(wx.EVT_BUTTON, self.OnEval)

				self.solve = wx.Button(panel_eval, -1, 'Aufloesen', (0, 30))
				self.solve.Bind(wx.EVT_BUTTON, self.OnSolve)

				self.solution = wx.StaticText(panel_eval, -1, '', pos=(100, 8),
																			size=(280, 20))

				sizer_eval.Add(panel_eval)

				sizer.Add(sizer_eval, flag=wx.CENTER | wx.EXPAND |wx.ALL, border=9)

				sizer.Fit(self)
				self.SetSizer(sizer)

		def AddRadios(self):
			# RadioButtons zum Bestimmen
			determine_sizer = wx.GridBagSizer(0,6)
			self.modus = wx.RadioBox(self, -1, ' Modus ',size=(-1, 158),
															 choices=q.solve_modus,
															 majorDimension=len(q.solve_modus),
															 style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER)
			self.tempora = wx.RadioBox(self, -1, ' Tempora ',size=(-1, 158),
																 choices=q.solve_tempora,
																 majorDimension=len(q.solve_tempora),
																 style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER)
			self.person = wx.RadioBox(self, -1, ' Person ', size=(-1, 158),
																choices = q.solve_person,
																majorDimension=len(q.solve_person),
																style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER)
			self.genus = wx.RadioBox(self, -1, ' Genus ',size=(-1, 158),
															 choices = q.solve_genus,
															 majorDimension=len(q.solve_genus),
															 style=wx.RA_SPECIFY_ROWS | wx.NO_BORDER |
															 wx.EXPAND)

			determine_sizer.Add(self.modus, (0, 0))
			determine_sizer.Add(self.tempora, (0, 1))
			determine_sizer.Add(self.person, (0, 2))
			determine_sizer.Add(self.genus, (0, 3))

			return determine_sizer

		def OnNew(self, event):
				a = newForm.VerbForm()
				form = a.generateForm(self.fontmodus)
				self.output.SetLabel(form[1])
				self.values = form[0]
				self.solution.SetLabel('')

		def OnEval(self, event):
				self.input = [self.modus.GetSelection(), self.tempora.GetSelection(),
											 self.genus.GetSelection(), self.person.GetSelection()]
				if self.input in self.values:
						self.solution.SetLabel('Richtig!!')
				else:
						self.solution.SetLabel('Falsch!')

#===============================================================================
#		def OnSolve(self, event):
#				self.solution.SetLabel(q.solve_modus[self.values[0][0]]+ ' ' +\
#															 q.solve_tempora[self.values[0][1]]+ ' '+\
#															 q.solve_person[self.values[0][3]]+ ' '+\
#															 q.solve_genus[self.values[0][2]])
#				self.solution.SetFont(wx.Font(9,  wx.NORMAL, wx.NORMAL, wx.NORMAL,
#															False))
#===============================================================================

		def OnSolve(self, event):
			self.solution.SetLabel('')

			temp = ""

			for i in range(len(self.values)):
				temp += q.solve_modus[self.values[i][0]] + ' ' +\
									   q.solve_tempora[self.values[i][1]] + ' '+\
									   q.solve_person[self.values[i][3]] + ' '+\
									   q.solve_genus[self.values[i][2]] + "\n"

			self.solution.SetLabel(temp)

			self.solution.SetFont(wx.Font(9,  wx.NORMAL, wx.NORMAL, wx.NORMAL,
														False))






class LearnGUI(wx.Frame):
	def __init__(self, parent=None, id=-1, title='NoName'):
		wx.Frame.__init__(
						self, parent, id, title, size=(430, 375),
						style=wx.MINIMIZE_BOX | wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU
		)

		self.fontmodus = 0

		# Menubar
		self.addMenuBar()

		# Content
		panel = wx.Panel(self)
		self.notebook = wx.Notebook(panel, -1, style=wx.NB_TOP)

		self.page1 = DetermineVerb(self.notebook)
		self.page2 = BuildVerb(self.notebook)
		self.page3 = Tools(self.notebook)

		self.notebook.AddPage(self.page1, 'Verb bestimmen')
		self.notebook.AddPage(self.page2, 'Verb bilden')
		self.notebook.AddPage(self.page3, 'Tools')

		sizer = wx.BoxSizer()
		sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 3)
		panel.SetSizer(sizer)

		# StatusBar
		self.statusbar = self.CreateStatusBar()
		self.statusbar.Hide()

## eventhandler -----------------------------------------------------------------
		self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.OnVersion, id=ID_VERSION)
		self.Bind(wx.EVT_MENU, self.ToggleStatusBar, id=ID_STAT)
		self.Bind(wx.EVT_MENU, self.ToggleModus, id=ID_DTERMINE)
		self.Bind(wx.EVT_MENU, self.ToggleModus, id=ID_BUILD)
		self.Bind(wx.EVT_MENU, self.ToggleFont, id=self.symbolItem.GetId())
		self.Bind(wx.EVT_MENU, self.ToggleFont, id=self.griechItem.GetId())
		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		self.Bind(wx.EVT_MENU, self.changeVerbDialog, id=self.verb.GetId())

		self.Bind(wx.EVT_MENU, self.exportEndungenDialog, id=self.exportEndungen.GetId())

		self.Centre()
		self.Show(True)

		self.ToggleFont(None)

	def addMenuBar(self):
		"""
Fuegt die Menueleiste hinzu.
		"""
## DATEI ======================================================================
		datei = wx.Menu()

		self.determineform = datei.Append(ID_DTERMINE, 'Verben bestimmen',
										  'Blendet den Dialog zum Bestimmen von Verben ein',
										  kind=wx.ITEM_RADIO)
		self.buildform = datei.Append(ID_BUILD, 'Verben bilden',
									  'Blendet den Dialog zum Bilden ovn Verben ein',
									  kind=wx.ITEM_RADIO)

## export ----------------------------------------------------------------------
		export = wx.Menu()
		self.exportEndungen = export.Append(wx.ID_ANY, 'Endungen', 'Exportiert alle Endungen in eine HTML Datei')

		datei.AppendSeparator()

		datei.AppendMenu(wx.ID_ANY, '&Exportieren', export)

## quit ------------------------------------------------------------------------
		datei.AppendSeparator()
		datei.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', 'Programm beenden')

## PREFERENCES =================================================================
		preferences = wx.Menu()
		self.verb = preferences.Append(wx.ID_ANY, "&Verben", "Verben hinzufuegen / entfernen")

## font ------------------------------------------------------------------------
		font = wx.Menu()
		self.symbolItem = font.Append(wx.ID_ANY, 'S&ymbol',
									  'Es werden keine Akzente dargestellt',
									  kind=wx.ITEM_RADIO)
		self.griechItem = font.Append(wx.ID_ANY, '&Griech2',
									  'Akzente werden dargestellt',
									  kind=wx.ITEM_RADIO)
		preferences.AppendMenu(wx.ID_ANY, 'Schri&ftart', font)

#===============================================================================
# ## difficulty -----------------------------------------------------------------
#		difficulty = wx.Menu()
#
#		self.easy = difficulty.Append(wx.ID_ANY, 'Einfach',
#									  'Es wird nur im Indikativ abgefragt',
#									  kind=wx.ITEM_RADIO)
#		self.medium = difficulty.Append(wx.ID_ANY, 'Mittel',
#									  'Es werden auch seltenere Formen abgefragt',
#									  kind=wx.ITEM_RADIO)
#		self.hard = difficulty.Append(wx.ID_ANY, 'Schwer',
#									  'Es wird alles abgefragt',
#									  kind=wx.ITEM_RADIO)
#		difficulty.AppendSeparator()
#
#		self.difficultyInfo = difficulty.Append(wx.ID_ANY, 'Info',
#									  'Detaillierte Beschreibung der momentanen Einstellung')
#		preferences.AppendMenu(wx.ID_ANY, 'Sch&wirigkeit', difficulty)
#===============================================================================


		preferences.AppendSeparator()

		self.shst = preferences.Append(ID_STAT, '&Statuleiste',
									   'Blende die Statusleiste ein/aus',
									   kind=wx.ITEM_CHECK)

## HILFE ======================================================================
		hilfe = wx.Menu()
		hilfe.Append(ID_VERSION, 'About', 'Versions Hinweise')

		# Die Menueleiste zusammenstellen
		menubar = wx.MenuBar()
		menubar.Append(datei, '&Datei')
		menubar.Append(preferences, '&Einstellungen')
		menubar.Append(hilfe, '&Hilfe')

		preferences.Check(ID_STAT, False)

		self.SetMenuBar(menubar)

	def changeVerbDialog(self, event):
		"""
Ermoeglicht das Hinzufuegen / Entfernen von Verben.
		"""
		list = ListBox(self, -1, 'Test')
		verbs = xmlparser.ParseXMLResource().getVerbalstock(q.VERBALSTOCK_FILE)
		for i in verbs:
			list.listbox.Append(i)

	def ToggleFont(self, event):
		"""
Aendert die Schriftart von Symbol auf griech.
		"""
		if self.symbolItem.IsChecked():
			self.page1.output.SetFont(self.page1.symbolFont)
			self.page2.input.SetFont(self.page1.symbolFont)
			self.page3.vonVerb.SetFont(self.page1.symbolFont)
			self.page1.fontmodus = 0
			self.page2.fontmodus = 0
			self.page3.fontmodus = 0
		elif self.griechItem.IsChecked():
			self.page1.output.SetFont(self.page1.griechFont)
			self.page2.input.SetFont(self.page1.griechFont)
			self.page3.vonVerb.SetFont(self.page1.griechFont)
			self.page1.fontmodus = 1
			self.page2.fontmodus = 1
			self.page3.fontmodus = 1

	def ToggleModus(self, event):
		"""
Wechselt zwischen den Nootebook-Panles 'Verb bestimmen' und 'Verb bilden'.
		"""
		if self.determineform.IsChecked():
			self.notebook.ChangeSelection(0)
		elif self.buildform.IsChecked():
			self.notebook.ChangeSelection(1)

	def exportEndungenDialog(self, event):
		"""
Ruft den Dialog fuer die Einstellungen fuer das Exportieren der Endungen auf.
		"""
		try:
			export.html().endungen(modus=1,save="endungen-"+q.NAME)
			wx.MessageBox('Datei erfolgreich gespeichert!', 'Info')

		except:
			a = wx.MessageDialog(self, 'Es trat ein Fehler auf!\n\n'+sys.exc_info()[0], 'Error', wx.ICON_ERROR)
			a.ShowModal()
		#dialog = EndungenExport(self, -1, 'Exportieren')


	def ToggleStatusBar(self, event):
		if self.shst.IsChecked():
			self.statusbar.Show()
			self.SetSize((430, 395))
		else:
			self.statusbar.Hide()
			self.SetSize((430, 375))

	def OnRightDown(self, event):
		self.PopupMenu(MyPopupMenu(self), event.GetPosition())
		event.Skip()

	def OnVersion(self, event):
		info = wx.AboutDialogInfo()
		info.SetName(q.NAME+' ')
		info.SetVersion(q.VERSION)
		info.SetWebSite('www.jonathanstroebele.de/gr/')
		wx.AboutBox(info)

	def OnQuit(self, event):
		self.Close()

ID_NEW = 1
ID_RENAME = 2
ID_CLEAR = 3
ID_DELETE = 4


class ListBox(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self,
						  parent,
						  id,
						  title,
						  size=(350, 220),
						  style= wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU)

		panel = wx.Panel(self, -1)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		self.listbox = wx.ListBox(panel, -1)
		hbox.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 20)

		self.symbolFont = wx.Font(13,  wx.NORMAL, wx.NORMAL, wx.NORMAL, False, 'Symbol')

		self.listbox.SetFont(self.symbolFont)

		btnPanel = wx.Panel(panel, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		new = wx.Button(btnPanel, ID_NEW, 'Neu', size=(90, 30))
		ren = wx.Button(btnPanel, ID_RENAME, 'Umbenennen', size=(90, 30))
		dlt = wx.Button(btnPanel, ID_DELETE, 'Loeschen', size=(90, 30))
		clr = wx.Button(btnPanel, ID_CLEAR, 'Alle loeschen', size=(90, 30))

		self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
		self.Bind(wx.EVT_BUTTON, self.OnRename, id=ID_RENAME)
		self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE)
		self.Bind(wx.EVT_BUTTON, self.OnClear, id=ID_CLEAR)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)

		vbox.Add((-1, 20))
		vbox.Add(new)
		vbox.Add(ren, 0, wx.TOP, 5)
		vbox.Add(dlt, 0, wx.TOP, 5)
		vbox.Add(clr, 0, wx.TOP, 5)

		btnPanel.SetSizer(vbox)
		hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
		panel.SetSizer(hbox)

		self.Centre()
		self.Show(True)

		def NewItem(self, event):
				text = wx.GetTextFromUser('Gebe eine neue Form ein', 'Neu')
				if text != '':
						self.listbox.Append(text)

		def OnRename(self, event):
				sel = self.listbox.GetSelection()
				text = self.listbox.GetString(sel)
				renamed = wx.GetTextFromUser('Umbenennen', 'Umbenennen', text)
				if renamed != '':
						self.listbox.Delete(sel)
						self.listbox.Insert(renamed, sel)


		def OnDelete(self, event):
				sel = self.listbox.GetSelection()
				if sel != -1:
						self.listbox.Delete(sel)

		def OnClear(self, event):
				self.listbox.Clear()


#--- Main ----------------------------------------------------------------------
if __name__ == '__main__':
		app = wx.App()
		LearnGUI(None, -1, q.NAME+' - '+q.VERSION)
		app.MainLoop()
		del app
