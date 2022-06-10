from ninja import NinjaAPI
from requests import request

api = NinjaAPI()

@api.get('/test')
def test(request):
    return {'test': 'success'}
