from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import graduateModel
from .agent import Student_Model 

COLORS = {
    "Satisfied": "#64dd17",
    "Mildly satisfied": "#ff9800",
    "Unsatisfied": "#f44336",
    "Needs help": "#e57373",
    "Suicide": "#e0e0e0",
    "males": "#03a9f4",
    "femalse": "#ff80ab",
    "international": "#5d4037",
    "domestic": "#e0e0e0",
    "AVG_Marks_Domestic": "#e0e0e0",
    "AVG_Marks_internation": "#5d4037",
    "AVG_Marks_males": "#03a9f4",
    "AVG_Marks_females": "#ff80ab",
    "AVG_Marks_Interact": "#ef9a9a",
    "AVG_Marks_NoInteract": "#263238",
    "AVG marks_interaction":  "#ba68c8",
    "Avg marks no interaction": "#607d8b"
}


def graduateModelPotrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "circle", "Filled": "true", "r": 3, "Layer": 2}

    (x, y) = agent.pos
    # print(agent.satisfaction)

    if agent.satisfaction > 80:
        portrayal["Color"] = COLORS["Satisfied"]
    elif agent.satisfaction > 60:
        portrayal["Color"] = COLORS["Mildly satisfied"]
    elif agent.satisfaction > 40:
        portrayal["Color"] = COLORS["Needs help"]
    elif agent.satisfaction > 1:
        portrayal["Color"] = COLORS["Unsatisfied"]
    else:
        portrayal["Color"] = COLORS["Suicide"]
        
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
    "eventFrequency": UserSettableParameter('slider',"Event Frequency",0,0,40,1),
    "eventBudget": UserSettableParameter('slider',"Event Budget For Each Event",0,0,100000,70),

}
server = ModularServer(
    graduateModel, [canvas_element, tree_chart],"Graduate life", model_params
)