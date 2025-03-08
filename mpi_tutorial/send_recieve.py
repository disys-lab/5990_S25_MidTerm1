from mpi4py import MPI

# Initialize the MPI communicator
comm = MPI.COMM_WORLD

# Get the rank (ID) of the current process
rank = comm.Get_rank()

if rank == 0:
    # Process 0 sends a message to Process 1
    data = "Hello from Process 0"
    comm.send(data, dest=1, tag=100)  # Sending data to Process 1 with tag 100
    print(f"Process {rank} sent data: {data}")

elif rank == 1:
    # Process 1 receives a message from Process 0
    data = comm.recv(source=0, tag=100)  # Receiving data from Process 0 with tag 100
    print(f"Process {rank} received data: {data}")
