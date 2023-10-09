from hashlib import sha256
import json
from operator import length_hint
import time
import pickle
from json import dumps
from json import JSONEncoder
from flask import Flask, request   
#from model.Blockchain import Blockchain
#from model.Block import Block
#from model.Blockchain import Blockchain
from model.Block import *
from model.Blockchain import *


app= Flask(__name__)
blockchain= Blockchain()

@app.route('/new_transaction',methods=['POST'])
def new_transaction():
    tx_data=request.get_json()
    require_fields=["author","content"]
    for field in require_fields:
        if not tx_data.get(field):
            return "Datos de transaccion invalidos",404
    tx_data["timestamp"]=time.time()
    blockchain.new_transaction(tx_data)
    return "Exito", 201


@app.route('/chain',methods=['GET'])
def get_chain():
    blockchain.imprimir()
    chain_data=[]
    length=len(blockchain.chain)
    print(length)
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length":len(chain_data),
                        "chain":chain_data})
    #return json.dumps({"length":length,
                       # "chain":chain_data})

@app.route('/genesis',methods=['GET'])
def genesis():
    blockchain.create_genesis_block()
    return "Genesis", 201

@app.route('/mine',methods=['GET'])
def mine_unconfirmed_transactions():
    result=blockchain.mine()
    if not result:
        return "Nothing to mine"
    return "Block #{} esta minado".format(result)

@app.route('/pending_tx',methods=['POST'])
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


app.run(port=8000)