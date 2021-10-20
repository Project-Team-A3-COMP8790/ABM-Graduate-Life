# from win10toast import ToastNotifier
from mesa import Model
from mesa.time import RandomActivation
from .agent import Student_Model as gradagents
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
import random
import numpy as np
from random import randint

# n = ToastNotifier()

class graduateModel(Model):
    workload  = [0.84, .70,0.60]
    work_value = 0
    stepCounter = 0
    agentCounter = 0
    eventCount = 0
    def __init__(self,N = 1000,height= 10,width = 10,initial_marks_signma= 20,gender_range = 0.69,visa_range = 70,mark_range = 0.3,interaction_intensity = 50,workload_first= 1,workload_second=0.5,worload_third_male = -1,workload_third_female= -0.75,eventFrequency = 0, eventBudget = 0):
        super().__init__()
        gender_range= 1- gender_range
        gender_range = gender_range*100
        print(gender_range)
        self.num_agents = N
        self.work_value = self.workload[random.randint(0,2)]   
        self.grid = MultiGrid(width,height,True)
        self.schedule = RandomActivation(self)
        self.initial_marks_signma = initial_marks_signma
        self.visa_range = visa_range
        self.gender_range = gender_range
        self.workload_first = workload_first
        self.workload_second = workload_second
        self.workload_third_male = worload_third_male
        self.workload_third_female = workload_third_female
        self.mark_range = mark_range
        self.interaction_intentsity = interaction_intensity

        self.eventFrequency = []
        for eventNo in range (0, eventFrequency):
            self.eventFrequency.append(random.randint(1, 150))
        if(len(self.eventFrequency)>0):
            self.eventFrequency.sort()
        print(self.eventFrequency)
        
        self.eventBudget = eventBudget/70
        

        for i in range(self.num_agents):
            mu, sigma = 70, 20 # mean and standard deviation
            temp_marks = np.random.normal(mu, self.initial_marks_signma, N)
            avg_marks = temp_marks[random.randint(0,len(temp_marks)-1)]
            mu, sigma = 50, 30 # mean and standard deviation
            gender = np.random.normal(mu, sigma, N)
            gender = gender[random.randint(0,len(gender)-1)]
            mu, sigma = 70, 30 # mean and standard deviation
            visa = np.random.normal(mu, sigma, N)
            visa = visa[random.randint(0,len(visa)-1)]
            

   
            a = gradagents(avg_marks, gender, self.gender_range, visa, self.visa_range,self.mark_range,workload_first,self.interaction_intentsity,workload_second,worload_third_male,workload_third_female,i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            # print("\nFor ",i, "th Agent")
            self.schedule.add(a)
        
        self.datacollector = DataCollector(
            {

                "Satisfied": lambda m: self.count_type_of_sat(m, 20, -100000000000),
                "Mildly satisfied": lambda m: self.count_type_of_sat(m, 40, 20),
                "Unsatisfied": lambda m: self.count_type_of_sat(m, 80, 40),
                "Needs help": lambda m: self.count_type_of_sat(m, 99, 80),
                "Suicide": lambda m: self.count_type_of_sat(m, 100, 99),
                "males": lambda m: self.count_males(m),
                "females": lambda m: self.count_females(m),
                "international": lambda m: self.count_international(m),
                "domestic": lambda m: self.count_domestic(m),
                "AVG_Marks_Domestic": lambda m: self.average_domestic(m),
                "AVG_Marks_internation": lambda m: self.average_international(m),
                "AVG_Marks_males": lambda m: self.average_marks_gender(m, "Male"),
                "AVG_Marks_females": lambda m: self.average_marks_gender(m, "Female"),
                "AVG marks_interaction":  lambda m: self.average_interact(m,self.interaction_intentsity),
                "Avg marks no interaction": lambda m: self.average_dont_interact(m,self.interaction_intentsity)
            }
        )
        
        
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        EventOccured = False
        for agent in self.schedule.agents:
            agent.workload = self.work_value
            
            if(self.stepCounter in self.eventFrequency):
                if(randint(0,1)>0.5):
                    EventOccured = True
                    agent.satisfaction -= 5
                    self.eventBudget = self.eventBudget - 1
            
        if(EventOccured == True):
            self.eventCount+=1
            # n.show_toast("Event Occurred", "Event has Occurred", duration = 0.5)
        self.stepCounter+=1
        self.schedule.step()
        self.work_value = self.workload[random.randint(0,2)]  
         
        # collect data
        self.datacollector.collect(self)


    @staticmethod
    def count_type_of_sat(model, higher_limit, lower_limit):
        count = 0
        for sat in model.schedule.agents:
            if sat.satisfaction <= higher_limit and sat.satisfaction > lower_limit:
                count += 1
        print("Between ", higher_limit, "and ", lower_limit, "Count is: ", count)
     
        return count

    @staticmethod
    def count_males(model):
        """
        Helper method to count unsatisfaction in a given condition in a given model.
        """
        count = 0
        for sat in model.schedule.agents:
            if sat.gender == 'Male':
                count += 1
        print("Male: ", count)
     
        return count

    @staticmethod
    def count_females(model):
        count = 0
        for sat in model.schedule.agents:
            if sat.gender == 'Female':
                count += 1
        print("Female: ", count)
     
        return count
    @staticmethod
    def count_international(model):
        count = 0
        for sat in model.schedule.agents:
            if sat.visa_status == "international":
                count += 1
        print("international: ", count)
     
        return count
    
    @staticmethod
    def count_domestic(model):
        count = 0
        for sat in model.schedule.agents:
            if sat.visa_status == "domestic":
                count += 1
        print("domestic: ", count)
     
        return count

    @staticmethod
    def average_domestic(model):
        count = 0
        agent_value  = 0
        for sat in model.schedule.agents:
            if sat.visa_status == "domestic":
                count += sat.currentmarks
                agent_value += 1
        
     
        if agent_value == 0:
            return count
        else:
            print("Avg Domestic Marks: ", count/agent_value)
            return count/agent_value

    @staticmethod
    def average_international(model):
        count = 0
        agent_value = 0
        for sat in model.schedule.agents:
            if sat.visa_status == "international":
                count += sat.currentmarks
                agent_value += 1
     
        if agent_value == 0:
            return count
        else:
            print("Avg Intl Marks: ", count/agent_value)
            return count/agent_value


    @staticmethod
    def average_marks_gender(model, gender):
        count = 0
        agent_value = 0
        for sat in model.schedule.agents:
            if sat.gender == gender:
                count += sat.currentmarks
                agent_value += 1
        print(gender,": ", count)
     
        if agent_value == 0:
            return count
        else:
            return count/agent_value
    
    @staticmethod
    def average_interact(model,interaction_intensity):
        count = 0
        agent_value = 0
        for sat in model.schedule.agents:
            if sat.interaction_value < interaction_intensity:
                count += sat.currentmarks
                agent_value += 1
        print("Avg Interact: ", count)

        if agent_value == 0:
            return count
        else:
            return count/agent_value
    
    @staticmethod
    def average_dont_interact(model,interaction_intensity):
        count = 0
        agent_value = 0
        for sat in model.schedule.agents:
             if sat.interaction_value > interaction_intensity:
                count += sat.currentmarks
                agent_value += 1
        print("Avg Dont Interact: ", count)
     
        if agent_value == 0:
            return count
        else:
            return count/agent_value

