#Computer Modelling and Simulation 
import math
import numpy as np
import random

class M1M2():
    def __init__(self, total_calls, mean_arrival_time_New, mean_arrival_time_Handover, mean_service_time):
        self.mean_arrival_time_Newcalls = 1/mean_arrival_time_New
        self.mean_arrival_time_Handover = 1/mean_arrival_time_Handover
        self.threshold = 2
        self.mean_service = mean_service_time 
        self.C = 16
        self.sim_time = 0
        self.num_event = self.C + 2
        self.num_calls = 0
        self.num_calls_NewCalls = 0
        self.num_calls_HandoverCalls = 0
        self.num_calls_required = total_calls
        self.server_status = np.zeros(self.C + 1)                                          
        self.area_server_status = np.zeros(self.C)
        self.time_next_event = np.zeros(self.C + 2)
        self.time_next_event[0] = self.sim_time + self.expon(self.mean_arrival_time_Newcalls)        
        self.time_next_event[self.C + 1] = self.sim_time + self.expon(self.mean_arrival_time_Handover)
        if self.time_next_event[0] < self.time_next_event[self.C + 1]:
            self.next_event_type=0
        else:
            self.next_event_type = self.C + 1
        for i in range(1, self.C + 1):
            self.time_next_event[i] = math.inf
        self.server_idle = 0        
        self.server_utilization = np.zeros(self.C)
        self.total_server_utilization = 0
        self.Total_Loss = 0
        self.Total_Loss_NewCalls = 0
        self.Total_Loss_HandoverCalls = 0

    def main(self):
        while ((self.num_calls_NewCalls + self.num_calls_HandoverCalls) < self.num_calls_required):
            self.timing()
            self.update_time_avg_stats()
            if (self.next_event_type == 0):
                self.arrive_NewCalls()                      
            elif (self.next_event_type == (self.C + 1)):
                self.arrive_HandoverCalls()                     
            else:  
                self.j = self.next_event_type
                self.depart()                       
        self.report()

    def timing(self):
        self.min_time_next_event = math.inf
        for i in range(0, self.num_event):
            if (self.time_next_event[i] <= self.min_time_next_event):
                self.min_time_next_event = self.time_next_event[i]
                self.next_event_type = i

        self.time_last_event=self.sim_time
        self.sim_time = self.time_next_event[self.next_event_type]
  
    def update_time_avg_stats(self):
        self.time_past = self.sim_time - self.time_last_event
        for i in range(1, self.C + 1):
            self.area_server_status[i-1] += self.time_past * self.server_status[i]

    def arrive_NewCalls(self):
        i = 0
        self.server_idle = 0
        ##Schedule next arrival
        self.time_next_event[0] = self.sim_time + self.expon(self.mean_arrival_time_Newcalls)
        while (self.server_idle == 0 and i <= self.C):
            if (self.server_status[i] == 0):
                self.server_idle = i
            i += 1
        if (self.server_idle != 0): ## Someone is IDLE
            self.server_status [self.server_idle] = 1
            self.time_next_event[self.server_idle] = self.sim_time + self.expon(self.mean_service)
        else:               ## server is BUSY
            self.Total_Loss_NewCalls += 1
        self.num_calls_NewCalls += 1

    def arrive_HandoverCalls(self):
        i = 0
        self.server_idle = 0
        ##Schedule next arrival
        self.time_next_event[self.C + 1] = self.sim_time + self.expon(self.mean_arrival_time_Handover)
        while (self.server_idle == 0 and i <= (self.C - self.threshold)):
            if (self.server_status[i] == 0):
                self.server_idle = i
            i += 1
        if (self.server_idle != 0): ## Someone is IDLE
            self.server_status [self.server_idle] = 1
            self.time_next_event[self.server_idle] = self.sim_time + self.expon(self.mean_service)
        else:               ## server is BUSY
            self.Total_Loss_HandoverCalls += 1
        self.num_calls_HandoverCalls += 1

    def depart(self):
        self.server_status [self.j] = 0
        self.time_next_event [self.j] = math.inf
    
    def expon(self, mean):
        return (-1 * mean * math.log(random.random()))
 
    def report(self):
        for i in range(0, self.C):
            self.server_utilization[i] = self.area_server_status[i]/self.sim_time
            self.total_server_utilization += self.area_server_status[i]
        self.total_server_utilization = self.total_server_utilization/(self.sim_time * self.C)
    
        print('----------------------------Simulation Report --------------------')
        µ = 1/self.mean_service
        λ1 = 1/self.mean_arrival_time_Newcalls
        λ2 = 1/self.mean_arrival_time_Handover
        SCBP = self.Total_Loss_NewCalls / self.num_calls_NewCalls
        SHFP = self.Total_Loss_HandoverCalls / self.num_calls_HandoverCalls
        SABP = SCBP + 10 * SHFP

        print('                                λ1 = ',λ1)
        print('                                λ2 = ',λ2)  
        print('                                 µ = ',µ)
        print('     Loss Probability of New Calls = ', SCBP)
        print('Loss Probability of Handover Calls = ', SHFP)
        print('   Aggregated Blocking Probability = ', SABP)
        print('          Total_server_utilization = ',self.total_server_utilization)

        One = 0
        Two = 0
        C = self.C
        N = self.threshold
        for i in range(0, C-N+1):
            One +=  (( 1/math.factorial(i)) * (((λ1 + λ2)/µ)**i))
            
        for i in range(C-N+1, C+1):
            Two +=  (( 1/math.factorial(i)) * (((λ1 + λ2)/µ)**(C-N)) * ((λ1/µ)**(i-C+N)))
        
        p0 = 1/(One + Two)
        pk_NewCalls = One * p0
        Pk_handOver = Two * p0
        print(' ------------  -----------Formulated Values -------------------------')
        print('                      pk_NewCalls = ',pk_NewCalls)
        print('                      Pk_handOver = ',Pk_handOver)
        print('                               p0 = ',p0)


myObject = M1M2(total_calls = 10_000_000, mean_arrival_time_New = 0.1, 
                   mean_arrival_time_Handover = 0.001, mean_service_time = 100)
myObject.main()