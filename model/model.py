from database.DAO import DAO
import networkx as nx
class Model:
    def __init__(self):
        self.listAirport = DAO.getAllAirports()
        self.airportMap = {}
        for a in self.listAirport:
            self.airportMap[a.ID] = a
        self.grafo = nx.Graph()

    def creaGrafo(self, minimo):
        self.grafo.clear()
        listaNodi = DAO.getNodi(minimo, self.airportMap)
        self.grafo.add_nodes_from(listaNodi)

    def aggiungiArchi(self, minimo):
        connessioni = DAO.getEdges(minimo, self.airportMap)
        for c in connessioni:
            v0 = c.v0
            v1 = c.v1
            peso = c.qta
            if self.grafo.has_edge(v0, v1):
                self.grafo[v0][v1]["weight"] += peso
            else:
                self.grafo.add_edge(v0, v1, weight=peso)

    def trovaConnessi(self, AereoportoP):
        vicini = self.grafo.neighbors(AereoportoP)
        listaArchi = []
        for v in vicini:
            peso = self.grafo[AereoportoP][v]["weight"]
            coppia = (v, peso)
            listaArchi.append(coppia)
        listaArchiOrd = sorted(listaArchi, key = lambda tup: tup[1], reverse=True)
        return listaArchiOrd

    def trovaItinerario(self,max, part, arr):
        vicini = self.grafo.neighbors(part)
        self.ricorsione(parziale,v0)

    def ricorsione(self,parziale, v0):
        pass

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)

    def getNodes(self):
        return self.grafo.nodes()