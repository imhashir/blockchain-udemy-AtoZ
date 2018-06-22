from flask import Flask, jsonify
import json
import hashlib
import datetime


# Create a blockchain
class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, prev_hash = '0')

    def create_block(self, proof, prev_hash):
        block = {
            'index': len(self.chain) + 1,
            'prev_hash': prev_hash,
            'proof': proof,
            'timestamp': str(datetime.datetime.now())
        }
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = str(json.dumps(block, sort_keys=True)).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        prev_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            prev_hash = self.hash(prev_block)
            if block['prev_hash'] != prev_hash:
                print("Invalid prev hash\nBlock has prev: " + block['prev_hash'] + "\nOriginal hash of prev: " + prev_hash)
                return False

            prev_proof = prev_block['proof']
            curr_proof = block['proof']
            hash_operation = hashlib.sha256(str(curr_proof ** 2 - prev_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                print("Invalid Proof")
                return False

            prev_block = block
            block_index += 1

        print("Valid")
        return True

# Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new Block
@app.route("/mine_block", methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block['proof']
    new_proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.hash(prev_block)
    new_block = blockchain.create_block(new_proof, prev_hash)

    response = {'message': 'Congrats! You mined a block!',
               'index': new_block['index'],
               'prev_hash': prev_hash,
               'proof': new_proof,
               'timestamp': new_block['timestamp']}

    return jsonify(response), 200

@app.route("/get_chain", methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route("/hack_chain", methods=['GET'])
def hack_chain():
    blockchain.chain[0]['proof'] = 121212
    response = {'message': "Chain is hacked. Might be corrupted."}
    return jsonify(response), 200

@app.route("/is_valid", methods=['GET'])
def is_valid():
    response = {'message': "The chain is valid" if blockchain.is_chain_valid() else "Chain is not valid"}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)
