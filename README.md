# Assignment: Blockchain Transactions and Merkle Trees with MPI

## **Objective**
This assignment focuses on implementing and extending blockchain transaction validation using **Merkle Trees**, **Unspent Transaction Output (UTXO) models**, and **MPI for distributed consensus**. 
You will complete missing functionality and answer conceptual questions.
---

## Instructions to setup MPI using docker containers:
Its best to use a Dockerfile supplied in the code (under folder `mpi_tutorial`) to do this assignment.
Some helpful tips are as follows:
1. Build the container image using the command `docker build . -t mpi_docker_image:latest`. Ensure you are in the current directory (same as Dockerfile)  before you execute this command.
2. Run the built container image using `docker run -v <midterm_directory_path_on_host>:/home/midterm/ -d mpi_docker_image:latest`. There are are many benefits to doing this:
   - This will map all files on your host present inside the directory `<midterm_directory_path_on_host>` to the folder `</home/midterm>`. 
   - This will allow you to live edit your code files inside the midterm_directory and have the changes instantly reflected inside the container image on `/home/midterm`.
   - Whenever you want to test/debug your midterm code for any question, simpley make edits on your host and run using mpi on the container to test.
   - This means you can keep using your favorite IDE such as PyCharm or VSCode without really worrying about installing MPI on your local computer.
3. You would need to run code using MPI inside the container. Instructions for running MPI are given below.
No points will be taken off for not using docker container image. This is just for your convenience. If you prefer, you can run this code on the Pete supercomputer or on any other machine that has MPI available.


## Distributed System Setting for simulating a cryptocurrency
In this question you are expected to implement basic functions that help simulate UTXO inside a distributed system (achieved using MPI). The simulation of UTXOs you build in this question is very close to what happens in real-world cryptocurrencies like Bitcoin.
The simulation itself is designed around four entities:
1. Miners: The entities that broadcast transactions, carry out consensus and update ledgers. In this simulation, they are also keeping track of the UTXOs. We will use MPI processes (or ranks) to designate miners. This means each miner is represented by only 1 MPI rank.
2. Users: The end user who is represented by a wallet_id.
3. Epochs: This is equivalent to a single block round found in systems like Bitcoin.
4. Transactions per epoch: This simulates transactions that each miner recieves in every epoch.

### Creating users
- In the simulation, unique wallet ids are created by MPI process 0 and stored in a file called `wallets.json`. This is done using the `WalletManager` class. 
- Think of these wallets as the **universe** of all users for this simulation.

Important to remember that in the real-world wallets can be created independently by anyone without miner knowledge. 
However, for the sake of simulation, in this assignment, we create wallets on MPI Rank 0, store it in a local file and ensure all miners (i.e. other MPI ranks) are able to read this file.
Think of these wallets as the **universe** of all users for this simulation.

### Pre-funding user accounts (genesis transactions)
- Once we have created these users, we need to fund their wallets so that transactions can take place. Therefore, we use the `initialize_state()` method to fund wallets with 100 coins at the very beginning.
- These coins are what will drive the simulation forward. The associated transactions are genesis transactions which are mined by all miners at the very beginning.

Currently, these transactions are implemented as a synchronous operation that is performed by all miners at the beginning. 
However, in a real-cryto system, these transactions are carried out by the **first** miner and serve as the foundation for the distributed ledger to function. 

### Epoch simulations
- At every epoch, each miner process (MPI rank) calls the `simulate_transaction_consensus()` which simulates a set of new transactions **recieved** by the miner. Each simulated transaction includes a transaction amount randomly selected between (0,50)
- It is quite likely that these transactions are different across miners, therefore, there is a consensus operation among miners at the start of every epoch to come up with the overall set of transactions to process for this individual epoch.

Important to remember that in a real-world crypto system, the transactions are asynchronously generated and that miners actually conduct consensus on the **blocks**. 
However for this simulation, we assume that consensus is a synchronous affair and as a result, consensus over transactions guarantees block-consensus as well.


## Objective of this assignment: What happens at each epoch ( after Tx consensus has taken place across miners)?
This assignment primarily focuses on your understanding of implementing steps that can help deliver consensus across miners and fulfill transaction requirments for end users. 
The functionality of consensus simulation and genesis state formation have already been given in the code. You are expected to implement features that help achieve integrity of the distributed system. Here is a summary of each question and how it is related to each other:
- In Question 1 you are expected to implement functions pertaining to a Merkle tree. Please pay close attention to the instructions since these functions are going to be re-used in subsequent parts.
- In Question 2, you are expected to implement functions pertaining to UTXO management at each miner level such as whether UTXO of a wallet is sufficient to cover the requested tranasction amount. These are for transactions only and do not assume a block structure yet.
- In Question 3, you are expected to augment Q2's functionality by including **additional checks** that verify whether each UTXO of a wallet is legitimate or not. To do so, you will have to integrate Q2 with the Merkle tree implementation of Q1 and generate a proof for every valid transaction specified in UTXO of a wallet. 
  To help with Q3, a class definition of `Block` has been provided which manages the Merkle tree for each block. You are expected to use this class definition to access the Merkle tree for each block and simplify your implementation. 

  
