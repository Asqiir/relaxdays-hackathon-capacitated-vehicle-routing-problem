import functools
from data_representation import Kante

def get_edges_by_node(number_of_nodes, edges_one_based):
	edges_by_node = dict()
	for node in range(0,number_of_nodes):
		edges_by_node[node] =[]

	for edge in edges_one_based:
		edges_by_node[edge[0]-1].append((edge[1]-1,edge[2]))
		edges_by_node[edge[1]-1].append((edge[0]-1,edge[2]))

	return edges_by_node

def get_goal_nodes(pakete_one_based,depot):
	#goal_nodes = {'input_nr':goal_nr}
	goal_nodes_list = sorted(set([depot] + [paket[0]-1 for paket in pakete_one_based]))

	goal_nodes = dict()
	for index in range(0,len(goal_nodes_list)):
		goal_nodes[index] = goal_nodes_list[index]

	return goal_nodes	


def compare(item1, item2):
	if item1==-1: #item1 größer
		return 1
	elif item2==-1: #item2 größer
		return -1
	elif item1 < item2: #item2 größer
		return -1
	elif item2 < item1: #item1 größer
		return 1
	else:
		return 0


def dijkstra(start_node, goal_nodes, nr_of_nodes, edges_by_node):
	'''return [Kante,Kante,Kante,...] of shortest path from start_node to node=index'''
	#goal_nodes = {input_nr:goal_nr}

	abstand = [-1 for index in range(0,nr_of_nodes)]
	vorgaenger = [None for index in range(0,nr_of_nodes)]

	abstand[start_node] = 0

	unbesucht = [start_node] + list(range(0,start_node)) + list(range(start_node+1,nr_of_nodes)) # ist zu jedem zeitpunkt dijkstra-sortiert

	while unbesucht:
		unbesucht.sort(key=functools.cmp_to_key(lambda item1, item2: compare(abstand[item1],abstand[item2])))
		v=unbesucht.pop(0)

		for kante in edges_by_node[v]:
			if kante[0] in unbesucht:
				if abstand[kante[0]]<0 or abstand[v] + kante[1] < abstand[kante[0]]:
					abstand[kante[0]] = abstand[v] + kante[1]
					vorgaenger[kante[0]] = v

	result = []
	for input_nr in goal_nodes:
		pfad = []
		last = input_nr
		while vorgaenger[last] != None:
			pfad.append(vorgaenger[last])
			last = vorgaenger[last]

		result.append(Kante(abstand[input_nr],pfad))
	return result


def alles_dijkstra(number_of_nodes, goal_nodes, edges_by_node):
	graph = []

	for index in range(0,len(goal_nodes)):
		graph.append(dijkstra(goal_nodes[index], goal_nodes, number_of_nodes, edges_by_node))

	return graph