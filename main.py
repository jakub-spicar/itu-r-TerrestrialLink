import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from utils.gdal_utils import get_elevation_profile, calculate_distance

# Coordinates of points
startLongitude, startLatitude = 14.3922919, 50.1030236
stopLongitude, stopLatitude = 14.4652642, 50.1364347

# Path to DEM file
baseDirectory = os.path.dirname(os.path.abspath(__file__))
demFile = os.path.join(
    baseDirectory, 
    'data', 
    'N50E014', 
    'ASTGTMV003_N50E014', 
    'ASTGTMV003_N50E014_dem.tif'
)

# Number of points for elevation profile calculation
numPoints = 6000

# Calculation of actual distance between points
distance = calculate_distance(
    startLongitude, startLatitude, 
    stopLongitude, stopLatitude
)

# Calculation of elevation profile
elevations = get_elevation_profile(
    demFile, 
    startLongitude, startLatitude, 
    stopLongitude, stopLatitude, 
    numPoints
)

# Saving results to CSV file
with open('results/elevation_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["index", "Distance", "Elevation"])
    for i, elevation in enumerate(elevations):
        writer.writerow([i, i / (numPoints - 1) * distance, elevation])

# Calculation and plotting of elevation profile
distances = np.linspace(0, distance, numPoints)
plt.plot(distances, elevations)
plt.xlabel('Vzdálenost (km)')
plt.ylabel('Elevation (m)')
plt.title('Výškový profil - Spoj A,B - x km')
plt.savefig('results/elevation_profile.png')
