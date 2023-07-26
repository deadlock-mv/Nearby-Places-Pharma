from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import googlemaps
from geopy.distance import distance
from datetime import datetime
from base1.models import StoreMaster, StoreCompetition
from base1.serializers import StoreCompetitionSerializer

gmaps = googlemaps.Client(key='AIzaSyCSqRLgFrxjKscyoXHc0LgYMmHr2LisbKU')


# this function returns the nearest Non-MedPlus pharmacy(Operational) for a particular lat and lang
def find_nearest_pharmacy(lat, lng):
    # Use the Google Maps API to search for pharmacies nearby
    places_result = gmaps.places_nearby(location=(lat, lng), radius=5000, type='pharmacy')

    # Find the nearest pharmacy based on distance from the starting point
    if places_result['status'] == 'OK':
        nearest_place = None
        nearest_distance = float('inf')

        # finding out the nearest
        for place in places_result['results']:
            place_latlng = (place['geometry']['location']['lat'], place['geometry']['location']['lng'])
            # gets the distance between two points
            dist = distance((lat, lng), place_latlng).meters

            # check for nearest as well its business status also it should be a Non-MedPlus store
            if dist < nearest_distance and (place['business_status'] in ['OPERATIONAL', 'CLOSED_TEMPORARILY']) \
                    and not ('MedPlus' in place['name'] or 'Medplus' in place['name']):
                nearest_distance = dist
                nearest_place = {
                    'competition_store_name': place['name'],
                    "competition_store_uid": place['place_id'],
                    "competition_store_type": 'pharmacy',
                    "competition_store_latitude": place['geometry']['location']['lat'],
                    "competition_store_longitude": place['geometry']['location']['lng'],
                    "competition_store_address": place['vicinity'],
                    "competition_store_distance": nearest_distance,
                    "competition_store_status": place['business_status'],
                    "year": datetime.now().year,
                    "week": datetime.now().isocalendar()[1],
                    "updated_date": datetime.now(),
                }
        if nearest_place:
            return nearest_place
        else:
            raise Exception("No Operational Non-MedPlus Store Nearby in a radius of 5000M")
    else:
        raise Exception("Pharmacies Not Found")


def post_nearby_stores(request):
    nearby_list = []
    medplus_stores = StoreMaster.objects.all()

    # getting nearest pharmacy for StoreMaster if no reference exists in StoreCompetition
    for store in medplus_stores:
        store_comp = StoreCompetition.objects.filter(store=store)
        if store_comp.exists():
            continue
        else:
            nearest_store = find_nearest_pharmacy(store.latitude, store.longitude)
            nearest_place = StoreCompetition(
                competition_store_name=nearest_store['competition_store_name'],
                competition_store_uid=nearest_store['competition_store_uid'],
                competition_store_type='pharmacy',
                competition_store_latitude=nearest_store["competition_store_latitude"],
                competition_store_longitude=nearest_store['competition_store_longitude'],
                competition_store_address=nearest_store['competition_store_address'],
                competition_store_distance=nearest_store['competition_store_distance'],
                competition_store_status=nearest_store['competition_store_status'],
                store=store,
                year=nearest_store['year'],
                week=nearest_store['week'],
                updated_date=nearest_store['updated_date'],
            )
            nearby_list.append(nearest_place)
    with transaction.atomic():
        StoreCompetition.objects.bulk_create(nearby_list)
    return get_nearby_store(request)


def update_nearby_store(request):
    medplus_stores = StoreMaster.objects.all()

    # for each store->if StoreCompetition exists, update nearest store-> update it in StoreCompetition table
    for store in medplus_stores:
        store_comp = StoreCompetition.objects.filter(store=store)
        if store_comp.exists():
            updated_nearest_store = find_nearest_pharmacy(store.latitude, store.longitude)
            store_comp.update(
                competition_store_name=updated_nearest_store['competition_store_name'],
                competition_store_uid=updated_nearest_store['competition_store_uid'],
                competition_store_type='pharmacy',
                competition_store_latitude=updated_nearest_store["competition_store_latitude"],
                competition_store_longitude=updated_nearest_store['competition_store_longitude'],
                competition_store_address=updated_nearest_store['competition_store_address'],
                competition_store_distance=updated_nearest_store['competition_store_distance'],
                competition_store_status=updated_nearest_store['competition_store_status'],
                year=updated_nearest_store['year'],
                week=updated_nearest_store['week'],
                updated_date=updated_nearest_store['updated_date'])

    return get_nearby_store(request)


def get_nearby_store(request):
    nearby_stores = StoreCompetition.objects.all()
    serializer = StoreCompetitionSerializer(nearby_stores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

