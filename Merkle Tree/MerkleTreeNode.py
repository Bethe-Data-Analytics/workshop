# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 13:42:33 2024

@author: Florian Bethe
"""
import zope.interface
from zope.interface import Attribute, implementer
from IMerkleTreeNode import IMerkleTreeNode

from operator import add

# pip install anytree
from anytree import Node
import hashlib

DEBUG = True
HASH_LEN_FOR_OUTPUT = 3 # 0 = ungekürzt

@implementer(IMerkleTreeNode)
class MerkleTreeNode(Node):
    
    # # Properties
    # hash_value          = None
    # left                = None
    # right               = None
    # '''
    # Liste aller Partner bis zum Root für den späteren Nachweis, dass der
    # Knoten Teil des Roots ist.
    # '''
    # authentication_path = []
    
    # def __init__(self, value:str=None, parent:MerkleTreeNodeInterface=None, left:MerkleTreeNodeInterface=None, right:MerkleTreeNodeInterface=None):
    def __init__(self, value:str=None, parent=None, left=None, right=None):
        '''
        Initialises instance of MerkleTreeNode.

        Parameters
        ----------
        value : str, optional
            The value or name of this node.

        parent : MerkleTreeNode, optional
            The parent of this node. The default is None.

        left : MerkleTreeNode, optional
            The left descendant of this node. The default is None.

        right : MerkleTreeNode, optional
            The right descendant of this node. The default is None.

        Returns
        -------
        None.

        '''
        
        if None == value:
            # At least either left and or right must be set and concatenated into this becoming a 'parent' nodes value
            value = left + right
            
        self.left   = left
        self.right  = right
        self.parent = parent
        
        # Initialise base class
        super().__init__(value, parent)

        self.value      = value
        self.hash_value = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
     
        
    def __str__(self):
        '''
        Returns
        -------
        Returns a human readable representation of this nodes properties.
        '''
        if False:
            return super().__str__()
        else:
            output = f"Value  = {self.hash_string(self.value)} (Hash: {self.hash_value})\n"
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


    def __add__(self, other):
        
        bin_str_self  = MerkleTreeNode.str_to_binary(self.hash_value)[2:]
        bin_str_other = MerkleTreeNode.str_to_binary(other.hash_value)[2:]
        
        # Konvertiere die binären Zeichenkettenstrings in Ganzzahlen
        bin_str_int_self  = int(bin_str_self,  2)
        bin_str_int_other = int(bin_str_other, 2)
        
        # Addiere die Ganzzahlen
        sum_int = add(bin_str_int_self, bin_str_int_other)
        
        # Konvertiere das Ergebnis zurück in eine binäre Zeichenkette
        sum_bin = bin(sum_int)

        return sum_bin


    @staticmethod
    def str_to_binary(string, length=0, char='0'):
        string_as_bin_str = ''.join([bin(ord(ch))[2:] for ch in string])
        if length > 0:
            string_as_bin_str = string_as_bin_str.rjust(length, char)

        return string_as_bin_str


    @staticmethod
    def hash_string(hash_value:str="", hash_len_for_output:int=HASH_LEN_FOR_OUTPUT):
        if hash_len_for_output > 0:
            hash_value = hash_value[0:hash_len_for_output]
        return hash_value


    @staticmethod
    def indent(level:int=0, text:str=""):
        indent = ""
        for i in range(level):
            indent+= "   "
        indent+= text
        return indent
        
    
    def merkle_tree(
            self,
            level = 0,
            show_authentication_path = False,
            show_parent = False):
        '''
        Returns
        -------
        str
            Returns a human readable representation of the tree starting with
            this node.
        '''
        output = "\n"
        indent = self.indent(level)

        output+= indent + MerkleTreeNode.hash_string(self.hash_value)

        # if DEBUG:
        #     output+= f"\n{indent}[{self.value}]\n"
        #     output+= f"{MerkleTreeNode.authentication_path}\n"
        
        if None != self.left:
            output+= self.left.merkle_tree(
                level = level+1,
                show_authentication_path = show_authentication_path,
                show_parent = show_parent)
            
        if None != self.right:
            output+= self.right.merkle_tree(
                level = level+1,
                show_authentication_path = show_authentication_path,
                show_parent = show_parent)
        
        
        if None == self.left or None == self.right:
            output+= f" (Value = {self.value})"

        if show_authentication_path:
            if len(self.authentication_path) > 0:
                output+=f"\n{indent}vv Auth Path vv\n"
                for hash in self.authentication_path:
                    output+=f"{indent} -> {MerkleTreeNode.hash_string(hash)}\n"
                output+=f"{indent}^^ Auth Path ^^"

        return output

    
    def build_authentication_path(self):
        '''
        Build the authentication paths for this node and every descendant.

        Returns
        -------
        list
            This instances authentication_path.

        '''
        self.authentication_path = []


        # Child Node
        if None != self.parent:
            # Inherit parents authentication path first, if not empty.
            # self.authentication_path.append(self.hash_string(self.parent.authentication_path))
            if len(self.parent.authentication_path) > 0:
                # self.authentication_path.append(self.parent.authentication_path)
                self.authentication_path += self.parent.authentication_path

            # Get siblings hash_value
            if False:
                # [0..1] Geschwister
                if len(self.siblings) > 0:
                    # self.authentication_path.append(self.hash_string(self.siblings[0].hash_value))
                    self.authentication_path.append(self.siblings[0].hash_value)
                else:
                    # TODO: Einzelkinder testen
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            else:
                if self.parent.left.hash_value == self.hash_value:
                    self.authentication_path.append(self.hash_value + self.parent.right.hash_value)
                    # self.right.build_authentication_path()
                elif self.parent.right.hash_value == self.hash_value:
                    self.authentication_path.append(self.parent.left.hash_value + self.hash_value)
                    # self.left.build_authentication_path()
 




        # Follow left branch
        if None != self.left:
            self.left.build_authentication_path()

        # Follow right branch
        if None != self.right:
            self.right.build_authentication_path()

        # if DEBUG:
        #     print(f"{self.hash_string(self.hash_value)}  Authentication Path: ", end="")
        #     if len(self.authentication_path) > 0:
        #         print(f"{', '.join(self.authentication_path)}")
            
        return self.authentication_path


    def authenticate_against_root(self, root_hash:str):
        '''
        Rebuilds root hash from authentication_path and comares with given root_hash.

        Parameters
        ----------
        root_hash : str
            The hash_value of the root node to validate against.

        Returns
        -------
        bool
            True when rebuild has equals given root_hash, otherwise False.

        '''
        authentication_path = list(reversed(self.authentication_path))

        if DEBUG:
            print(f"\n_____________________\nAuthenticate Node\n\t{self.hash_string(self.hash_value)} (Value: {self.value})\nagainst\n\t{self.hash_string(root_hash)}")
            # print(f"Authentication Path:\n\t{self.authentication_path}")
            # print(f"Authentication Path reversed:\n\t{authentication_path}\n")

        
        auth_hash = self.hash_value
        for hash_value in authentication_path:
            if False:
                if DEBUG:
                    # print(f"->\t{self.hash_string(auth_hash)}")
                    print(f"->\t{self.hash_string(auth_hash)} + {self.hash_string(hash_value)} => ", end="")
    
                # TODO: Reihenfolge ist relevant!!!
                concatenated_hash = auth_hash + hash_value
                auth_hash = hashlib.sha256(str(concatenated_hash).encode("utf-8")).hexdigest()
    
                if DEBUG:
                    print(f"{self.hash_string(auth_hash)}")

            else:
                if DEBUG:
                    print(f"->\t{self.hash_string(auth_hash)}")
                    # print(f"->\t{self.hash_string(auth_hash)} + {self.hash_string(hash_value)} => ", end="")
    
                # TODO: Reihenfolge ist relevant!!!
                auth_hash = hashlib.sha256(str(hash_value).encode("utf-8")).hexdigest()
    
                if DEBUG:
                    print(f"{self.hash_string(auth_hash)}")
                

        if DEBUG:
            print(f"=> {root_hash == auth_hash}\n")

        return root_hash == auth_hash
    

# --------------------------------------------------------------------------- #
# -------------------------------- T E S T ---------------------------------- #
# --------------------------------------------------------------------------- #

if "__main__" == __name__:

    if not DEBUG:
        print("\033[H\033[J", end="")
        
        Node1 = MerkleTreeNode(value="1")
        Node2 = MerkleTreeNode(value="2")
        
        Node12 = MerkleTreeNode(value = Node1.hash_value + Node2.hash_value)
        Node1.parent = Node12
        Node2.parent = Node12
        Node12.left  = Node1
        Node12.right = Node2
        
        Node3 = MerkleTreeNode(value="3")
        Node4 = MerkleTreeNode(value="4")
        
        Node34 = MerkleTreeNode(value=Node3.hash_value + Node4.hash_value)
        Node3.parent = Node34
        Node4.parent = Node34
        Node34.left  = Node3
        Node34.right = Node4
        
        Node1234 = MerkleTreeNode(value=Node12.hash_value + Node34.hash_value)
        Node12.parent = Node1234
        Node34.parent = Node1234
        Node1234.left  = Node12
        Node1234.right = Node34

        test = Node1234
    
    print(MerkleTreeNode.indent(0, "Node1234"))
    # print(Node1234)
    print()
    print(MerkleTreeNode.indent(1, "Node12"))
    # print(Node12)
    print()
    print(MerkleTreeNode.indent(2, "Node1"))
    # print(Node1)
    print()
    print(MerkleTreeNode.indent(2, "Node2"))
    # print(Node2)
    print()
    print(MerkleTreeNode.indent(1, "Node34"))
    # print(Node34)
    print()
    print(MerkleTreeNode.indent(2, "Node3"))
    # print(Node3)
    print()
    print(MerkleTreeNode.indent(2, "Node4"))
    # print(Node4)
    
    """
