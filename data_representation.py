from tsp import tsp_lower_bound, tsp_upper_bound

class Kante:
	distanz = None
	pfad = []

	def __init__(self, distanz, pfad):
		self.distanz = distanz
		self.pfad = pfad

	def __repr__(self):
		return str(self.distanz)

class Paket:
	zielknoten = None
	gewicht = None
	own_id=None

	'''immutable'''
	def __init__(self, zielknoten_index, gewicht,own_id):
		self.zielknoten = zielknoten_index
		self.gewicht = gewicht
		self.own_id=own_id

	def __repr__(self):
		return str((self.zielknoten, self.gewicht))

class Fahrt:
	platz_frei = None
	pakete = None

	'''immutable'''
	def __init__(self, paketliste, lastgrenze_auto):
		self.platz_frei = lastgrenze_auto - sum([paket.gewicht for paket in paketliste])
		self.pakete = paketliste
		
	def knoten(self):
		return list(set([paket.zielknoten for paket in self.pakete]))

	def __repr__(self):
		return str(self.pakete)

#Graph ist immer:
# Knoten x Knoten-Matrix, wobei ein Eintrag ein Kanten-Objekt ist
#
#



class Tasse:
	#jede fahrt ist menge von paketen + freies gewicht
	__volle_fahrten = []
	__offene_fahrten = []

	anzahl_abgearbeiteter_pakete = None
	__upper_bound = None
	lower_bound=None

	def __init__(self, volle_fahrten, offene_fahrten, anzahl_abgearbeiteter_pakete, graph, pakete, lastgrenze_auto,depot):
		self.__volle_fahrten = volle_fahrten
		self.__offene_fahrten = offene_fahrten
		self.anzahl_abgearbeiteter_pakete = anzahl_abgearbeiteter_pakete
		self.lower_bound = self.__gen_lower_bound(graph,pakete,depot,lastgrenze_auto)

	def fahrten(self):
		return self.__volle_fahrten + self.__offene_fahrten

	def __gen_lower_bound(self, graph,pakete,depot,lastgrenze_auto):
		result=0

		for fahrt in self.__volle_fahrten:
			result += tsp_lower_bound(graph,fahrt.knoten(),depot)

		for fahrt in self.__offene_fahrten:
			result += tsp_lower_bound(graph,fahrt.knoten(),depot)

		# GEHT DAS BESSER?

		#übervolle angefangene fahrten
		skip_counter = 0
		tmp = [of.platz_frei for of in self.__offene_fahrten]
		while tmp:
			while tmp[0]>0 and len(pakete)>self.anzahl_abgearbeiteter_pakete+skip_counter:
				tmp[0] -= pakete[self.anzahl_abgearbeiteter_pakete+skip_counter].gewicht
				skip_counter += 1
			tmp.pop(0)

		#mehr übervolle autos
		aktuell_frei = 0
		while len(pakete)>self.anzahl_abgearbeiteter_pakete+skip_counter:
			if aktuell_frei<=0:
				result += 2* graph[pakete[self.anzahl_abgearbeiteter_pakete+skip_counter].zielknoten][depot].distanz
				aktuell_frei = lastgrenze_auto
			aktuell_frei -= pakete[self.anzahl_abgearbeiteter_pakete+skip_counter].gewicht
			skip_counter += 1

		return result

	def gen_upper_bound(self, graph, depot): 
		'''erst aufrufen, wenn Tasse ein Blatt ist'''
		if self.__upper_bound==None:
			self.__upper_bound = 0


			for fahrt in self.__volle_fahrten:
				self.__upper_bound += tsp_upper_bound(graph,fahrt.knoten(),depot)

			for fahrt in self.__offene_fahrten:
				self.__upper_bound += tsp_upper_bound(graph,fahrt.knoten(),depot)

		return self.__upper_bound

	def teiltassen_generieren(self, graph, pakete, lastgrenze_auto, depot):
		result = []

		paket = pakete[self.anzahl_abgearbeiteter_pakete]

		neue_fahrt_fuer_neues_paket = Tasse(self.__volle_fahrten, self.__offene_fahrten + [Fahrt([paket], lastgrenze_auto)], self.anzahl_abgearbeiteter_pakete+1, graph, pakete, lastgrenze_auto, depot)
		result.append(neue_fahrt_fuer_neues_paket)

		for fahrt in self.__offene_fahrten:
			if fahrt.platz_frei>=paket.gewicht:
				fahrt_bearbeitet = Fahrt(fahrt.pakete + [paket], lastgrenze_auto)
				
				if fahrt_bearbeitet.platz_frei==0:
					offene_fahrten_neu = [of for of in self.__offene_fahrten if of!=fahrt]
					volle_fahrten_neu = self.__volle_fahrten + [fahrt_bearbeitet]
				else:
					offene_fahrten_neu = [of for of in self.__offene_fahrten if of!=fahrt] + [fahrt_bearbeitet]
					volle_fahrten_neu = self.__volle_fahrten

				result.append(Tasse(volle_fahrten_neu, offene_fahrten_neu, self.anzahl_abgearbeiteter_pakete+1, graph, pakete, lastgrenze_auto, depot))

		return sorted(result, key=lambda k:-k.lower_bound)

	def __repr__(self):
		return '{Lower Bound: ' + str(self.lower_bound) + '\nFahrten: ' + str(self.__volle_fahrten + self.__offene_fahrten) + '}'