from hashlib import sha256
import json
from operator import length_hint
import time
import pickle
from json import dumps
from json import JSONEncoder
from flask import Flask, request
from model.Block import Block

class Blockchain: #clase blockchain
    # difficulty of our PoW algorithm
    difficulty = 2 #dificultad de la prueba de trabajo
  
    #def __init__(self): #constructor
    unconfirmed_transactions = [] #transacciones no confirmadas
    chain = [] #cadena
        #self.create_genesis_block()     #crea el bloque genesis
 
    def create_genesis_block(self): #crea el bloque genesis
        genesis_block = Block(0, [], time.time(), "0"*64) #crea el bloque genesis
        genesis_block.hash = genesis_block.compute_hash() #genera el hash del bloque genesis
        self.chain.append(genesis_block) #agrega el bloque genesis a la cadena
 
    @property #propiedad
    def last_block(self): #ultimo bloque
        return self.chain[-1] #retorna el ultimo bloque de la cadena
    
    def print_block(self,n): #imprime el bloque n
        if(len(self.chain) < n): #si la longitud de la cadena es menor o igual a n
            return 
        else: 
            block=self.chain[n] #obtiene el bloque n
            return ' \n Index: {}\n Transactions: {}\n Timestamp: {}\n PreviousHash: {}\n'.format(block.index,block.transactions,block.timestamp,block.previous_hash) #retorna el bloque n


    def proof_of_work(self,block): #prueba de trabajo
        block.nonce = 0 #nonce
        computed_hash = block.compute_hash() #genera el hash del bloque
        while not computed_hash.startswith('0'*Blockchain.difficulty): #mientras el hash no empiece con tantos ceros como la dificultad
            block.nonce += 1 #incrementa el nonce
            computed_hash = block.compute_hash() #genera el hash del bloque
        return computed_hash #retorna el hash del bloque

    def add_block(self, block, proof): #agrega un bloque
        print("add_block")
        previous_hash = self.last_block.hash #obtiene el hash del ultimo bloque
        if (previous_hash != block.previous_hash): #si el hash del ultimo bloque es diferente al hash del bloque
            return False #retorna falso
        if not self.is_valid_proof(block, proof): #si la prueba no es valida
            return False #retorna falso
        block.hash = proof #asigna el hash del bloque
        self.chain.append(block) #agrega el bloque a la cadena
        print(len(self.chain))
        for i in range(len(self.chain)):
            print(self.print_block(i))
        print(self.chain)
        return True #retorna verdadero

    def is_valid_proof(self, block, block_hash): #valida la prueba
        return (block_hash.startswith('0'*Blockchain.difficulty) and block_hash == block.compute_hash()) #retorna verdadero si el hash empieza con tantos ceros como la dificultad y el hash es igual al hash del bloque

    def new_transaction(self,transaction): 
        self.unconfirmed_transactions.append(transaction)
    
    def mine(self):
        if not self.unconfirmed_transactions: #si no hay transacciones no confirmadas
            return False #retorna falso

        last_block = self.last_block #obtiene el ultimo bloque
        new_block=Block(index=last_block.index+1,transactions=self.unconfirmed_transactions,timestamp=time.time(),previous_hash=last_block.hash) #crea un nuevo bloque
        proof = self.proof_of_work(new_block) #genera la prueba de trabajo
        self.add_block(new_block, proof) #agrega el bloque a la cadena
        self.unconfirmed_transactions=[]
        return new_block.index #retorna el indice del bloque

    def imprimir(self):
        for block in self.chain:
        #return json.dumps({"length":len(chain_data),
                            #"chain":chain_data})
            print (block)
        
        

app= Flask(__name__)
blockchain=Blockchain()