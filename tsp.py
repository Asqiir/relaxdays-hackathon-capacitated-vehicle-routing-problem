from python_tsp.exact import solve_tsp_dynamic_programming

def alle_kanten(graph, knoten):
	alle_kanten = []

	for index1 in range(0,len(knoten)):
		for index2 in range(index1+1,len(knoten)):
			knoten1 = knoten[index1]
			knoten2 = knoten[index2]

			alle_kanten.append(graph[knoten1][knoten2])

	return alle_kanten


def tsp_lower_bound(graph, knoten, depot):
	if len(knoten)==1:
		return 2 * graph[knoten[0]][depot].distanz

	knoten.append(depot)
	alle_kanten_kosten = [kante.distanz for kante in alle_kanten(graph, knoten)]
	return sum(sorted(alle_kanten_kosten)[:len(knoten)])



def tsp_upper_bound(graph, knoten, depot):
	knoten.append(depot)
	result = 0
	for index in range(0,len(knoten)):
		result += graph[knoten[index-1]][knoten[index]].distanz


	return result
