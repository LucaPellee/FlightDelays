import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.AereoportoP = None
        self.AereoportoA = None

    def handle_analizza(self, e):
        if self._view.txt_min is None:
            self._view.create_alert("Inserire valore minimo")
            return
        else:
            minimo = int(self._view.txt_min.value)
            self._model.creaGrafo(minimo)
            nNodes = self._model.getNumNodes()
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {nNodes}"))
            self._model.aggiungiArchi(minimo)
            nEdges = self._model.getNumEdges()
            self._view.txt_result.controls.append(ft.Text(f"Numero archi: {nEdges}"))
            self.fillPart()
            self._view.btnConnessi.disabled = False
            self._view.update_page()

    def fillPart(self):
        nodi = self._model.getNodes()
        for n in nodi:
            self._view.ddAereoportoPart.options.append(ft.dropdown.Option(data = n, on_click=self.readDD, text = n.AIRPORT))
            self._view.ddAereoportoArr.options.append(ft.dropdown.Option(data=n, on_click=self.readDDArr, text=n.AIRPORT))
        self._view.update_page()

    def readDD(self, e):
        if e.control.data is None:
            self._view.create_alert("Inserire valore")
        else:
            self.AereoportoP = e.control.data

    def readDDArr(self, e):
        if e.control.data is None:
            self._view.create_alert("Inserire valore")
        else:
            self.AereoportoA = e.control.data

    def handle_connessi(self, e):
        listaConnessi = self._model.trovaConnessi(self.AereoportoP)
        self._view.txt_result.controls.append(ft.Text("Aereoporti connessi:"))
        for a in listaConnessi:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]}, numero voli: {a[1]}"))
        self._view.update_page()

    def handleItinerario(self, e):
        max = self._view.txtTratte.value
        self._model.trovaItinerario(self, max, self.AereoportoP, self.AereoportoA)
