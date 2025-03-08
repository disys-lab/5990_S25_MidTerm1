from mpi4py import MPI
import hashlib, uuid, json, random, pickle
from Q1_MerkleTrees import MerkleTree

class WalletManager:
    def __init__(self, num_wallets, filename="/tmp/wallets.json"):
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


class LedgerHandler:
    def __init__(self,num_wallets,txns_per_epoch,initial_balance=100):
        self.NUM_WALLETS = num_wallets
        self.TXNS_PER_EPOCH = txns_per_epoch
        self.INITIAL_BALANCE=initial_balance
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
        for idx in range(self.NUM_WALLETS):
            tx_data = {"from":"genesis","to": self.wallet_ids[idx], "amount":self.INITIAL_BALANCE}
            tx_id = str(self.hash_function(tx_data))
            tx_data["tx_id"] = tx_id

            self.add_new_unspent_txns(tx_id,tx_data)

    def calculate_net_unspent_value(self,wallet_id):
        """TODO: Implement logic to calculate total unspent value and the unspent transactions in a given wallet_id"""
        total_value = 0
        unspent_tx_ids = []

        return total_value,unspent_tx_ids

    def eliminate_previous_unspent_txns(self,unspent_tx_ids):
        """TODO: Implement logic for eliminating previously unspent transactions. Hint: You can use self.unspent_txns[tx_id] and delete transactions that have been spent."""
        pass

    def add_new_unspent_txns(self,tx_id,tx_data):
        self.unspent_txns[tx_id] = tx_data

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

    def process_transaction(self, txn_list, rank, epoch):

        valid_txns = []
        spent_tx_ids = []
        for txn_data in txn_list:

            from_wallet = txn_data["from"]
            to_wallet = txn_data["to"]
            tx_amt = txn_data["amount"]

            #TODO: For each new transaction (i.e. in tx_data), determine the net unspent trransaction amount, unspent transaction ids corresponding to the from wallet.
            #TODO: For each new transaction you will need to eliminate the previous transactions from the unspent transaction list.
            #TODO: For each transaction's "from wallet", you will need to check if the transaction amount is less than the unspent amount.
            #TODO: Make a decision to reject or accept transactions based on whether unspent amount is sufficient for this wallet
            #TODO: If youre accepting transactions create two new transactions, that splits the outstanding amount into two parts like the example below:
            """
            txn1_data = {"from":from_wallet,"to": to_wallet, "amount":tx_amt }
            txn1_id = str(self.hash_function(txn1_data))
            txn1_data["tx_id"] = txn1_id

            new_net_balance = net_unspent_amt - tx_amt
            txn2_data = {"from":from_wallet,"to": from_wallet, "amount":new_net_balance}
            txn2_id = str(self.hash_function(txn2_data))
            txn2_data["tx_id"] = txn2_id
            """
            #TODO: This ensures the "change" of the outstanding amount (i.e. net unspent amount)-tx amount will be refunded back to the "from wallet"

        #TODO: Once youre done with iterating through new transactions you will need to eliminate the unspent transactions that were consumed to fulfill the new transactions.
        #TODO: Make sure that the new transactions that are resulted are put inside the unspent transaction pool
        """You can use code like this to ensure the unspent transaction pool is constantly updated:
        self.eliminate_previous_unspent_txns(spent_tx_ids)

        for txn in valid_txns:
            txn_id = txn["tx_id"]
            self.add_new_unspent_txns(txn_id, txn)
        """


        return valid_txns

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

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
local_LedgerHandler = LedgerHandler(num_wallets=num_wallets,txns_per_epoch=txns_per_epoch,initial_balance=initial_balance)

for epoch in range(num_epochs):

    #simulate consensus transactions
    global_txn_list = simulate_transaction_consensus()

    #find out latest valid transactions by processing new broadcasted transactions
    latest_valid_txns = local_LedgerHandler.process_transaction(global_txn_list,rank,epoch)







