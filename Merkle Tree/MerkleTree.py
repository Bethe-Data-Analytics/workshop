# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:46:06 2024

@author: Florian Bethe
"""
from MerkleTreeNode import MerkleTreeNode

DEBUG = True

class MerkleTree(MerkleTreeNode):
    def __init__(self, value, parent=None):
        super().__init__(value, parent)
        
    def __str__(self):
        '''
        Returns
        -------
        Returns a human readable representation of this nodes properties.
        '''

        output = f"Value  = {self.value} (Hash: {self.hash_value})\n"
        output+= f"Parent = {self.parent}\n"
        if None == self.left:
            output+=f"{self.left} | "
        else:
            output+=f"{self.left.value} | "
            
        if None == self.right:
            output+=f"{self.right}"
        else:
            output+=f"{self.right.value}"

        output+= f"\n{self.authentication_path_to_string()}\n\n________________"

        return output

    @staticmethod
    def buildTree(leaves):
        if DEBUG:
            print(f"leaves = {leaves}\n")

        nodes      = [MerkleTreeNode(i) for i in leaves]
        nodes_list = nodes

        if False:
            print("Nodes:")
            for node in nodes:
                print(f"{MerkleTreeNode.hash_string(node)}\n")

        
        while len(nodes) != 1:
            temp = []
            for i in range(0, len(nodes), 2):
                node1 = nodes[i]
                if i+1 < len(nodes):
                    node2 = nodes[i+1]
                    # node2.authentication_path.append(node1.hash_value)
                    # node1.authentication_path.append(node2.hash_value)
                else:
                    temp.append(nodes[i])
                    break
                
                
                
                
                
                
                if True:
                    # Strings werden aneinandergehängt um den Wert vom Parent zu ermitteln
                    concatenated_hash = node1.hash_value + node2.hash_value
                    parent = MerkleTreeNode(concatenated_hash)
                else:
                    # Strings werden bittweise addiert, um den Wert des gemeinsamen Parent zu erhalten
                    parent = MerkleTreeNode(left=node1, right=node2)


                # parent1 = MerkleTreeNode(node1.hash_value + node2.hash_value)
                # parent2 = MerkleTreeNode(left=node1, right=node2)
                # print(f"_________________________________\nparent1:\n{parent1}\n---------------------------------\nparent2:\n{parent2}\n_________________________________")





                parent.left = node1
                parent.right = node2
                temp.append(parent)
                nodes_list.append(parent)
                
                node1.parent = parent
                node2.parent = parent
                
            nodes = temp

        # # Build authentisation paths for all nodes in tree.
        # nodes[0].build_authentication_path()
        # TODO: Build authentisation path for this node up to root.
        # nodes[0].build_authentication_path()

        return nodes[0], nodes_list