## **Question 1: Implementing a Merkle Tree**

### **Background:**
A Merkle Tree is a data structure used to verify transactions efficiently. The provided `MerkleTree` class in `Q1_MerkleTrees.py` requires completion.

### **Task:**
1. [10 points] Implement the `build_tree` method to construct a Merkle Tree from a list of leaf nodes.
   - Ensure proper handling of an **odd number** of leaves by duplicating the last leaf.
   - Build the tree **bottom-up** using SHA-256 hashes.

2. [5 points] Implement `get_root` to return the Merkle Root (topmost node of the tree).

3. [5 points] Implement `get_proof` to generate a proof-of-inclusion for a given leaf index.

4. [10 points] Implement `verify_proof` to verify the proof using hash computations.

### **Example Output:**
```python
merkle_tree = MerkleTree(["tx1", "tx2", "tx3", "tx4"])
print("Merkle Root:", merkle_tree.get_root())
proof = merkle_tree.get_proof(2)  # Proof for "tx3"
valid = merkle_tree.verify_proof(proof, merkle_tree.hash_function("tx3"), merkle_tree.get_root())
print("Proof Valid:", valid)
```

---

## **Question 2: Implementing UTXO-Based Transactions**

### **Background:**
The Unspent Transaction Output (UTXO) model ensures that transactions are based on previously received funds. In `Q2_MPI_UTXO_consensus.py`, the **LedgerHandler** class is responsible for handling transactions.


### **Task:**
1. [5 points] Implement `calculate_net_unspent_value(wallet_id)`, which should:
   - Retrieve all unspent transactions for a given `wallet_id`.
   - Compute and return the total unspent balance.

2. [10 points] Implement `eliminate_previous_unspent_txns(unspent_tx_ids)`, which should:
   - Remove spent transactions from the UTXO set.

3. [20 points] Modify `process_transaction()` to:
   - Verify if the sender has enough unspent funds.
   - If valid, split the transaction: one transaction for the recipient and one for the remaining balance (change back to sender).
   - Reject transactions with insufficient funds.

4. [5 points]Run the program using MPI and analyze how transactions are propagated across different nodes. You would need to supply the following parameters:
   - NUM_EPOCHS : The total number of rounds of transactions to process
   - NUM_WALLETS : Total users in the system
   - TXNS_PER_EPOCH : Transactions to simulate per epoch. Transactions are randomly generated in `simulate_transaction_consensus()` which you are not expected to edit.

### **Example Execution:**
```bash
mpirun -n 4 python Q3_MPI_MerkleTree_consensus.py NUM_EPOCHS NUM_WALLETS TXNS_PER_EPOCH
```

### **Example Output:**
```python
ledger = LedgerHandler(num_wallets=10, txns_per_epoch=5)
unspent_value, unspent_txns = ledger.calculate_net_unspent_value("some_wallet_id")
print("Unspent Value:", unspent_value)
```

---

## **Question 3: Integrating Merkle Trees with MPI Consensus**

### **Background:**
In `Q3_MPI_MerkleTree_consensus.py`, transactions are grouped into blocks. Each block contains a **Merkle Tree** to verify transactions efficiently.

### **Task:**
1. [20 points] Implement `verify_unspent_txn_validity(unspent_txn_ids)`, which should:
   - Retrieve the Merkle Root from the relevant block.
   - Use Merkle Tree proofs to verify that transactions exist in the block.
   - Return `True` if all transactions are valid, otherwise `False`.

2. [10 points] Modify `process_transaction()` to:
   - Ensure transactions are validated using both **UTXO verification** and **Merkle Tree proofs** before accepting them.
   
3. Run the program using MPI and analyze how transactions are propagated across different nodes. 


## **Bonus Question: Simulating asynchronous computation over MPI**
Edit `Q3_MPI_MerkleTree_consensus.py` to include an asynchronous computation model. You can use non-blocking operations like [`irecv`](https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.irecv) and [`isend`](https://mpi4py.readthedocs.io/en/stable/reference/mpi4py.MPI.Comm.html#mpi4py.MPI.Comm.isend)
You can also use other ways to accomplish asynchronous communication such as simulating a dummy transaction with a probability.
Once youre done accomplishing asynchrnous communication, evaluate the strength of the given consensus protocol and provide details on how this can be made more resilient.
---

## **Submission Guidelines**
- Submit your modified Python scripts (`Q1_MerkleTrees.py`, `Q2_MPI_UTXO_consensus.py`, `Q3_MPI_MerkleTree_consensus.py`).

---

## **Evaluation Criteria**

All your code will be automatically evaluated against the following test cases:

| **NUM_MINERS** | **NUM_EPOCHS** | **NUM_WALLETS** | **TXNS_PER_EPOCHS** |
|----------------|----------------|-----------------|---------------------|
| 2              | 2              | 4               | 2                   |
| 6              | 4              | 8               | 8                   |
| 8              | 10             | 21              | 16                  |

Points will be deducted for runtime bugs, incorrect rejection of transactions and failure to produce Merkle proofs.

Good luck! 🚀

