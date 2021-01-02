from geopy.geocoders import Nominatim

geolocator = Nominatim(timeout=3,user_agent="Shivasapp")

def citycountname(cityname):
	'''
	Usage:
	INPUT: Name of Place
	OUTPUT: Cityname and country if input is city name else country name if input is country name
	'''

	location = geolocator.geocode(cityname,language='en')
	loc_dict = location.raw
	sub=','
	if sub in loc_dict['display_name']:
		return (cityname,loc_dict['display_name'].rsplit(', ' , 1)[1])
	else:
		return (loc_dict['display_name'].rsplit(',' , 1)[0])





print(citycountname('Rohtak'))
