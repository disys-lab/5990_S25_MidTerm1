import hashlib,json
class MerkleTree:
    def __init__(self, data_blocks):
        self.leaves = [self.hash_function(data) for data in data_blocks]
        self.tree = self.build_tree(self.leaves)

    def hash_function(self, data):
        """Computes SHA-256 hash of input data."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def acquire_leaf_index(self,data):
        """Computes index of leaf node given the hash contained in the data"""
        tx_leaf_index = -1

        for idx, leaf in enumerate(self.leaves):
            if self.hash_function(data) == leaf:
                tx_leaf_index = idx

        return tx_leaf_index

    def build_tree(self, leaves):
        """TODO: Implement logic for building a Merkle Tree using an array containing leaves.
        Ensure you handle corner cases such as odd number of leaves."""
        tree = []

        return tree

    def get_root(self):
        """TODO: Implement logic for obtaining the root hash of the Merkle tree"""
        return None

    def get_proof(self, index):
        """TODO: Implement logic for obtaining the proof of membership for a given leaf index"""
        proof = []
        return proof

    def verify_proof(self, proof, target_hash, root):
        """TODO: Implement logic for verifying the proof for a target hash given the root"""
        computed_hash = target_hash
        return computed_hash == root

if __name__ == "__main__":
    data_blocks = ["block1", "block2", "block3", "block4"]
    merkle_tree = MerkleTree(data_blocks)

    root_hash = merkle_tree.get_root()
    print("Merkle Root:", root_hash)

    proof = merkle_tree.get_proof(2)  # Proof for "block3"
    print("Merkle Proof for 'block3':", proof)

    valid = merkle_tree.verify_proof(proof, merkle_tree.hash_function("block3"), root_hash)
    print("Proof Valid:", valid)
