# High Workload -> decrease the satisfaction
# Move function (kinda) Student Academics in university + before university (GPA in undergrad) -> cumulative results
# Gender
# VISA Status (International OR Domestic)
# Department

# All the above things combined after 2 years to get the satisfaction. 


from mesa import Agent
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

class Student_Model(Agent):
    satisfaction_level_overall = 0
    def __init__(self, arg_marks, gender, visa, dept):
        self.satisfaction = 0
        self.currentmarks = arg_marks
        self.gender = gender
        self.visa = visa
        self.dept = dept
    
    def move():
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def step(self, workload):
        self.move()
        student_group = self.model.grid.get_cell_list_contents([self.pos])
        cummulative = 0.00
        for other_students in student_group:
            cummulative += other_students
        cummulative = cummulative/len(student_group)
        self.currentmarks = (0.7*cummulative) + (0.3*self.currentmarks)
        self.workload += workload

    def get_current_satisfaction(self):
        self.satisfaction = 0.2(self.currentmarks) + 0.4(self.workload) + 0.3(self.gender) + 0.5(self.visa) + 0.2(self.dept)
        print (self.satisfaction)

    def end_of_life(self):
        self.satisfaction_level_overall = self.satisfaction

test = Student_Model(0,0,0,0)
Student_Model.move()
Student_Model.step(5)
Student_Model.get_current_satisfaction()
