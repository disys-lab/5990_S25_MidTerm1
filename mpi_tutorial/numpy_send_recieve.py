from mpi4py import MPI
import numpy as np

# Initialize the MPI communicator
comm = MPI.COMM_WORLD

# Get the rank of the current process
rank = comm.Get_rank()

if rank == 0:
    # Process 0 creates a NumPy array and sends it to Process 1
    data = np.array([1.1, 2.2, 3.3, 4.4, 5.5], dtype='d')  # 'd' = double (float64)
    print(f"Process {rank} sending array: {data}")
    comm.Send([data, MPI.DOUBLE], dest=1, tag=100)  # Send the array to Process 1

elif rank == 1:
    # Process 1 prepares an empty array to receive the data
    data = np.empty(5, dtype='d')  # Must match the size & type of the sent array
    comm.Recv([data, MPI.DOUBLE], source=0, tag=100)  # Receive the array from Process 0
    print(f"Process {rank} received array: {data}")
