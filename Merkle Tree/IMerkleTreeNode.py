# -*- coding: utf-8 -*-
"""
@author: Florian Bethe
"""
import zope.interface
# from zope.interface import Attribute, implementer


class IMerkleTreeNode(zope.interface.Interface):
    
    # Properties
    hash_value          = zope.interface.Attribute("""hash value""")
    left                = zope.interface.Attribute("""left child""")
    right               = zope.interface.Attribute("""right child""")
    authentication_path = zope.interface.Attribute("""authentication path""")
    
    def __init__(self, value, parent, left, right):
        pass
    
    def __str__(self):
        pass
    
    def __add__(self, other):
        pass

    def build_authentication_path(self):
        pass

    def authenticate_against_root(self, root_hash:str):
        pass

    def str_to_binary(string):
        pass

    def hash_string(hash_value, hash_len_for_output):
        pass
        
    def indent(level:int, text:str):
        pass

    def merkle_tree(self, level, show_authentication_path, show_parent):
        pass




# pip install anytree
from anytree import Node
import hashlib
from operator import add

DEBUG = True
HASH_LEN_FOR_OUTPUT = 3 # 0 = ungekürzt

@zope.interface.implementer(IMerkleTreeNode)
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
        
        bin_str1 = MerkleTreeNode.str_to_binary(self.hash_value)
        bin_str2 = MerkleTreeNode.str_to_binary(other.hash_value)
        
        # Konvertiere die binären Zeichenketten in Dezimalzahlen
        dec_num1 = int(bin_str1, 2)
        dec_num2 = int(bin_str2, 2)
        
        # Addiere die Dezimalzahlen
        sum_dec = add(dec_num1, dec_num2)
        
        # Konvertiere das Ergebnis zurück in eine binäre Zeichenkette
        sum_bin = bin(sum_dec)[2:]

        
        value = sum_bin
        return value

    def authentication_path_to_string(self):
        '''
        Formatierte Darstellung des Authentisierungspfades.
        Liste aller Partner bis zum Root für den späteren Nachweis, dass der
        Knoten Teil des Roots ist.

        Returns
        -------
        Returns a human readable representation of the tree starting with this node.
        '''
        output = "Authentication Path:\n"

        for hash in self.authentication_path:
            output+=f" - {MerkleTreeNode.hash_string(hash)}\n"
            
        output+=f"\n-----------\n{self.authentication_path}\n-----------\n"

        return output



    @staticmethod
    def str_to_binary(string):
        binary_list = []
        for char in string:
            binary_list.append(bin(ord(char))[2:].zfill(8))
        return ''.join(binary_list)


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
    
