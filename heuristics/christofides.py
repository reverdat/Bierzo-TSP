import numpy as np
from typing import List, Set, Tuple
import networkx as nx
from itertools import combinations

def prims_algorithm(distance_matrix: np.ndarray) -> List[Tuple[int, int]]:
    """
    Implements Prim's algorithm to find the Minimum Spanning Tree (MST).
    
    Parameters
    ----------

        distance_matrix:  `np.ndarray`
            Distance matrix.
        
    Returns
    -------

        mst_edge: `List[Tuple[int, int]]`
            List of tuples representing edges in the MST (node1, node2)
    """
    
    num_nodes = len(distance_matrix)
    
    mst_nodes: Set[int] = {0}  
    
    mst_edges: List[Tuple[int, int]] = []
    
    while len(mst_nodes) < num_nodes:
        min_weight = float('inf')
        min_edge = (-1, -1)
        
        for node in mst_nodes:
            for neighbor in range(num_nodes):
                if neighbor not in mst_nodes:
                    weight = distance_matrix[node][neighbor]
                    if weight < min_weight:
                        min_weight = weight
                        min_edge = (node, neighbor)
        
        if min_edge[0] != -1:  
            mst_nodes.add(min_edge[1])
            mst_edges.append(min_edge)
            
    return mst_edges

def get_odd_degree_vertices(
    mst_edges: List[Tuple[int, int]], num_nodes: int
) -> Set[int]:
    """
    Find vertices with odd degree in the MST.
    """
    degree = [0] * num_nodes
    for edge in mst_edges:
        degree[edge[0]] += 1
        degree[edge[1]] += 1

    return {i for i in range(num_nodes) if degree[i] % 2 == 1}


def minimum_weight_perfect_matching(
    distance_matrix: np.ndarray, odd_vertices: Set[int]
) -> List[Tuple[int, int]]:
    """
    Find minimum weight perfect matching for odd degree vertices.
    Uses NetworkX for the implementation.
    """
    G = nx.Graph()
    odd_vertices_list = list(odd_vertices)

    # Add edges between all odd degree vertices
    for i, j in combinations(range(len(odd_vertices_list)), 2):
        v1, v2 = odd_vertices_list[i], odd_vertices_list[j]
        G.add_edge(v1, v2, weight=distance_matrix[v1][v2])

    # Find minimum weight perfect matching
    matching = nx.min_weight_matching(G)
    return list(matching)


def find_eulerian_circuit(edges: List[Tuple[int, int]], num_nodes: int) -> List[int]:
    """
    Find Eulerian circuit in the multigraph formed by MST and matching edges.
    """
    # Create adjacency list representation
    adj = [[] for _ in range(num_nodes)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Find Eulerian circuit
    circuit = []

    def dfs(u: int):
        while adj[u]:
            v = adj[u].pop()
            adj[v].remove(u)
            dfs(v)
        circuit.append(u)

    dfs(0)
    return circuit


def christofides(distance_matrix: np.ndarray) -> List[int]:
    """
    Implements Christofides algorithm for TSP approximation.

    Parameters
    ----------
        distance_matrix: `np.ndarray`
            A square numpy array representing distances between nodes

    Returns
    -------
        hamiltonian_cycle: `List[int]`
            List of nodes representing the approximate TSP tour
    """
    num_nodes = len(distance_matrix)

    # Step 1: Find minimum spanning tree
    mst_edges = prims_algorithm(distance_matrix)

    # Step 2: Find vertices with odd degree in the MST
    odd_vertices = get_odd_degree_vertices(mst_edges, num_nodes)

    # Step 3: Find minimum weight perfect matching of odd degree vertices
    matching_edges = minimum_weight_perfect_matching(distance_matrix, odd_vertices)

    # Step 4: Combine MST and matching edges to form multigraph
    combined_edges = mst_edges + matching_edges

    # Step 5: Find Eulerian circuit
    euler_circuit = find_eulerian_circuit(combined_edges, num_nodes)

    # Step 6: Convert Eulerian circuit to Hamiltonian cycle (shortcut)
    # Keep track of visited nodes to avoid repetition
    visited = set()
    hamiltonian_cycle = []
    for v in euler_circuit:
        if v not in visited:
            hamiltonian_cycle.append(v)
            visited.add(v)

    # Complete the cycle
    hamiltonian_cycle.append(hamiltonian_cycle[0])

    return hamiltonian_cycle