# -*- coding: utf-8 -*-
"""
Created on Sat May 14 12:41:50 2022

@author: David Garcerán Herráiz
"""


import bitstring

# Huffman Coding in python
class NodeTree(object):
    
        def __init__(self, left=None, right=None):
            self.left = left
            self.right = right
    
        def children(self):
            return (self.left, self.right)
    
        def nodes(self):
            return (self.left, self.right)
    
        def __str__(self):
            return '%s_%s' % (self.left, self.right)
  
class HUFF():
    
    def __init__(self,string):
        self.string=string
        self.freq={}
        self.huffmanCode=None
        self.exe()
    
    
    # Main function implementing huffman coding
    def huffman_code_tree(self,node, left=True, binString=''):
        if type(node) is str:
            return {node: binString}
        (l, r) = node.children()
        d = dict()
        d.update(self.huffman_code_tree(l, True, binString + '0'))
        d.update(self.huffman_code_tree(r, False, binString + '1'))
        return d
    
    def exe(self):
        # Calculating frequency
        for c in self.string:
            if c in self.freq:
                self.freq[c] += 1
            else:
                self.freq[c] = 1
        
        self.freq = sorted(self.freq.items(), key=lambda x: x[1], reverse=True)
        
        nodes = self.freq
        
        while len(nodes) > 1:
            (key1, c1) = nodes[-1]
            (key2, c2) = nodes[-2]
            nodes = nodes[:-2]
            node = NodeTree(key1, key2)
            nodes.append((node, c1 + c2))
        
            nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
        
        self.huffmanCode = self.huffman_code_tree(nodes[0][0])
        self.tree=node
    
    def __str__(self):
        
        s=' Char | Huffman code \n'   
        s+='----------------------\n'
        for (char, frequency) in self.freq:
            s+=' %-4r |%12s' % (char, self.huffmanCode[char])+'\n'
        return s
    
    def encode(self,string):
        if self.huffmanCode:
            s=''.join([self.huffmanCode[i] for i in string if i in self.huffmanCode])
            return bitstring.BitArray(bin=s)
    
    def decode(self,encoded):
        
        if type(encoded)==bitstring.BitArray:
            encoded=encoded.bin
        
        tree_copy=self.tree
        decoded_output=[]
        for x in encoded:
            if x=='1':
                tree_copy=tree_copy.right
            elif x=='0':
                tree_copy=tree_copy.left
            try:
                if len(str(tree_copy.left))>1 and len(str(tree_copy.right))>1:
                    pass
            except AttributeError:
                decoded_output.append(str(tree_copy))
                tree_copy=self.tree
        string=''.join([i for i in decoded_output])
        return string
    
                
        
        
        
                    
            