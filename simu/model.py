
from mesa import Model
from mesa.time import RandomActivation
from .agent import Student_Model as gradagents
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
import random
import numpy as np

class graduateModel(Model):
    workload  = [0.84, .70,0.60]
    work_value = 0
    def __init__(self,N = 1000,height= 10,width = 10,initial_marks= 0,gender = 0.69,visa_status = 0.79):
        super().__init__()
        self.num_agents = N
        self.work_value = self.workload[random.randint(0,2)]   
        self.grid = MultiGrid(width,height,True)
        self.schedule = RandomActivation(self)



        for i in range(self.num_agents):
            mu, sigma = 70, 20 # mean and standard deviation
            temp_marks = np.random.normal(mu, sigma, N)
            avg_marks = temp_marks[random.randint(0,len(temp_marks)-1)]
            mu, sigma = 50, 30 # mean and standard deviation
            gender = np.random.normal(mu, sigma, N)
            gender = gender[random.randint(0,len(gender)-1)]
            visa = self.random.randrange(10)
            
            a = gradagents(avg_marks, gender, visa,i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            print("\nFor ",i, "th Agent")
            self.schedule.add(a)
        
        self.datacollector = DataCollector(
            {
            "Satisfied": lambda m: self.count_type_sat(m, 10),
            "Unsatisfied": lambda m: self.count_type_unsat(m, 10)
            
            }
        )
        
        
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        for agent in self.schedule.agents:
            agent.workload = self.work_value
        self.schedule.step()
        self.work_value = self.workload[random.randint(0,2)]  
         
        # collect data
        self.datacollector.collect(self)


    @staticmethod
    def count_type_sat(model, sat_condition):
        """
        Helper method to count satisfaction in a given condition in a given model.
        """
        
        count = 0
        for sat in model.schedule.agents:
            if sat.satisfaction <= sat_condition:
                count += 1
        print("Sa: ", count)
        
        return count

    @staticmethod
    def count_type_unsat(model, sat_condition):
        """
        Helper method to count unsatisfaction in a given condition in a given model.
        """
        count = 0
        for sat in model.schedule.agents:
            if sat.satisfaction > sat_condition:
                count += 1
        print("Un: ", count)
     
        return count