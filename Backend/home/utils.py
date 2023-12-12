import math
from accounts.models import Kitchen

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # calculate the central angle between the two points on the unit sphere
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Calculate the distance
    distance = R * c
    
    return distance


def getNearestKitchen(currentLatitude, currentLongitude):
    
    if currentLatitude != None and currentLongitude !=None:

        kitchen = Kitchen.objects.all()
        area = 5
        nearest_kitchen = []

        for place in kitchen:
            if place.location and place.latitude!=0 and place.longitude!=0:
                distance = math.ceil(haversine(float(currentLatitude), float(currentLongitude), place.latitude, place.longitude))
                if distance <= area:
                    nearest_kitchen.append(place.kitchen_name)
            else:
                continue

        return nearest_kitchen
    
   
