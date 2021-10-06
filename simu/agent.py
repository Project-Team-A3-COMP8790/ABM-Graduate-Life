# High Workload -> decrease the satisfaction
# Move function (kinda) Student Academics in university + before university (GPA in undergrad) -> cumulative results
# Gender
# VISA Status (International OR Domestic)
# Department

# All the above things combined after 2 years to get the satisfaction. 


from mesa import Agent,Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.space import Grid
from mesa.time import RandomActivation

class Student_Model(Agent):
    satisfaction_level_overall = 0
    def __init__(self, arg_marks, gender, visa, dept, unique_id, model):
        super().__init__(unique_id, model)
        self.satisfaction = 0
        self.currentmarks = arg_marks
        self.gender = gender
        self.visa = visa
        self.dept = dept
        self.workload = 0.00
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        print ("Going to this position: ", new_position)
    
    def step(self, workload):
        self.move()
        # student_group = [{"currentmarks": 6}]
        student_group = self.model.grid.get_cell_list_contents([self.pos])
        cummulative = 0.00
        for other_students in student_group:
            # print (other_students.currentmarks)
            cummulative += other_students.currentmarks
        cummulative = cummulative/len(student_group)
        self.currentmarks = (0.7*cummulative) + (0.3*self.currentmarks)
        self.workload += workload
        print("Workload changed to: ", self.workload)
        print("Marks changed to: ", self.currentmarks)

    def get_current_satisfaction(self):
        self.satisfaction = 0.2*(self.currentmarks) - 0.4*(self.workload) + 0.3*(self.gender) + 0.5*(self.visa) + 0.2*(self.dept)
        print ("Final Satisfaction: ", self.satisfaction)

    def end_of_life(self):
        self.satisfaction_level_overall = self.satisfaction

class testModel(Model):
    """A model with some number of agents."""
    def __init__(self, N, width, height):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(10, 10, True)
        # Create agents
        for i in range(self.num_agents):
            avg_marks = self.random.randrange(10)
            gender = self.random.randrange(10)
            visa = self.random.randrange(10)
            dept = self.random.randrange(10)
            workload = self.random.randrange(10)
            a = Student_Model(avg_marks, gender, visa, dept,i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            print("\nFor ",i, "th Agent")
            a.step(workload)
            

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

empty_model = testModel(100,100,100)
empty_model.step()