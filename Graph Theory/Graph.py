# -*- coding: utf-8 -*-
"""
@author: Florian Bethe
"""
# pip install numpy
import numpy as np

# pip install matplotlib
import matplotlib.pyplot as plt

DEBUG = False

class Graph():
    
    # keep vertex identifiers list of vertexes.
    vertexes = []

    # keep edges in adjacency matrix.
    adjacency_matrix = np.array([[]])
    
    def __init__(self):
        '''
        Initialises instance of Graph with empty sets of vertexes and edges.

        Returns
        -------
        None.

        '''
        
    def __str__(self):
        '''
        Returns
        -------
        Returns a human readable representation of this graphs properties.
        '''

        output = ""
        for row in self.adjacency_matrix:
            output += f"{row}\n"
        
        return output


    def add_vertex(self, key:str=None):
        '''
        Adds the key as name of vertex in list of vertexes.

        Returns
        -------
        None.

        '''
        if DEBUG:
            print(f"\nDEBUG:\n\tadd_vertex(key='{key}')\n\tadd vertex begin\n\nadjacency_matrix =\n{self.adjacency_matrix}")

        # avoid empty vertex identifier
        if None == key:
            key = f"Vertex {len(self.vertexes)+1}"

        # avoid duplicate vertex identifier
        elif key in self.vertexes:
            key += " (2)"

        self.vertexes.append(key)

        num_of_vertexes = len(self.vertexes)
        
        if 1 == num_of_vertexes:
            # special case: first vertex does not need a second dimension
            self.adjacency_matrix = np.zeros((1,1))
            
        else:            
            # add new row and initialise with 0
            new_row = np.zeros((1, self.adjacency_matrix.shape[1]))  # Eine neue Zeile mit der gleichen Anzahl an Spalten
            array_with_new_row = np.append(self.adjacency_matrix, new_row, axis=0)
    
            # add new column and initialise with 0
            new_col = np.zeros((array_with_new_row.shape[0], 1))  # Eine neue Spalte mit der gleichen Anzahl an Zeilen
            self.adjacency_matrix = np.append(array_with_new_row , new_col, axis=1)

        if DEBUG:
            print(f"\nDEBUG:\n\tadd_vertex(key='{key}')\n\tadd vertex end\n\nadjacency_matrix =\n{self.adjacency_matrix}")


    def add_edge(self, key_node_1:str, key_node_2:str, weight:float=1.0):
        '''
        Adds the weight for the nodes between key_node_1 and key_node_2.

        Returns
        -------
        None.

        '''

        if None == key_node_1 or None == key_node_2:
            print("!!! invalid node index !!!")
            return
        
        elif not (key_node_1 in self.vertexes and key_node_2 in self.vertexes):
            print("!!! invalid node index !!!")
            return
        
        elif 1 == len(self.vertexes):
            self.adjacency_matrix[0] = weight

        else:
            index_node_1 = self.vertexes.index(key_node_1)
            index_node_2 = self.vertexes.index(key_node_2)
        
        self.adjacency_matrix[index_node_1][index_node_2] = weight
        self.adjacency_matrix[index_node_2][index_node_1] = weight

        if DEBUG:
            print(self)


    def get_edges(self):
        '''
        Gets all nodes values within the adjacency matrix which are not zero.
        
        Assuming the direction is irrelevant, only one half of the matrixes
        values.

        Returns
        -------
        Array listing all nodes values combined with their position in the
        matrix in a list of tuples.
        '''

        non_zero_indices = np.nonzero(self.adjacency_matrix)
        non_zero_values  = self.adjacency_matrix[non_zero_indices]
        edges = list(zip(non_zero_indices[0], non_zero_indices[1], non_zero_values))
        
        # remove lower left half of the matrix
        edges_top_right = [(row, col, value) for row, col, value in edges if col > row]
       
        return edges_top_right


    def draw(self):
        '''
        Draws the vertexes and edges as matplotlib.pyplot scatter plot.

        Returns
        -------
        None.

        '''

        num_points = len(self.vertexes)

        # Radius des Kreises
        radius = 5  # Du kannst den Radius nach Bedarf anpassen
        arrow_offset = 5 / 100  # Umrechnung von Pixel in Einheiten (hier: 5 Pixel)
    
        # Berechne die Winkel für die gleichmäßige Verteilung der Punkte
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    
        # Berechne die x- und y-Koordinaten der Punkte auf dem Kreis
        x = radius * np.cos(angles)
        y = radius * np.sin(angles)
    
        # Erstelle das Diagramm
        plt.figure(figsize=(10, 10))  # Größe des Diagramms
        diameter = 50  # Durchmesser in Pixeln
        plt.scatter(x, y, s=diameter**2, color='lightblue', alpha=0.6)  # s=50^2 für Durchmesser von 50 Pixeln
    
        # Füge beschreibenden Text hinzu
        for i in range(num_points):
            plt.text(x[i], y[i], f"{self.vertexes[i]}", fontsize=20, color="red", ha="center", va="center")
        

        # Ermittle die Kanten (edges)
        edges = self.get_edges()

        if DEBUG:
            print("Edges:")
            print(edges)
        
        for e in edges:
            edge_start  = e[0]
            edge_end    = e[1]
            edge_weight = e[2]

            # Berechne die Positionen für den Pfeil zwischen den Endpunkten der Kante
            start_x = x[edge_start] + (arrow_offset * np.cos(angles[edge_start]))
            start_y = y[edge_start] + (arrow_offset * np.sin(angles[edge_start]))
            end_x   = x[edge_end]   - (arrow_offset * np.cos(angles[edge_end]))
            end_y   = y[edge_end]   - (arrow_offset * np.sin(angles[edge_end]))


            # start_x = x[edge_vertex_1] + (arrow_offset * np.cos(angles[edge_vertex_1])) - (100 / 100) * np.sin(angles[edge_vertex_1])  # Kürze um 100 Pixel am Anfang
            # start_y = y[edge_vertex_1] + (arrow_offset * np.sin(angles[edge_vertex_1])) - (100 / 100) * np.sin(angles[edge_vertex_1])
            # start_x = x[2] + (arrow_offset * np.cos(angles[2])) + (35 / 100) * np.cos(angles[2])  # Punkt 3 + Offset für Durchmesser/2
            # start_y = y[2] + (arrow_offset * np.sin(angles[2])) + (35 / 100) * np.sin(angles[2])
            # start_x = x[2] + (35 / 100) * np.cos(angles[2]) - (100 / 100) * np.sin(angles[2])  # Kürze um 100 Pixel am Anfang
            # start_y = y[2] + (35 / 100) * np.sin(angles[2]) - (100 / 100) * np.sin(angles[2])        
            # start_x = x[2] + (arrow_offset * np.cos(angles[2])) - (100 / 100) * np.sin(angles[2])  # Kürze um 100 Pixel am Anfang
            # start_y = y[2] + (arrow_offset * np.sin(angles[2])) - (100 / 100) * np.sin(angles[2])
    
            # end_x = x[edge_vertex_2] - (arrow_offset * np.cos(angles[edge_vertex_2])) - (100 / 100) * np.cos(angles[edge_vertex_2])  # Kürze um 100 Pixel am Ende
            # end_y = y[edge_vertex_2] - (arrow_offset * np.sin(angles[edge_vertex_2])) - (100 / 100) * np.cos(angles[edge_vertex_2])
            # end_x = x[3] - (arrow_offset * np.cos(angles[3])) - (35 / 100) * np.cos(angles[3]) - (5 / 100) * np.cos(angles[3])  # Punkt 4 - Offset für Durchmesser/2 und zusätzliche 5 Pixel
            # end_y = y[3] - (arrow_offset * np.sin(angles[3])) - (35 / 100) * np.sin(angles[3]) - (5 / 100) * np.sin(angles[3])
            # end_x = x[3] - (35 / 100) * np.cos(angles[3]) - (100 / 100) * np.cos(angles[3])  # Kürze um 100 Pixel
            # end_y = y[3] - (35 / 100) * np.sin(angles[3]) - (100 / 100) * np.cos(angles[3])
            # end_x = x[3] - (arrow_offset * np.cos(angles[3])) - (100 / 100) * np.cos(angles[3])  # Kürze um 100 Pixel
            # end_y = y[3] - (arrow_offset * np.sin(angles[3])) - (100 / 100) * np.cos(angles[3])
    
    
            # Zeichne den Pfeil
            plt.arrow(start_x,
                      start_y,
                      end_x - start_x,
                      end_y - start_y,
                      # head_width=0.3,
                      # head_length=0.5
                      fc='lightblue',
                      ec='lightblue',
                      linewidth=2)
    
        
            # Füge den Text entlang des Pfeils hinzu
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            plt.text(mid_x, mid_y, f"{edge_weight}", color="red", fontsize=20, ha='center', va='center', rotation=0)
    
    
        # Einstellungen für die Achsen
        # plt.xlim(-radius - 1, radius + 1)
        # plt.ylim(-radius - 1, radius + 1)
        plt.gca().set_aspect('equal', adjustable='box')  # Gleiche Skalierung für x und y
    
        # Titel und Labels
        plt.title(f'{num_points} Vertexes and their weighted Edges')
    
        # Diagramm anzeigen
        plt.grid(True)
        plt.show()


