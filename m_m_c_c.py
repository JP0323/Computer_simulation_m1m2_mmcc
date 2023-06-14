#Computer Modelling and Simulation  
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import pandas as pd

class MMCC():
    def __init__(self, total_calls, mean_arrival_time, mean_service_time):
        #Initializing all the parameters that are required
        self.mean_arrival = 1/mean_arrival_time
        self.mean_service = mean_service_time 
        self.sim_time = 0.0
        self.C = 16
        self.num_event = self.C + 1
        self.num_calls = 0
        self.num_calls_required = total_calls
        self.next_event_type = 0
        self.server_status =  np.zeros(self.C + 1)                                          
        self.area_server_status = np.zeros(self.C)
        self.time_next_event = np.zeros(self.C + 1) 
        self.time_next_event[0] = self.sim_time + self.expon(self.mean_arrival)            
        for i in range(1,self.C+1):
            self.time_next_event[i] = math.inf
        self.server_idle = 0        
        self.server_utilization = np.zeros(self.C)
        self.total_server_utilization = 0
        self.total_loss = 0
        
    #Main method which runs the entire Program
    def main(self):
        while (self.num_calls < self.num_calls_required):
            self.timing()
            self.update_time_avg_stats()
            if (self.next_event_type == 0):    
                self.arrive()                      
            else:
                self.j=self.next_event_type
                self.depart()                    
        self.report()

    def timing(self):
        self.min_time_next_event = math.inf
        for i in range(0, self.num_event):
            if (self.time_next_event[i] <= self.min_time_next_event):
                self.min_time_next_event=self.time_next_event[i]
                self.next_event_type=i

        self.time_last_event=self.sim_time
        self.sim_time=self.time_next_event[self.next_event_type]

    def update_time_avg_stats(self):
        self.time_past=self.sim_time-self.time_last_event
        for i in range(1,self.C + 1):
            self.area_server_status[i-1]+=self.time_past*self.server_status[i]
    
    def arrive(self):
        i = 0
        self.server_idle = 0
        self.time_next_event[0] = self.sim_time + self.expon(self.mean_arrival)

        while (self.server_idle == 0 and i <= self.C):
            if (self.server_status[i] == 0):
                self.server_idle = i
            i += 1

        if (self.server_idle != 0):  #Any of the server is idle
            self.server_status [self.server_idle] = 1
            self.time_next_event[self.server_idle] =self.sim_time + self.expon(self.mean_service)

        else:    #All Servers are busy
            self.total_loss +=1
        self.num_calls+=1

    def depart(self):
        self.server_status [self.j] = 0
        self.time_next_event [self.j] = math.inf

    def expon(self,mean):
        return (-1 * mean * math.log(random.random()))

    def report(self):
        #Simulated values of Server Utilization and Bolocking Probability
        for i in range(0,self.C):
            self.server_utilization[i] = self.area_server_status[i] / self.sim_time
            self.total_server_utilization += self.area_server_status[i]
        self.total_server_utilization = self.total_server_utilization/(self.sim_time * self.C)
        Simulated_total_server_utilization.append(self.total_server_utilization)
        
        Blocking_Probability = self.total_loss/self.num_calls_required
        Simulated_Blocking_probabilty.append(Blocking_Probability)
        
        #Formulated values of Server Utilization and Bolocking Probability
        µ = 1/self.mean_service
        Service.append(µ)
        λ = 1/self.mean_arrival
        Lamda.append(λ)
        
        Denomenator = 0
        for j in range (0,self.C+1):
            Denomenator += ((λ/µ)**j)/(math.factorial(j))
        BP = (((λ/µ)**self.C)/(math.factorial(self.C)))/Denomenator #BP = Blocking Pobability
        SU = (λ/(self.C*µ)) * (1 - BP) #SU = Server Utilisation
        Formulated_Blocking_probabilty.append(BP)
        Formulated_total_server_utilization.append(SU)

Formulated_total_server_utilization = []
Simulated_total_server_utilization  = []
Formulated_Blocking_probabilty = []
Simulated_Blocking_probabilty = []
Lamda = []
Service = []
mean_interarrival_time = 0.01
x = []
for i in range(20):
    x.append(mean_interarrival_time)
    myObject = MMCC(total_calls = 10_000_000, mean_arrival_time = mean_interarrival_time, mean_service_time = 100)
    myObject.main()
    mean_interarrival_time += 0.01

Headers = ['µ', 'λ' , 'FSU', 'SSU', 'FBP', 'SBP']
df = pd.DataFrame(list(zip(Service, Lamda, Formulated_total_server_utilization, Simulated_total_server_utilization,
                          Formulated_Blocking_probabilty, Simulated_Blocking_probabilty)), columns = Headers)

print(df)

plt.plot(x, Simulated_total_server_utilization)
plt.xlabel('Arrival rate')
plt.ylabel('Total Server Utilization')
plt.title('M/M/C/C')
plt.show()

plt.plot(x, Simulated_Blocking_probabilty)
plt.xlabel('Arrival rate')
plt.ylabel('Blocking Probability')
plt.title('M/M/C/C')
plt.show()