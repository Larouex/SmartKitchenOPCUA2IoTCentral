import json

data = '{"forecastDate": "2020-09-25", "weather": "Showers", "morning": [{"8am": 45}, {"9am": 46}]}'

data_dict = json.loads(data)

print(data_dict['weather'])
print(data_dict["morning"][0])