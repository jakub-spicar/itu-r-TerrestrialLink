from osgeo import gdal
from math import radians, cos, sin, asin, sqrt

def get_elevation_profile(dem_file, lon1, lat1, lon2, lat2, num_points):
    # Open the DEM file
    dem = gdal.Open(dem_file)
    geotransform = dem.GetGeoTransform()
    band = dem.GetRasterBand(1)

    # Function to retrieve elevation at a given point
    def get_elevation(lon, lat):
        # Convert coordinates from geographic to pixel coordinates
        x = int((lon - geotransform[0]) / geotransform[1])
        y = int((lat - geotransform[3]) / geotransform[5])
        return band.ReadAsArray(x, y, 1, 1)[0][0]

    # Calculation of elevation profile
    elevations = []
    for i in range(num_points):
        lon = lon1 + (lon2 - lon1) * i / (num_points - 1)
        lat = lat1 + (lat2 - lat1) * i / (num_points - 1)
        elevation = get_elevation(lon, lat)
        elevations.append(elevation)

    return elevations

def calculate_distance(lon1, lat1, lon2, lat2):
    # Convert coordinates from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Calculation of the straight-line distance
    x = (lon2 - lon1) * cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    return sqrt(x**2 + y**2) * 6371