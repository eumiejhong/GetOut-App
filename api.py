import requests
from coords_calc import calculate_coords
from flask import Flask, render_template, request, redirect, flash, session, g

API_KEY = 'fb417b74-ac58-4623-9f4d-d69943dfa739'
DEFAULT_CAMPSITE_IMAGE = "https://images.pexels.com/photos/2975445/pexels-photo-2975445.jpeg"
DEFAULT_RECPARK_IMAGE = "https://images.pexels.com/photos/210243/pexels-photo-210243.jpeg"
DEFAULT_DESCRIPTION = "More info coming soon!"

DEFAULT_LATITUDE = 42.261702
DEFAULT_LONGITUDE = -71.79741589999999

class Campsite():
    def __init__(self, campsiteJsonData):
        self.type = 'campsite'
        media = campsiteJsonData['MEDIA']
        self.image_url = DEFAULT_CAMPSITE_IMAGE

        if (len(media)):
            self.image_url = media[0].get('URL', DEFAULT_CAMPSITE_IMAGE)

        self.name = campsiteJsonData['FacilityName']

        description = campsiteJsonData['FacilityDescription']
        self.description = DEFAULT_DESCRIPTION

        if (len(description)):
            self.description = description

        self.rec_gov_id = campsiteJsonData.get('FacilityID', None)
        self.id = f"{self.type}-{self.rec_gov_id}"
        self.directions = campsiteJsonData.get('FacilityDirections', None)
        
        if campsiteJsonData.get('FACILITYADDRESS', []).__len__() > 0:
            self.city = campsiteJsonData.get('FACILITYADDRESS')[0].get('City', None)
            self.state = campsiteJsonData.get('FACILITYADDRESS')[0].get('AddressStateCode', None)
        else:
            self.city = None
            self.state = None
        self.latitude = campsiteJsonData.get('FacilityLatitude', None)
        self.longitude = campsiteJsonData.get('FacilityLongitude', None)

    def to_json(self, user=None):
        data = {
            'image_url': self.image_url,
            'name': self.name,
            'description': self.description,
            'rec_gov_id': self.rec_gov_id,
            'id': self.id,
            'directions': self.directions,
            'city': self.city,
            'state': self.state,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'has_liked': False,
            'type': 'campsite'
        }

        if user:
            data['has_liked'] = user.has_liked_site(self) is not None

        return data
        

def get_campsites( latitude, longitude, limit=1, offset=0, radius=15,):
    params = {'apikey': API_KEY, 'limit': limit, 'offset': offset, 'full': True, 'latitude': latitude, 'longitude': longitude, 'radius': radius}
    response = requests.get('https://ridb.recreation.gov/api/v1/facilities', params=params)
    data = response.json()
    campsites = data['RECDATA']

    return [Campsite(d) for d in campsites]

class RecPark():
    def __init__(self, recparkJsonData):
        self.type = 'rec_park'
        media = recparkJsonData['MEDIA']
        self.image_url = DEFAULT_RECPARK_IMAGE

        if (len(media)):
            self.image_url = media[0].get('URL', DEFAULT_RECPARK_IMAGE)

        self.name = recparkJsonData['RecAreaName']
        description = recparkJsonData['RecAreaDescription']
        self.description = DEFAULT_DESCRIPTION

        if(len(description)):
            self.description = description

        self.rec_gov_id = recparkJsonData['RecAreaID']
        self.id = f"{self.type}-{self.rec_gov_id}"
        self.directions = recparkJsonData['RecAreaDirections']
        if recparkJsonData.get('RECAREAADDRESS', []).__len__() > 0:
            self.city = recparkJsonData['RECAREAADDRESS'][0].get('City', None)
            self.state = recparkJsonData['RECAREAADDRESS'][0].get('AddressStateCode', None)
        else:
            self.city = None
            self.state = None
        self.latitude = recparkJsonData['RecAreaLatitude']
        self.longitude = recparkJsonData['RecAreaLongitude']

    
    def to_json(self, user=None):
        data = {
            'image_url': self.image_url,
            'name': self.name,
            'description': self.description,
            'rec_gov_id': self.rec_gov_id,
            'id': self.id,
            'directions': self.directions,
            'city': self.city,
            'state': self.state,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'has_liked': False,
            'type': 'campsite'
        }

        if user:
            data['has_liked'] = user.has_liked_site(self) is not None

        return data

def get_rec_parks(limit=1, offset=0, radius=15, latitude=0, longitude=0):
    params = {'apikey': API_KEY, 'limit': limit, 'offset': offset, 'full': True, 'latitude': latitude, 'longitude': longitude, 'radius': radius}
    response = requests.get('https://ridb.recreation.gov/api/v1/recareas', params=params)
    data = response.json()
    rec_parks = data['RECDATA']

    return [RecPark(d) for d in rec_parks]

