from rest_framework.views import APIView
from rest_framework.response import Response
from base1.manager import post_nearby_stores, update_nearby_store, get_nearby_store


class NearestComp(APIView):
    @staticmethod
    def get(request):
        try:
            return get_nearby_store(request)
        except Exception as err:
            error = str(err)
            return Response(error)

    @staticmethod
    def post(request):
        try:
            return post_nearby_stores(request)
        except Exception as err:
            error = str(err)
            return Response(error)

    @staticmethod
    def put(request):
        try:
            return update_nearby_store(request)
        except Exception as err:
            error = str(err)
            return Response(error)
