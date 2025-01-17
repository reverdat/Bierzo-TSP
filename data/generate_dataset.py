import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform


def generate_dataset(path_to_csv: str) -> pd.DataFrame:
    """
    Generates the distance matrix.

    Parameters
    ----------

        path_to_csv: `str`
            Path to CSV file containing coordinates.

    Returns
    -------

        distance_df: `pd.DataFrame`
            Distance matrix as DataFrame.
    
    """

    # Calculate pairwise distances using Haversine formula
    def _haversine_distance(point1, point2):
        lat1, lon1 = point1
        lat2, lon2 = point2
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of Earth in kilometers
        return c * r

    df = pd.read_csv(path_to_csv)
    coordinates = df[["Latitude", "Longitude"]].values
    distances = pdist(coordinates, metric=_haversine_distance)
    distance_matrix = squareform(distances)

    distance_df = pd.DataFrame(
        distance_matrix, index=range(1, len(df) + 1), columns=range(1, len(df) + 1)
    )

    return distance_df