import numpy as np
from typing import List, Tuple


def calculate_tour_length(tour: List[int], distance_matrix: np.ndarray) -> float:
    """
    Computes the total length of a tour.

    Parameters
    ----------

        tour: `List[int]`
            Tour to compute length of.

        distance_matrix: `np.ndarray`
            Distance matrix.
    """

    return sum(distance_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))


def two_opt_swap(tour: List[int], i: int, j: int) -> List[int]:
    """
    Perform a 2-opt swap by reversing the segment between positions i and j.

    Parameters
    ----------

        tour: `List[int]`
            Tour to perform swap.

        i:  `int`
            Position i of the tour.

        j: `int`
            Position j of the tour.

    Returns
    -------

        new_tour: `List[int]`
            Swapped tour.
    """

    new_tour = tour[:i]
    new_tour.extend(reversed(tour[i : j + 1]))
    new_tour.extend(tour[j + 1 :])
    return new_tour


def two_opt(
    initial_tour: List[int],
    distance_matrix: np.ndarray,
    max_iterations: int = 1000,
    improvement_threshold: float = 0.0,
) -> Tuple[List[int], float]:
    """
    Improve a tour using 2-opt local search.

    Parameters
    ----------

        initial_tour: `List[int]`
            Initial tour.

        distance_matrix: `np.ndarray`
            Distance matrix.

        max_iterations: `int`
            Maximum number of iterations without improvement.

        improvement_threshold: `float`
            Minimum improvement required to accept a swap.

    Returns
    -------

        best_tour, best_length: `Tuple[List[int], floats]`
            Improved tour and its length.
            
    """
    best_tour = initial_tour.copy()
    best_length = calculate_tour_length(best_tour, distance_matrix)

    improvement_found = True
    iterations_without_improvement = 0

    while improvement_found and iterations_without_improvement < max_iterations:
        improvement_found = False

        # Try all possible 2-opt swaps
        for i in range(1, len(best_tour) - 2):
            for j in range(i + 1, len(best_tour) - 1):
                # Calculate the change in tour length if we make this swap
                old_distance = (
                    distance_matrix[best_tour[i - 1]][best_tour[i]]
                    + distance_matrix[best_tour[j]][best_tour[j + 1]]
                )
                new_distance = (
                    distance_matrix[best_tour[i - 1]][best_tour[j]]
                    + distance_matrix[best_tour[i]][best_tour[j + 1]]
                )

                if new_distance < old_distance - improvement_threshold:
                    # If the swap improves the tour, make it
                    best_tour = two_opt_swap(best_tour, i, j)
                    best_length = calculate_tour_length(best_tour, distance_matrix)
                    improvement_found = True
                    iterations_without_improvement = 0
                    break

            if improvement_found:
                break

        if not improvement_found:
            iterations_without_improvement += 1

    return best_tour, best_length
