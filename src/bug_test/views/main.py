"""Application for reproducing potential upstream bugs."""

import plotly.graph_objects as go
from plotly.data import iris, wind
from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import plotly
from trame.widgets import vuetify3 as vuetify

IRIS_DATA = iris()
WIND_DATA = wind()


@TrameApp()
class TestApp:
    """Class for reproducing potential upstream bugs."""

    def __init__(self) -> None:
        self.server = get_server(None, client_type="vue3")
        self.server.state.figure = "Figure 1"

        self.create_figures()

        with VAppLayout(self.server) as layout:
            with layout.root:
                vuetify.VSelect(
                    v_model="figure",
                    items=("['Figure 1', 'Figure 2']",),
                    update_modelValue="trigger('show_figure', [figure])",
                )
                self.figure = plotly.Figure()

            @self.server.controller.trigger("show_figure")
            def _show_figure(name: str) -> None:
                self.show_figure(name)

        self.show_figure("Figure 1")

    def create_figures(self) -> None:
        self.figure_1 = go.Figure(
            go.Heatmap(x=IRIS_DATA["sepal_width"], y=IRIS_DATA["petal_width"], z=IRIS_DATA["petal_length"])
        )
        self.figure_2 = go.Figure(
            go.Heatmap(x=WIND_DATA["direction"], y=WIND_DATA["strength"], z=WIND_DATA["frequency"])
        )

    def show_figure(self, name: str) -> None:
        match name:
            case "Figure 1":
                self.figure.update(self.figure_1)
            case "Figure 2":
                self.figure.update(self.figure_2)
            case _:
                raise ValueError("Figure not found.")
