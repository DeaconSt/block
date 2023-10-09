from hashlib import sha256
import json
from operator import length_hint
import time
import pickle
from json import JSONEncoder
from flask import Flask, request
import requests

class Block: #clase bloque
    def __init__(self, index, transactions, timestamp, previous_hash): #constructor
        self.index = index #indice
        self.transactions = transactions #transacciones
        self.timestamp = timestamp #tiempo
        self.previous_hash = previous_hash #hash anterior
 
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True) #convierte el bloque a string
        return sha256(block_string.encode()).hexdigest() #genera el hash del bloque