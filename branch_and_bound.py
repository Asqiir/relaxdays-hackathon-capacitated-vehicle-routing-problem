from data_representation import Tasse, Paket
from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np

def do(graph, pakete, lastgrenze_auto, depot):
	'''
	* pakete ist absteigend sortiert nach entfernung des zielknotens zum depot
	* graph als array knoten x knoten -> verbindung ist kante = Objekt, das Kosten und Kante im originalgraph kennt -> an der Hauptdiagonale gespiegelt (da ungerichtet) -> Referenz auf selbes Objekt!
	'''
	UPPER_BOUND = -1 #-1 means infinity
	regal_bester_platz = None #beste lösung bisher

	tassen = [Tasse([],[],0,graph,pakete,lastgrenze_auto,depot)]

	while tassen: #solange noch entscheidungen zu treffen
		print('Tasse:')
		print(tassen)
		print(regal_bester_platz)
		print(UPPER_BOUND)
		print()

		aktuelle_tasse = tassen.pop(-1)

		if UPPER_BOUND>-1 and aktuelle_tasse.lower_bound >= UPPER_BOUND:
			continue

		if aktuelle_tasse.anzahl_abgearbeiteter_pakete==len(pakete): #ist blatt im entscheidungsbaum
			#calculate more detailed?
			if UPPER_BOUND < 0 or aktuelle_tasse.gen_upper_bound(graph,depot) <= UPPER_BOUND:
				regal_bester_platz = aktuelle_tasse
#				print('bestes gefunden')
				UPPER_BOUND = aktuelle_tasse.gen_upper_bound(graph,depot)

			continue

		teiltassen = aktuelle_tasse.teiltassen_generieren(graph, pakete, lastgrenze_auto, depot) #absteigend sortiert nach untere_schranke
		tassen.extend(teiltassen)

	return regal_bester_platz #beste tasse



def tsp(knoten, graph):
	small_graph = np.array([ [ graph[knoten[index]][knoten[j]].distanz for j in range(0,len(knoten)) ] for index in range(0,len(knoten)) ])

	permutation, distance = solve_tsp_dynamic_programming(small_graph)
	return [knoten[p] for p in permutation if knoten[p]]