# --------------------------------------------------------------------------- #
# -------------------------------- T E S T ---------------------------------- #
# --------------------------------------------------------------------------- #

if "__main__" == __name__:

    if not DEBUG:
        import subprocess as sp
        sp.call('%reset -f', shell=True)  # für Windows
        # oder
        # sp.call('%reset -f', shell=True)  # für Linux/Mac
        
        print("\033[H\033[J", end="")

    print("\n__________________________________________________________________")
    print("\nT E S T   M O D E\n")

    if DEBUG:
        print("DEBUG = True")

    g = Graph() 
    
    g.add_vertex("a")
    g.add_vertex("b")
    g.add_vertex("c")
    g.add_vertex("d")
    g.add_vertex("e")
    g.add_vertex("f")
    # g.add_vertex("g")
    
    g.add_edge("a", "b")
    g.add_edge("b", "c", weight=100)
    g.add_edge("c", "d", weight= 20)
    g.add_edge("d", "a", weight=100)
    
    g.draw()
    
    print("__________________________________________________________________")
    
    print("\nGraph g =>\n")
    print(g)

    print("\nGraph Vertexes g.vertexes =>\n")
    print(g.vertexes)

    print("\nGraph Adjacency Matrix g.adjacency_matrix =>\n")
    print(g.adjacency_matrix)
