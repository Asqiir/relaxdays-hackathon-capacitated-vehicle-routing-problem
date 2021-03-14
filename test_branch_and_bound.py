from data_representation import Kante, Paket
import branch_and_bound

graph = [

[Kante(0), Kante(4), Kante(4), Kante(9), Kante(1)],
[Kante(4), Kante(0), Kante(8), Kante(13),Kante(5)],
[Kante(4), Kante(8), Kante(0), Kante(5), Kante(5)],
[Kante(9), Kante(13),Kante(5), Kante(0), Kante(10)],
[Kante(1), Kante(5), Kante(5), Kante(10),Kante(0)]

]


pakete = [

Paket(3,3),
Paket(2,9),
Paket(2,5),
Paket(1,4),
Paket(4,5)


]

depot = 0

lastgrenze_auto = 10



ergebnis = branch_and_bound.do(graph, pakete, lastgrenze_auto, depot)
print('Ergebnis:')
print(ergebnis)
print(ergebnis.gen_upper_bound(graph,depot))