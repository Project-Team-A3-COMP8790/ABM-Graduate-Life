
from mesa import Model
from mesa.time import RandomActivation


class graduateModel(Model):

    def __init__(self,N,width,height,initial_marks,gender,visa_status,dept) -> None:
        super().__init__()
        self.running = True
        self.num_agents = N

        self.grid = MultiGrid(width,height,True)

        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            student =  gradagents(i,self,initial_marks,gender,visa_status,dept)

            self.schedule.add(a)
        
        try:
            start_cell = self.gird.find_empty()
            self.grid.place_agent(student,start_cell)
        except:
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(student,start_cell)


        def step(self):
            self.schedule.step()