import json
import time
from hashlib import sha256


class Block(object):
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def print_block(self):
        print(f'index        : {self.index}')
        print(f'transactions : {self.transactions}')
        print(f'timestamp    : {self.timestamp}')
        print(f'previous_hash: {self.previous_hash}')
        print(f'hash         : {self.hash}')
        print(f'nonce        : {self.nonce}')


class Blockchain(object):
    def __init__(self, difficulty=2):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()
        self.difficulty: int = difficulty

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), '0')
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        block.hash = proof
        self.chain.append(block)

        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty)
                and block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return True

    def print_chain(self):
        for block in self.chain:
            print('------------------------------------')
            block.print_block()
            print('------------------------------------')


def main():
    blockchain = Blockchain(difficulty=5)
    blockchain.add_new_transaction({
        'price': 100000,
        'size': 10,
        'id': 11
    })
    blockchain.mine()
    blockchain.add_new_transaction({
        'price': 100000,
        'size': 10,
        'id': 14
    })
    blockchain.mine()

    blockchain.add_new_transaction({
        'price': 100000,
        'size': 10,
        'id': 18
    })
    blockchain.mine()
    blockchain.print_chain()


if __name__ == '__main__':
    main()