85df8945419d2b5038f7ac83ec1ec6b8267c40fdb3b1e56ff62f6676eb855e70
[33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca]

   33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a
   [6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4bd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35]

      6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b (Value = 1)
      [1]

      d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35 (Value = 2)
      [2]

   13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca
   [4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a]

      4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce (Value = 3)
      [3]

      4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a (Value = 4)
      [4]

    
    85df8945419d2b5038f7ac83ec1ec6b8267c40fdb3b1e56ff62f6676eb855e70
       33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a
          6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b (Value = 1)
          d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35 (Value = 2)
       13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca
          4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce (Value = 3)
          4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a (Value = 4)




[MerkleTreeNode(
    '/33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca', 
    hash_value='85df8945419d2b5038f7ac83ec1ec6b8267c40fdb3b1e56ff62f6676eb855e70', 
    left=MerkleTreeNode('/33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4bd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', 
                        hash_value='33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a',
                        left=MerkleTreeNode('/33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4bd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35/1',
                                            hash_value='6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', 
                                            value=1),
                        right=MerkleTreeNode('/33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca/6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4bd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35/2',
                                             hash_value='d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35',
                                             value=2),
                        value='6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4bd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35'), 
    right=MerkleTreeNode('/33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca/4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
                         hash_value='13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca', 
                         left=MerkleTreeNode('/33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca/4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a/3',
                                             hash_value='4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce',
                                             value=3),
                         right=MerkleTreeNode('/33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca/4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a/4',
                                              hash_value='4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
                                              value=4),
                         value='4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a'),
    value='33b675636da5dcc86ec847b38c08fa49ff1cace9749931e0a5d4dfdbdedd808a13656c83d841ea7de6ebf3a89e0038fea9526bd7f686f06f7a692343a8a32dca')]

    """

    # mtn = MerkleTreeNode("Root")
    # child1 = MerkleTreeNode("Child1", parent=mtn)
    # child2 = MerkleTreeNode("Child2", parent=mtn)
    # print()
    # print(mtn)
    # print()
    # print(child1)
    # print()
    # print(child2)
    