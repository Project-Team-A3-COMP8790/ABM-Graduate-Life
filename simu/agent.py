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
import random

class Student_Model(Agent):
    satisfaction_level_overall = 0
    def __init__(self, arg_marks, gender, visa, unique_id, model):
        super().__init__(unique_id, model)
        self.satisfaction = 0
        self.currentmarks = arg_marks
        self.gender = self.determine_gender(gender)
        self.visa = visa
        self.workload = 0
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        print ("Going to this position: ", new_position)
    
    def step(self):
        self.move()
        # student_group = [{"currentmarks": 6}]
        student_group = self.model.grid.get_cell_list_contents([self.pos])
        cummulative = 0.00
        for other_students in student_group:
            # print (other_students.currentmarks)
            cummulative += other_students.currentmarks
        cummulative = cummulative/len(student_group)
        self.currentmarks = (0.3*cummulative) + (0.7*self.currentmarks)
        if self.gender == 'Male':
            work_val = self.workload_update_male(self.workload)
        else:
            work_val = self.workload_update_female_and_trans(self.workload)
        self.satisfaction += work_val
        print(self.workload)
        
        if (self.currentmarks > 77.67)
            self.satisfaction += 1
        else
            self.satisfaction -= 1
        
        # self.satisfaction = 0.2*(self.currentmarks) + 0.4*(self.workload) + 0.3*(self.gender) + 0.5*(self.visa) + 0.2*(self.dept)
        # print("Workload changed to: ", self.workload)
        # print("Marks changed to: ", self.currentmarks)


    def end_of_life(self):
        self.satisfaction_level_overall = self.satisfaction

    def end_of_life(self):
        self.satisfaction_level_overall = self.satisfaction
    
    def workload_update_male(self,workload):

        if workload  == 0.84:
            return 1.5
        elif workload == 0.70:
            return 0.5
        elif workload == 0.60:
            return -1
    
    def workload_update_female_and_trans(self,workload):

        if workload  == 0.84:
            return 1.5
        elif workload == 0.70:
            return 1
        elif workload == 0.60:
            return -0.75

    def determine_gender(self,gender):
        if gender  > 50 :
            return "Male"
        elif gender < 50 :
            return "Female"
        elif gender == 50:
            return "Trans"
        

