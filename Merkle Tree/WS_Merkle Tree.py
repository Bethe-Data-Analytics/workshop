# -*- coding: utf-8 -*-
""" Workshop 23.03.2024 - Merkle Tree 3 - Authorisierungspfad

    Programmiere eine Merkle-Tree für die Liste [1, 2, 3, 4].
    
    
    @author:        Florian Bethe
    Datum:          28.03.2024
 
TODO: Authentisierungspfad (notwendige Partner zum Verifizieren gegen den Root Hash) im Knoten festhalten beim Aufbau, evtl. via Lambda Funktion
TODO: Authentisierungsfunktion implementieren als @static in MerkleTree Klasse

TODO: Geschwister binär addieren statt an einander zu hängen
TODO: Operatoren verwenden für binäre Addition und athenticate_against_root()
TODO: Prüfen, ob eine logische Operation statt der binären Addition sinnvoll verwendet werden kann

"""
from MerkleTreeNode import MerkleTreeNode
from MerkleTree import MerkleTree


DEBUG = False
HASH_LEN_FOR_OUTPUT = 3 # 0 = ungekürzt

if True or not DEBUG:
    print("\033[H\033[J", end="")

        
# Liste der Blattknoten
leaves = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# leaves = [1, 2, 3, 4]

# Baum erstellen
root_node, nodes = MerkleTree.buildTree(leaves)

# Root-Hash ausgeben
print()
# print(f"Root Hash: {root_node.hash_value}")
print(f"Root Hash: {MerkleTreeNode.hash_string(root_node.hash_value)}")

# print(root_node.authentication_path())
print(root_node.merkle_tree(show_authentication_path=False))
# print(root_node.merkle_tree(show_authentication_path=True))

print()
root_node.build_authentication_path()

print(nodes[1].authentication_path)
# print(nodes[1].authenticate_against_root("adfe872941bc6e006ada78c339e8137fd1db595dcb78baba0db330d065f73da0"))
if False:
    print(nodes[1].authenticate_against_root("85df8945419d2b5038f7ac83ec1ec6b8267c40fdb3b1e56ff62f6676eb855e70"))
else:
    for node in nodes:
        print(node.authenticate_against_root(root_node.hash_value))
        print("==============================================================")

print()
# print(root_node)

# print(root.authorisation_path_list())


# print()
# print(root_node.authentication_path)
# print()
# print(root_node.left.authentication_path)
# print()
# print(root_node.left.left.authentication_path)
# print(root_node.left.right.authentication_path)
# print()
# print(root_node.right.authentication_path)
# print()
# print(root_node.right.left.authentication_path)
# print(root_node.right.right.authentication_path)



