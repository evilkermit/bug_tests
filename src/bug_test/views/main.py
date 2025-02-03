"""Application for reproducing potential upstream bugs."""

import pyvista as pv
from pyvista import examples
from pyvista.trame.ui import plotter_ui
from trame.app import get_server
from trame.decorators import TrameApp
from trame.ui.vuetify3 import VAppLayout
from trame.widgets import html
from trame.widgets import vuetify3 as vuetify

KNEE = examples.download_knee_full()


@TrameApp()
class TestApp:
    """Class for reproducing potential upstream bugs."""

    def __init__(self) -> None:
        self.server = get_server(None, client_type="vue3")
        self.create_plotter()

        with VAppLayout(self.server) as layout:
            with layout.root:
                vuetify.VBtn("Set Colormap to coolwarm", color="green", click=self.change_colormap)
                with html.Div(classes="d-flex flex-row h-100"):
                    self.view1 = plotter_ui(self.plotter1)
                    self.view2 = plotter_ui(self.plotter2)

    def create_plotter(self) -> None:
        self.plotter1 = pv.Plotter(off_screen=True)
        self.plotter2 = pv.Plotter(off_screen=True)
        self.mesh = self.plotter1.add_mesh(KNEE, colormap="viridis", opacity="sigmoid", show_scalar_bar=False)
        self.volume = self.plotter2.add_volume(KNEE, colormap="viridis", opacity="sigmoid", show_scalar_bar=False)
        print(type(self.mesh), type(self.volume))

    def change_colormap(self) -> None:
        self.mesh.mapper.lookup_table.cmap = "coolwarm"
        self.view1.update()
        self.volume.mapper.lookup_table.cmap = "coolwarm"
        self.view2.update()
