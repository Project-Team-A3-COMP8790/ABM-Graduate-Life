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
    largest = 100
    smallest = 0
    visa = random.randint(smallest, largest - 1)    
    def __init__(self, arg_marks, gender, gender_range, visa, visa_range,workload_first,mark_range,interaction_intensity,workload_second,worload_third_male,workload_third_female, unique_id, model):
        super().__init__(unique_id, model)
        self.satisfaction = random.randint(0, 100 - 40)
        self.currentmarks = arg_marks
        self.gender = self.determine_gender(gender, gender_range)
        self.visa = visa
        self.workload = 0.60
        self.workload_first = workload_first
        self.workload_second = workload_second
        self.workload_third_male = worload_third_male
        self.workload_third_female = workload_third_female
        self.visa_status = self.get_visa_status(self.visa,visa_range)
        self.mark_range = mark_range
        self.interaction_value = random.randint(0, 100 - 1)
        self.interaction_intensity =  interaction_intensity
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        # print ("Going to this position: ", new_position)
    
    def step(self):

        if self.satisfaction <= 99:
            
            if self.interaction_value < self.interaction_intensity:
                self.move()
            # student_group = [{"currentmarks": 6}]
                student_group = self.model.grid.get_cell_list_contents([self.pos])
                cummulative = 0.00
                for other_students in student_group:
                # print (other_students.currentmarks)
                    cummulative += other_students.currentmarks
                    cummulative = cummulative/len(student_group)
                self.currentmarks = (self.mark_range*cummulative) + ((1-self.mark_range)*self.currentmarks)
            else:
                if random.randint(0, 100 - 1) > 50:
                    self.currentmarks = self.currentmarks - random.uniform(0, 1)
                else:
                    self.currentmarks = self.currentmarks - random.uniform(0, 1)

            if self.gender == 'Male':
                work_val = self.workload_update_male(self.workload,self.workload_first,self.workload_second,self.workload_third_male)
            else:
                work_val = self.workload_update_female_and_trans(self.workload,self.workload_first,self.workload_second,self.workload_third_female)
            self.satisfaction += work_val
            
            if self.visa == "international":
                self.satisfaction += 0.65
            else:
                self.satisfaction += -0.35

            
            if self.currentmarks >= 77.67:
                self.satisfaction += 1
            else:
                self.satisfaction -= 1
        
        # self.satisfaction = 0.2*(self.currentmarks) + 0.4*(self.workload) + 0.3*(self.gender) + 0.5*(self.visa) + 0.2*(self.dept)
        # print("Workload changed to: ", self.workload)
        # print("Marks changed to: ", self.currentmarks)


    def end_of_life(self):
        self.satisfaction_level_overall = self.satisfaction

    def end_of_life(self):
        self.satisfaction_level_overall = self.satisfaction
    
    def workload_update_male(self,workload,workload_first,workload_second,worload_third_male):

        if workload  == 0.84:
            return workload_first
        elif workload == 0.70:
            return workload_second
        elif workload == 0.60:
            return worload_third_male
    
    def workload_update_female_and_trans(self,workload,workload_first,workload_second,worload_third_female):

        if workload  == 0.84:
            return workload_first
        elif workload == 0.70:
            return workload_second
        elif workload == 0.60:
            return worload_third_female

    def determine_gender(self,gender,gender_range):
        if gender  > gender_range :
            return "Male"
        elif gender < gender_range :
            return "Female"
        elif gender == gender_range:
            return "Trans"
    
    def get_visa_status(self,visa,range):
        if visa < range:
            return "international"
        else:
            return "domestic"