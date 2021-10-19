from mesa.model import Model
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
import numpy as np

from .model import graduateModel
from .agent import Student_Model 
from mesa.visualization.ModularVisualization import VisualizationElement

class pieChartModule(VisualizationElement):
    package_includes = ["Chart.min.js"]
    local_includes = ["pieChart.js"]

    def __init__(self, bins, canvas_height, canvas_width):
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.bins = bins
        new_element = "new pieChartModule({}, {}, {})"
        new_element = new_element.format(bins,
                                         canvas_width,
                                         canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        wealth_vals = [agent.wealth for agent in model.schedule.agents]
        pieC = np.pieChart(wealth_vals, bins=self.bins)[0]
        return [int(x) for x in pieC]

COLORS = {
    "Satisfied": "#64dd17",
    "Mildly satisfied": "#ff9800",
    "Unsatisfied": "#f44336",
    "Needs help": "#e57373",
    "Suicide": "black",
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

    if agent.satisfaction > 0 and agent.satisfaction <= 20:
        portrayal["Color"] = COLORS["Satisfied"]
    elif agent.satisfaction > 20 and agent.satisfaction <= 40:
        portrayal["Color"] = COLORS["Mildly satisfied"]
    elif agent.satisfaction > 40 and agent.satisfaction <= 60:
        portrayal["Color"] = COLORS["Needs help"]
    elif agent.satisfaction > 60 and agent.satisfaction <= 98:
        portrayal["Color"] = COLORS["Unsatisfied"]
    else:
        portrayal["Color"] = COLORS["Suicide"]
        
    return portrayal


canvas_element = CanvasGrid(graduateModelPotrayal, 100, 100, 730, 500)
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "N": UserSettableParameter('slider',"Number of Agents",20,2,1000,1),
    "height": 100,
    "width": 100,
    "initial_marks_signma" : UserSettableParameter('slider',"Initial Mark Distribution tails",20,0,30,1),
    "gender_range" : UserSettableParameter('slider',"gender ratio Male/Feamle",0.69,0,1,0.1),
    "visa_range" : UserSettableParameter('slider',"Student Type Inter/Domes",70,0,100,2),
    "mark_range" : UserSettableParameter('slider',"Mark Ratio Group/Individual",0.69,0,1,0.1),
    "interaction_intensity" : UserSettableParameter('slider',"Interacting Agents Introvert/Extrovert",50,0,100,1),
    "workload_first" : UserSettableParameter('slider',"Male and Female Workload Pressure",1,0,1,0.1),
    "worload_third_male" : UserSettableParameter('slider',"Male Workload Relief",-1,-1,0,0.1),
    "workload_third_female" : UserSettableParameter('slider',"Female Workload Relief",-0.75,-1,0,0.1),
    "eventFrequency": UserSettableParameter('slider',"Event Frequency",0,0,40,1),
    "eventBudget": UserSettableParameter('slider',"Event Budget For Each Event",0,0,100000,70),

}

pieChart = PieChartModule([{"Label": label, "Color": color} for (label, color) in COLORS.items()], 200, 500)

server = ModularServer(
    graduateModel, [canvas_element, tree_chart, pieChart],"Graduate life", model_params
)

