import haversine as hs

def calculate_coords(loc1, loc2):
    output = hs.haversine(loc1, loc2)
    return output