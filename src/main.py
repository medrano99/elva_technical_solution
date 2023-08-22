import requests as request
from secrets_key import TOKEN_ARGIS
from shapely.geometry import Point, Polygon
from pyproj import Transformer

def geocoding(street_address: str) -> dict:
    # Geocode the provided street address using ArcGIS API
    url = f"https://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?f=pjson&singleLine={street_address}&token={TOKEN_ARGIS}"
    result = request.get(url=url).json()
    candidates = result["candidates"][0]
    return candidates["location"]

def get_neighborhood(x_lon, y_lat) -> str:
    # Base URL of the neighborhood query service
    url = "https://www.portlandmaps.com/arcgis/rest/services/Public/COP_OpenData/MapServer/125/query"

    # Query parameters to obtain neighborhood geometry
    params = {
        "where": "1=1",
        "geometryType": "esriGeometryPolygon",
        "outFields": "*",
        "f": "json"
    }

    # Perform GET request to obtain neighborhood geometry
    response = request.get(url, params=params)
    data = response.json()

    if "features" not in data:
        return ""
    features = data["features"]
    if len(features) == 0:
        return ""
        
    # Convert Web Mercator (EPSG:3857) to geographic (latitude, longitude)
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    for feat in features:
        neighborhood = feat["attributes"]["NAME"]
        coordinates = feat["geometry"]["rings"][0]    

        # Convert projected coordinates to geographic
        geographic_coordinates = [transformer.transform(x, y) for x, y in coordinates]

        # Create a polygon object using geographic coordinates of the neighborhood
        neighborhood_polygon = Polygon(geographic_coordinates)

        # Coordinates of the input point in geographic
        longitude_point, latitude_point = x_lon, y_lat
        point = Point(longitude_point, latitude_point)

        # Check if the point is within the neighborhood polygon
        result = bool(point.within(neighborhood_polygon))
        if result:
            return neighborhood
    
    return ""    

def increment_address_and_query(address, original_neighborhood, increment=100):
    # Geocode the provided address
    location = geocoding(address)
    
    if location:
        # Get the neighborhood for the geocoded location
        neighborhood = get_neighborhood(location["x"], location["y"])
        
        if neighborhood and neighborhood == original_neighborhood:
            # Increment the address and print the new address and neighborhood
            new_address = f"{int(address.split()[0]) + increment} {' '.join(address.split()[1:])}"
            print("Address:", new_address, neighborhood)
            
            # Recursively call the function for the new address
            increment_address_and_query(new_address, original_neighborhood, increment)
        else:
            print("Neighborhood has changed", neighborhood)
    else:
        print("Geocoding error.")

if __name__ == '__main__':
    # Solution 1: Geocode a street address and print the result
    street_address = "1300 SE Stark Street, Portland, OR 97214"
    location = geocoding(street_address=street_address)
    message = "Current position is: ({x}, {y}) for street address '{add}'".format(x=location["x"], y=location["y"], add=street_address)
    print(message)

    # Solution 2: Get the neighborhood for the geocoded location
    neighborhood = get_neighborhood(location["x"], location["y"])

    # Solution 3: Print the neighborhood for the given position
    print("For position ({}, {}) the corresponding neighborhood is {}".format(location["x"], location["y"], neighborhood))

    # Solution 4: Increment the initial address and query the neighborhood
    initial_address = "1300 SE Stark Street, Portland, OR"
    location = geocoding(initial_address)
    original_neighborhood = get_neighborhood(location["x"], location["y"])

    increment_address_and_query(initial_address, original_neighborhood)
