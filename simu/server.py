from mesa.model import Model
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule, BarChartModule, TextElement
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
import numpy as np

from .model import graduateModel
from .agent import Student_Model 
from mesa.visualization.ModularVisualization import VisualizationElement

graduateModel_Initial = graduateModel
class AttributeElementSimpleText(TextElement):
    def __init__(self, attr_name):
        '''
        Create a new text attribute element.

        Args:
            attr_name: The name of the attribute to extract from the model.

        Example return: "happy: 10"
        '''
        self.attr_name = attr_name

    def render(self, model):
        return str(self.attr_name)


class AttributeElement(TextElement):
    def __init__(self, attr_name):
        '''
        Create a new text attribute element.

        Args:
            attr_name: The name of the attribute to extract from the model.

        Example return: "happy: 10"
        '''
        self.attr_name = attr_name

    def render(self, model):
        val = getattr(model, str(self.attr_name))
        return self.attr_name + ": " + str(val)

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

COLORS_SATISFICATION = {
    "Satisfied": "#64dd17",
    "Mildly satisfied": "#ff9800",
    "Unsatisfied": "#e57373",
    "Needs help": "#f44336",
    "Suicide": "black",
}
COLORS_GENDER = {
    "males": "#03a9f4",
    "females": "#ff80ab",
}
COLORS_VISA = {
    "international": "#5d4037",
    "domestic": "#009688",
}
COLORS_AVG_MARKS = {
    "AVG_Marks_Domestic": "#009688",
    "AVG_Marks_internation": "#5d4037",
    "AVG_Marks_males": "#03a9f4",
    "AVG_Marks_females": "#ff80ab",
    "AVG marks_interaction":  "#ba68c8",
    "Avg marks no interaction": "#607d8b"
}

ShapeIcon = "student_icon_"
def graduateModelPotrayal(agent):
    if agent is None:
        return
    portrayal = {"Filled": "true", "scale": 5, "Layer": 2}

    (x, y) = agent.pos
    # print(agent.satisfaction)

    if agent.satisfaction <= 20:
        portrayal["Color"] = COLORS_SATISFICATION["Satisfied"]
        portrayal["Shape"] = ShapeIcon + "Satisfied.png"
    elif agent.satisfaction > 20 and agent.satisfaction <= 40:
        portrayal["Color"] = COLORS_SATISFICATION["Mildly satisfied"]
        portrayal["Shape"] = ShapeIcon + "Mildly satisfied.png"
    elif agent.satisfaction > 40 and agent.satisfaction <= 80:
        portrayal["Color"] = COLORS_SATISFICATION["Unsatisfied"]
        portrayal["Shape"] = ShapeIcon + "Unsatisfied.png"
    elif agent.satisfaction > 80 and agent.satisfaction <= 99:
        portrayal["Color"] = COLORS_SATISFICATION["Needs help"]
        portrayal["Shape"] = ShapeIcon + "Needs help.png"
    else:
        portrayal["Color"] = COLORS_SATISFICATION["Suicide"]
        portrayal["Shape"] = ShapeIcon + "Suicide.png"
        
    return portrayal


canvas_element = CanvasGrid(graduateModelPotrayal, 100, 100, 730, 500)
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS_SATISFICATION.items()]
)

model_params = {
    "N": UserSettableParameter('slider',"Number of Agents",20,2,3000,1),
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

pieChart_Visa = PieChartModule([{"Label": label, "Color": color} for (label, color) in COLORS_VISA.items()], 200, 250)
pieChart_Gender = PieChartModule([{"Label": label, "Color": color} for (label, color) in COLORS_GENDER.items()], 200, 250)
barChart_Satisfaction = BarChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS_SATISFICATION.items()]
)
barChart_Marks = BarChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS_AVG_MARKS.items()]
)
TextElement_Event = AttributeElement("eventCount")

studentCountVSStep = AttributeElementSimpleText("Student Count VS Step")
InternationVSDomesticStudentCount = AttributeElementSimpleText("International VS Domestic Student Count")
MaleVSFemaleStudentCount = AttributeElementSimpleText("Male VS Female Student Count")
studentCountVSSatisfactionGroup = AttributeElementSimpleText("Student Count VS Satisfaction Group")
studentCountVSAvgMarksGroup = AttributeElementSimpleText("Student Count VS Avg Marks Group")


server = ModularServer(
    graduateModel_Initial, [
        TextElement_Event, canvas_element, tree_chart, studentCountVSStep, 
        barChart_Satisfaction, studentCountVSSatisfactionGroup, 
        barChart_Marks, studentCountVSAvgMarksGroup,
        pieChart_Visa, InternationVSDomesticStudentCount, pieChart_Gender, MaleVSFemaleStudentCount,
    ],"Graduate life", model_params
)

