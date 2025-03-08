from mpi4py import MPI
import hashlib, uuid, json, random, pickle
from Q1_MerkleTrees import MerkleTree

class WalletManager:
    def __init__(self, num_wallets, filename="wallets.json"):
        self.NUM_WALLETS = num_wallets
        wallet_ids = [str(uuid.uuid4()) for _ in range(self.NUM_WALLETS)]
        self.wallet_ids = [hashlib.sha256(wallet.encode()).hexdigest() for wallet in wallet_ids]
        self.filename = filename

    def save_wallets(self):
        """Save wallet IDs to a file (JSON format)"""
        with open(self.filename, "w") as f:
            json.dump(self.wallet_ids, f, indent=4)

    def load_wallets(self):
        """Load wallets from JSON file"""
        with open(self.filename, "r") as f:
            self.wallet_ids = json.load(f)

        return self.wallet_ids

class Block:
    """denotes a block containing transactions and the Merkle tree developed in Q1"""
    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.merkle_tree = MerkleTree(transactions)
        self.merkle_root = self.merkle_tree.get_root()
        self.block_hash = self.compute_block_hash()

    def compute_block_hash(self):
        """Computes the block hash including Merkle root"""
        block_data = str(self.previous_hash) + str(self.merkle_root)
        return hashlib.sha256(block_data.encode()).hexdigest()


class LedgerHandler:
    def __init__(self,num_wallets,txns_per_epoch,initial_balance,genesis_block_hash):
        self.NUM_WALLETS = num_wallets
        self.TXNS_PER_EPOCH = txns_per_epoch
        self.INITIAL_BALANCE=initial_balance
        self.GENESIS_BLOCK_HASH=genesis_block_hash
        self.wallet_manager = WalletManager(self.NUM_WALLETS)
        self.wallet_manager.load_wallets()
        self.wallet_ids = self.wallet_manager.wallet_ids
        self.transactions_ledger = {}
        self.unspent_txns = {}
        self.initialize_state()

    def hash_function(self,data):
        data_str = json.dumps(data, sort_keys=True)
        """Computes SHA-256 hash of input data."""
        return hashlib.sha256(data_str.encode()).hexdigest()

    def initialize_state(self):
        txn_ids = []
        for idx in range(self.NUM_WALLETS):
            tx_data = {"from":"genesis","to": self.wallet_ids[idx], "amount":self.INITIAL_BALANCE}
            tx_id = str(self.hash_function(tx_data))
            tx_data["tx_id"] = tx_id
            tx_data["block_hash"] = genesis_block_hash

            txn_ids.append(tx_id)

            self.add_new_unspent_txns(tx_id,tx_data)

        genesis_block = Block(previous_hash=self.GENESIS_BLOCK_HASH, transactions=txn_ids)

        self.transactions_ledger[genesis_block.block_hash] = genesis_block

        self.current_hash = genesis_block.block_hash

        self.update_block_hash_of_unspent_txns(self.current_hash, txn_ids)

    def add_new_unspent_txns(self,tx_id,tx_data):
        self.unspent_txns[tx_id] = tx_data

    def update_block_hash_of_unspent_txns(self,block_hash,latest_txn_ids):
        for tx_id in latest_txn_ids:
            self.unspent_txns[tx_id]["block_hash"] = block_hash

    def simulate_new_transactions(self):
        txn_list = []
        for _ in range(self.TXNS_PER_EPOCH):

            from_wallet_idx,to_wallet_idx = random.sample(range(self.NUM_WALLETS), 2)

            from_wallet = self.wallet_ids[from_wallet_idx]
            to_wallet = self.wallet_ids[to_wallet_idx]

            tx_amt = random.uniform(0, 50)

            txn = {"from":from_wallet,"to": to_wallet, "amount":tx_amt }

            txn_list.append(txn)

        return txn_list

    def calculate_net_unspent_value(self,wallet_id):
        """TODO: (Same as Q2) Reuse same function as Q2"""
        total_value = 0
        unspent_tx_ids = []

        return total_value,unspent_tx_ids

    def eliminate_previous_unspent_txns(self,unspent_tx_ids):
        """TODO: (Same as Q2) Reuse same function as Q2"""
        pass

    def verify_unspent_txn_validity(self,unspent_txn_ids):
        """TODO: Given a list of unspent transaction ids, verify that each of them are
        contained within their respective blocks
        You can utilize `self.unspent_txns[tx_id]["block_hash"]` to acquire the block_hash of a tx_id
        If no block_hash exists for a particular tx_id within unspent_txn_ids, you may ignore it
        Once you get the block_has, refer to the "Block" class definition above to acquire the Merkle root of the block
        Then use the functions from the Merkle Tree definitions in Q1 to obtain validity of transactions and the proofs
        """

        unspent_txn_validity = True

        return unspent_txn_validity

    def process_transaction(self,txn_list,rank,epoch):
        valid_txns = []
        spent_tx_ids = []
        for txn_data in txn_list:

            from_wallet= txn_data["from"]
            to_wallet = txn_data["to"]
            tx_amt = txn_data["amount"]

            net_unspent_amt,unspent_tx_ids = self.calculate_net_unspent_value(from_wallet)

            unspent_txn_validity = self.verify_unspent_txn_validity(unspent_tx_ids)
            # TODO: Carry over steps from Question 2.
            # TODO: In addition to checking if total_unspent_amount > tx_amount, also check the validity of each transaction that makes up the total unspent amount.
            # TODO: Make a decision to reject or accept transactions based on whether unspent amount is sufficient for this wallet AND if the unspent transactions are valid.

        self.eliminate_previous_unspent_txns(spent_tx_ids)

        for txn in valid_txns:
            txn_id = txn["tx_id"]
            self.add_new_unspent_txns(txn_id, txn)

        return valid_txns

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

genesis_block_hash = "0" * 64
initial_balance = 100

num_epochs=int(sys.argv[1])
num_wallets = int(sys.argv[2])
txns_per_epoch = int(sys.argv[3])


if rank == 0:
    WalletManager(num_wallets).save_wallets()

def simulate_transaction_consensus():
    local_txn_list = local_LedgerHandler.simulate_new_transactions()

    serialized_local_txn_list = pickle.dumps(local_txn_list)

    serialized_global_txn_list = comm.alltoall([serialized_local_txn_list] * size)

    global_txn_list = []

    for data in serialized_global_txn_list:
        global_txn_list.extend(pickle.loads(data))

    return global_txn_list


comm.Barrier()
local_LedgerHandler = LedgerHandler(num_wallets=num_wallets,txns_per_epoch=txns_per_epoch,initial_balance=initial_balance,genesis_block_hash=genesis_block_hash)

for epoch in range(num_epochs):

    global_txn_list = simulate_transaction_consensus()

    latest_valid_txns = local_LedgerHandler.process_transaction(global_txn_list,rank,epoch)

    latest_valid_txn_ids = [txn["tx_id"] for txn in latest_valid_txns]

    new_block = Block(previous_hash=local_LedgerHandler.current_hash,transactions=latest_valid_txn_ids)

    local_LedgerHandler.transactions_ledger[new_block.block_hash] = new_block

    local_LedgerHandler.update_block_hash_of_unspent_txns(new_block.block_hash,latest_valid_txn_ids)

    local_LedgerHandler.current_hash = new_block.block_hash