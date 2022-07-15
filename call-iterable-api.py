# Read email and location details and send to Iterable
# Could also pull the location details from standard mP location values
# but not done here since values are actually being pulled from internal systems
# and available as user_attributes
#

import http.client
import json

def lambda_handler(event_batch, context):

  user_email = get_email(event_batch['user_identities'])
  lat = get_lat(event_batch['user_attributes'])
  lon = get_lon(event_batch['user_attributes'])
  
  conn = http.client.HTTPSConnection("api.iterable.com")

  payload = json.dumps({
    "email": user_email,
    "preferUserId": True,
    "dataFields": {
      "source": "lambda",
      "last_geo_location": {
        "lat": lat, 
        "lon": lon
      }
    }
  })
  headers = {
    'api_key': '-- API KEY --',
    'Content-Type': 'application/json'
  }
  conn.request("POST", "/api/users/update", payload, headers)
  res = conn.getresponse()
  data = res.read()
  return event_batch

def get_email(user_id) -> str:
    user_email = user_id['email']
    return user_email

def get_lat(user_attr) -> float:
    lat = user_attr['last_latitude']
    return lat

def get_lon(user_attr) -> float:
    lon = user_attr['last_longitude']
    return lon
