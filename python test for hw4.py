#HW 4 with GUI Graphs
import numpy as np
import heapq
import matplotlib.pyplot as plt

class Event:
    def __init__(self, event_time, event_type):
        self.event_time = event_time
        self.event_type = event_type  # "arrival" or "departure"

    def __lt__(self, other):
        return self.event_time < other.event_time

class Process:
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time

class MM1QueueSimulator:
    def __init__(self, avg_arrival_rate, avg_service_time, max_processes=10000):
        self.avg_arrival_rate = avg_arrival_rate
        self.avg_service_time = avg_service_time
        self.max_processes = max_processes
        
        self.event_queue = []
        self.ready_queue = []
        self.clock = 0
        self.cpu_idle = True

        self.completed_processes = 0
        self.total_turnaround_time = 0
        self.total_waiting_time = 0
        self.total_busy_time = 0

        self.turnaround_times = []
        self.queue_lengths = []

    def generate_interarrival_time(self):
        return np.random.exponential(1 / self.avg_arrival_rate)

    def generate_service_time(self):
        return np.random.exponential(self.avg_service_time)

    def schedule_event(self, event):
        heapq.heappush(self.event_queue, event)

    def run_simulation(self):
        # Initialize the first arrival event
        first_arrival_time = self.generate_interarrival_time()
        self.schedule_event(Event(first_arrival_time, "arrival"))

        while self.completed_processes < self.max_processes:
            current_event = heapq.heappop(self.event_queue)
            self.clock = current_event.event_time

            if current_event.event_type == "arrival":
                self.handle_arrival(current_event)
            elif current_event.event_type == "departure":
                self.handle_departure(current_event)

            # Log queue length at each event for average computation
            self.queue_lengths.append(len(self.ready_queue))

        # Calculate performance metrics
        avg_turnaround_time = self.total_turnaround_time / self.completed_processes
        throughput = self.completed_processes / self.clock
        cpu_utilization = self.total_busy_time / self.clock
        avg_queue_length = np.mean(self.queue_lengths)

        return avg_turnaround_time, throughput, cpu_utilization, avg_queue_length

    def handle_arrival(self, event):
        service_time = self.generate_service_time()
        process = Process(self.clock, service_time)

        if self.cpu_idle:
            self.cpu_idle = False
            departure_time = self.clock + process.service_time
            self.total_busy_time += process.service_time
            self.schedule_event(Event(departure_time, "departure"))
        else:
            self.ready_queue.append(process)

        # Schedule the next arrival event
        next_arrival_time = self.clock + self.generate_interarrival_time()
        self.schedule_event(Event(next_arrival_time, "arrival"))

    def handle_departure(self, event):
        self.completed_processes += 1
        if self.ready_queue:
            next_process = self.ready_queue.pop(0)
            turnaround_time = self.clock - next_process.arrival_time + next_process.service_time
            self.total_turnaround_time += turnaround_time
            departure_time = self.clock + next_process.service_time
            self.total_busy_time += next_process.service_time
            self.schedule_event(Event(departure_time, "departure"))
        else:
            self.cpu_idle = True

# Testing simulator
arrival_rates = range(10, 31)  # Lambda will be test over 10 to 30 (31-1=30)
avg_service_time = 0.04  # Our given Average Service time
max_processes = 10000

with open('simulation_resultsFORHW4.txt', 'w') as file:
    file.write("Arrival Rate, Avg Turnaround Time, Throughput, CPU Utilization, Avg Queue Length\n")

    # In our test the metrics list should have 20 records each metric (20 = 30 -10)
    metrics = {
        'avg_turnaround_time': [],
        'throughput': [],
        'cpu_utilization': [],
        'avg_queue_length': []
    }

    for arrival_rate in arrival_rates:
        simulator = MM1QueueSimulator(arrival_rate, avg_service_time, max_processes)
        avg_turnaround_time, throughput, cpu_utilization, avg_queue_length = simulator.run_simulation()
        # Adds our different metrics into our list
        metrics['avg_turnaround_time'].append(avg_turnaround_time)
        metrics['throughput'].append(throughput)
        metrics['cpu_utilization'].append(cpu_utilization)
        metrics['avg_queue_length'].append(avg_queue_length)

        # Writes the metrics into our txt file
        file.write(f"Arrival Rate: {arrival_rate}: \n" 
            f"\tAvg Turnaround Time: {avg_turnaround_time}\n" 
            f"\tThroughput: {throughput}\n" 
            f"\tCPU Utilization/RHO: {cpu_utilization}\n"
            f"\tAvg number of processes in the ready queue {avg_queue_length}\n\n")
        
        # Prints in terminal the metrics
        print("Arrival Rate:", arrival_rate)
        print("Average Turnaround Time:", avg_turnaround_time)
        print("Throughput:", throughput)
        print("CPU Utilization/RHO:", cpu_utilization)
        print("AAvg number of processes in the ready queue:", avg_queue_length)
        print()

plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(arrival_rates, metrics['avg_turnaround_time'], marker='o')
plt.xlabel("Arrival Rate (λ)")
plt.ylabel("Average Turnaround Time")
plt.title("Average Turnaround Time vs Arrival Rate")

plt.subplot(2, 2, 2)
plt.plot(arrival_rates, metrics['throughput'], marker='o')
plt.xlabel("Arrival Rate (λ)")
plt.ylabel("Throughput")
plt.title("Throughput vs Arrival Rate")

plt.subplot(2, 2, 3)
plt.plot(arrival_rates, metrics['cpu_utilization'], marker='o')
plt.xlabel("Arrival Rate (λ)")
plt.ylabel("CPU Utilization")
plt.title("CPU Utilization vs Arrival Rate")

plt.subplot(2, 2, 4)
plt.plot(arrival_rates, metrics['avg_queue_length'], marker='o')
plt.xlabel("Arrival Rate (λ)")
plt.ylabel("Average Queue Length")
plt.title("Average Queue Length vs Arrival Rate")

plt.tight_layout()
plt.show()
