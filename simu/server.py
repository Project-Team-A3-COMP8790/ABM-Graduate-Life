from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import graduateModel
from .agent import Student_Model 

COLORS = {"Unsatisfied": "RED", "Satisfied": "BLACK"}


def graduateModelPotrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    (x, y) = agent.pos
    # print(agent.satisfaction)


    if agent.satisfaction > 10:
        portrayal["Color"] = COLORS["Satisfied"]
        portrayal["Layer"] = 2
        portrayal["r"] = 3
    else:
        portrayal["Color"] = COLORS["Unsatisfied"]
        portrayal["Layer"] = 2
        portrayal["r"] = 3
    

    return portrayal


canvas_element = CanvasGrid(graduateModelPotrayal, 100, 100, 730, 500)
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "N": UserSettableParameter('slider',"Number of Agents",20,2,1000,1),
    "height": 100,
    "width": 100,

}
server = ModularServer(
    graduateModel, [canvas_element, tree_chart],"Graduate life", model_params
)