#include <iostream>

struct Process
{
    int id;
    int serviceTime;
    enum State
    {
        ARR,
        DEP
    } state;
};

unsigned int interArrivalTimes(int averageServiceTime){

    return -1;
}

// Handle Arrival of a process
void HandleArrival(Process &process){

}

// Handle Departure of a process
void HandleDeparture(Process &process){

}

// simulated process by giving the lambda, and average service time, and the number of processes
Process simulateProcessMM1(int labmda, int avgServiceTime, int numProcesses)
{
    unsigned int time; // Total time of processes
    
    // Creating first process
    Process process;
    process.id = 1;
    process.serviceTime = ;

    while(process.id <= numProcesses)
    {

    }

    return process;
}