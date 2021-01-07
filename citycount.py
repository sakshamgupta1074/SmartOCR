from geopy.geocoders import Nominatim

geolocator = Nominatim(timeout=3,user_agent="countrychecker")

def citycountname(cityname):
	'''
	Usage:
	INPUT: Name of Place
	OUTPUT: Cityname and country if input is city name else country name if input is country name
	'''

	location = geolocator.geocode(cityname,language='en')
	loc_dict = location.raw
	sub=','
	stateb=len(loc_dict['display_name'].rsplit(',')[0:-1])
	if stateb==1:
		return (' ',cityname,loc_dict['display_name'].rsplit(', ' , 1)[1])
	if stateb>1:
		return (cityname,loc_dict['display_name'].rsplit(', ')[-2],loc_dict['display_name'].rsplit(', ' , 1)[1])
	elif sub not in loc_dict['display_name']:
		return (' ',' ',loc_dict['display_name'].rsplit(',' , 1)[0])



print(citycountname('los angeles'))