# ABM-Graduate-Life

/root/My Computer/ABM Graudate Life/ABM-Graduate-Life/simu/model.py Assumptions – 

 

Parameters ---  

      Cost of each Event is 70 per person, so accordingly the students are invited, and satisfaction is increased by 20 units as the base and the interaction between students stays independent to this. 

 

      Event Frequency is taken as the upper limit, as the events may get cancelled, etc. so keeping this into account, the occurrence of event is taken at random steps from 1 to 150. 

 

      Visa is considered a distribution, that is has a range from 0 to 100. 

  

      Gender of the student is considered a normal distribution and according to the gender of the individual, there will be an inherent disadvantage that they will perform worse than male [1] 

      The Women and Trans genders will have a more negative affect on the satisfaction according to the workload [1]. 

      The males too will be affected and not much as compared to the women. 

 

      The marks/grades of the students will play a vital role when the students interact with one another during the term. So, keeping this in mind, the marks will be affected by the students who are close to the agent and hence, the satisfaction will also be dependent on this. 

 

      Agent Interaction --- The number of agents that will interact and the number of agents that will not interact. 

 

      Workload --- determines how the satisfaction meter of the agents increase or decrease based on the workload they face. 

	 

Output ---  

      Satisfaction for the visualization. A student is  

      “Satisficed” state when the satisfaction unit is between 0 and 20 

      “Mildly satisfied” state when the satisfaction unit is between 40 and 60 

      “Unsatisfied” state when the satisfaction unit is between 60 and 80 

      “Needs help” state when the satisfaction unit is between 80 and 98 

      “Suicide” state when the satisfaction unit is between 98 and 100. Hence, no step of this student is considered. 

How to run the model ----- 

      -> Git pull {repository} 

      -> Pip3 Install the requirements.txt 

      -> mesa runserver 

Git Link --- https://github.com/Project-Team-A3-COMP8790/ABM-Graduate-Life 

Citations – 

suhail_02 https://doi.org/10.1080/1360080X.2019.1660045 
