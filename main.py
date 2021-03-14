from data_representation import Paket
from input_convert import alles_dijkstra, get_goal_nodes, get_edges_by_node
import branch_and_bound
import json
import sys

# samen suchen (input lesen)
path_to_file = sys.argv[1]
with open(path_to_file,'r') as file:
	file_content = json.loads(file.read())

	# pflanzen (vorverarbeitung)
	depot = 0
	autolast = file_content['cap']

	number_of_nodes = file_content['graph']['nodes']
	pakete_one_based = file_content['pickpool']
	edges_one_based = file_content['graph']['edges']


	edges_by_node = get_edges_by_node(number_of_nodes, edges_one_based)
	goal_nodes = get_goal_nodes(pakete_one_based,depot)

	graph = alles_dijkstra(number_of_nodes, goal_nodes, edges_by_node)
	pakete = [Paket(pakete_one_based[index][0]-1, pakete_one_based[index][1],index) for index in range(0,len(pakete_one_based))]

	# tassen, tassen
	bestes_ergebnis = branch_and_bound.do(graph, pakete, autolast, depot)

	alle_reisen = []

	for fahrt in bestes_ergebnis.fahrten():

		pakete_je_knoten = dict()
		for paket in fahrt.pakete:
			if not paket.zielknoten in pakete_je_knoten:
				pakete_je_knoten[paket.zielknoten] = []
			pakete_je_knoten[paket.zielknoten].append(paket.own_id)

		reihenfolge = branch_and_bound.tsp(fahrt.knoten()+[depot],graph)

		result = []
		for station in reihenfolge:
			result.extend(pakete_je_knoten[station])
		alle_reisen.append(result)

	# schön machen
	print(alle_reisen)