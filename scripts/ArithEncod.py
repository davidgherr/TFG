# -*- coding: utf-8 -*-
"""
Created on Fri May 13 18:50:33 2022

@author: david
"""
import numpy as np
from decimal import Decimal,getcontext
import re

getcontext().prec=1500

'''
freq_table = {'|':0,'+':0,'-':0,'0':0,'1':0}
for i in b:
        if i in freq_table:
            freq_table[i] += 1
    
prob_table=[j/len(b) for j in freq_table.values()]
'''
class AD:
    def __init__(self, frequency_table):
        self.probability_table = self.get_probability_table(frequency_table)
    
    def get_probability_table(self, frequency_table):
        total_frequency = sum(list(frequency_table.values()))
    
        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = value/total_frequency
    
        return probability_table
    
    def encode(self, msg, probability_table):
        encoder = []
        
        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)
    
        for msg_term_idx in range(len(msg)):
            stage_probs = self.process_stage(probability_table, stage_min, stage_max)
    
            msg_term = msg[msg_term_idx]
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]
    
            encoder.append(stage_probs)
    
        stage_probs = self.process_stage(probability_table, stage_min, stage_max)
        encoder.append(stage_probs)
    
        encoded_msg = self.get_encoded_value(encoder)
    
        return encoder, encoded_msg
    
    def decode(self, encoded_msg, msg_length, probability_table):
        decoder = []
        decoded_msg = ""
    
        stage_min = Decimal(0.0)
        stage_max = Decimal(1.0)
    
        for idx in range(msg_length):
            stage_probs = self.process_stage(probability_table, stage_min, stage_max)
    
            for msg_term, value in stage_probs.items():
                if encoded_msg >= value[0] and encoded_msg <= value[1]:
                    break
    
            decoded_msg = decoded_msg + msg_term
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]
    
            decoder.append(stage_probs)
    
        stage_probs = self.process_stage(probability_table, stage_min, stage_max)
        decoder.append(stage_probs)
    
        return decoder, decoded_msg
    
    def get_encoded_value(self, encoder):
        """
        After encoding the entire message, this method returns the single value that represents the entire message.
        """
        last_stage = list(encoder[-1].values())
        last_stage_values = []
        for sublist in last_stage:
            for element in sublist:
                last_stage_values.append(element)

        last_stage_min = min(last_stage_values)
        last_stage_max = max(last_stage_values)

        return (last_stage_min + last_stage_max)/2
    
    def process_stage(self, probability_table, stage_min, stage_max):
        """
        Processing a stage in the encoding/decoding process.
        """
        stage_probs = {}
        stage_domain = stage_max - stage_min
        for term_idx in range(len(probability_table.items())):
            term = list(probability_table.keys())[term_idx]
            term_prob = Decimal(probability_table[term])
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [stage_min, cum_prob]
            stage_min = cum_prob
        return stage_probs
    
    
def FULL(bitstream):
    
    freq_table = {'|':0,'+':0,'-':0,'0':0,'1':0}
    for i in bitstream:
            if i in freq_table:
                freq_table[i] += 1
                
    AE=AD(freq_table)
    splitted=re.split('\|',bitstream)
    coded=[]
    for msg in splitted:
        _,encoded=AE.encode(msg,AE.probability_table)
        coded.append((encoded,len(msg)))
    
    decoded=[]
    
    for dmsg in coded:
        _,decoded_msg=AE.decode(dmsg[0], dmsg[1], AE.probability_table)
        decoded.append(decoded_msg)
        
    return [splitted,decoded]
    




    
            
    