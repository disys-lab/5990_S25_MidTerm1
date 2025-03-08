from mpi4py import MPI

# Initialize the MPI communicator
comm = MPI.COMM_WORLD

# Get the total number of processes
size = comm.Get_size()

# Get the rank (ID) of the current process
rank = comm.Get_rank()

# Get the name of the processor (useful in cluster computing)
processor_name = MPI.Get_processor_name()

param = 0
param_str = f"param={param}"

# Print message from each process
print(f"Hello from process {rank} out of {size} on {param_str}")
with open(f"process_{rank}/data.txt") as file:
    data = file.read()
    print(data)

# Barrier synchronization (optional, to ensure all processes reach this point)
comm.Barrier()

if rank == 0:

    print("All processes have completed execution.")
