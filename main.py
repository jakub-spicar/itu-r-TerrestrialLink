import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import pandas as pd
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

# Create dataFrame to store the results
data = {
    "index": range(numPoints),
    "distance": [i / (numPoints-1) * distance for i in range(numPoints)],
    "elevation": elevations
}
df = pd.DataFrame(data)
df.to_csv('results/elevation_data.csv', index=False)

# Plotting elevation profile
fig, ax = plt.subplots()
ax.plot(  # Elevation
    df['distance'], df['elevation'], 
    linestyle='-', 
    color='blue', 
    label='Nadmořská výška'
)
ax.plot(  # O elevation
    df['distance'], [0]*len(df['distance']), 
    linestyle='-', 
    color='white'
)
ax.fill_between( 
    df['distance'], [0]*len(df['distance']), df['elevation'], 
    color='skyblue', alpha=0.3
)
ax.set_xlabel('Vzdálenost (km)')
ax.set_ylabel('Nadmořská výška (m)')
ax.set_title(f'Výškový profil - Spoj A,B - {distance:.2f} km')
plt.savefig('results/elevation_profile.png')

# Calculation for Earth curvature
kFactor = 4/3
R_e = kFactor * 6371
df['x'] = (df['distance'] * 1000 * (distance - df['distance'])) / (2 * R_e)
df['curved_elevation'] = df['elevation'] + df['x']

# Antena heights
startAntenaHeight = 30
endAntenaHeight = 0
frequency = 17.0
maxH2 = 0
n = 1.0
for i in range(numPoints):
    d1 = df['distance'][i]
    d2 = distance - d1
    h0 = df['curved_elevation'][i] 
    x = df['x'][i] 
    h1 = df['elevation'][0] + startAntenaHeight
    F1 = 17.3 * np.sqrt(n * d1 * d2 / (frequency * distance))
    if d2 > 0 and d1>0:
        h2 = h1 + distance * 1000 / (d1 * 1000) *  (x + h0 + F1 - h1)
        if h2 > maxH2:
            maxH2 = h2
            endAntenaHeight = maxH2 - df.elevation.iloc[-1]

df['F1'] = 17.3 * np.sqrt(n * df['distance'] * (distance - df['distance']) / (frequency * distance))
df['LOS'] = np.interp(df['distance'], [0, distance], [df.elevation[0] + startAntenaHeight, df.elevation.iloc[-1] + endAntenaHeight])

df.to_csv('results/path_clearance_s1.csv', index=False)

# Plotting of elevation profile with curvature
fig, ax = plt.subplots()
ax.plot(  # Earth curvature
    df['distance'], df['x'], 
    linestyle='--', 
    color='red', 
    label='Zakřivení Země'
)
ax.plot(  # Elevation profile
    df['distance'], df['curved_elevation'], 
    linestyle='-', 
    color='blue', 
    label='Výškový profil'
)
ax.fill_between(  # Fill between Earth curvature and elevation profile
    df['distance'], df['x'], df['curved_elevation'], 
    color='skyblue', alpha=0.3
)
ax.plot(  # Fresnel zone - upper
    df['distance'], df['LOS']+df['F1'], 
    linestyle='--', 
    color='gray',
    label='F1'
)
ax.plot(  # Fresnel zone - lower
    df['distance'], df['LOS']-df['F1'], 
    linestyle='--', 
    color='gray'
)
ax.plot(  # Start antena
    [
        0, 
        0
    ], 
    [
        df.elevation[0], 
        df.elevation[0] + startAntenaHeight
    ], 
    linestyle='-', 
    color='black', 
    linewidth=2
)
ax.plot(  # End antena
    [
        distance, 
        distance], 
    [
        df.elevation.iloc[-1], 
        df.elevation.iloc[-1] + endAntenaHeight
    ], 
    linestyle='-', 
    color='black', 
    linewidth=2
)
ax.plot(  # Line of sight
    [
        0, 
        distance
    ], 
    [
        df.elevation[0] + startAntenaHeight, 
        df.elevation.iloc[-1] + endAntenaHeight
    ], 
    linestyle='-', 
    color='black', 
    linewidth=2, 
    marker='o',
    label='Linie viditelnosti'
)
ax.set_xlabel('Vzdálenost (km)')
ax.set_ylabel('Nadmořská výška (m)')
ax.set_title(f'Výškový profil - Spoj A,B - {distance:.2f} km')
ax.legend()
plt.savefig('results/elevation_profile_with_curvature.png')
plt.show()