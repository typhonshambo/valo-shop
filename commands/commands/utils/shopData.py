import json
import requests
import re
from collections import OrderedDict
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import ssl
import socket

requests.packages.urllib3.disable_warnings()

def username_to_data(username, password):

		# More on the topic: https://stackoverflow.com/questions/62684468/pythons-requests-triggers-cloudflares-security-while-urllib-does-not

		# grab the address using socket.getaddrinfo
		answers = socket.getaddrinfo('auth.riotgames.com', 443)
		(family, type, proto, canonname, (address, port)) = answers[0]

		headers = OrderedDict({
			'Accept-Encoding': 'gzip, deflate, br',
			'Host': "auth.riotgames.com",
			'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)'
		})

		session = requests.session()
		session.headers = headers

		data = {
			'client_id': 'play-valorant-web-prod',
			'nonce': '1',
			'redirect_uri': 'https://playvalorant.com/opt_in',
			'response_type': 'token id_token',
		}
		r = session.post(f'https://{address}/api/v1/authorization', json=data, headers=headers, verify=False)

		
		data = {
			'type': 'auth',
			'username': username,
			'password': password
		}
		r = session.put(f'https://{address}/api/v1/authorization', json=data, headers=headers, verify=False)
		pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
		data = pattern.findall(r.json()['response']['parameters']['uri'])[0] 
		access_token = data[0]
		

		headers = {
			'Accept-Encoding': 'gzip, deflate, br',
			'Host': "entitlements.auth.riotgames.com",
			'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
			'Authorization': f'Bearer {access_token}',
		}
		r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
		entitlements_token = r.json()['entitlements_token']
		# print('Entitlements Token: ' + entitlements_token)

		headers = {
			'Accept-Encoding': 'gzip, deflate, br',
			'Host': "auth.riotgames.com",
			'User-Agent': 'RiotClient/43.0.1.4195386.4190634 rso-auth (Windows;10;;Professional, x64)',
			'Authorization': f'Bearer {access_token}',
		}

		r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
		user_id = r.json()['sub']
		# print('User ID: ' + user_id)
		headers['X-Riot-Entitlements-JWT'] = entitlements_token
		del headers['Host']
		session.close()

		return [access_token, entitlements_token, user_id]


def getVersion():
	versionData = requests.get("https://valorant-api.com/v1/version")
	versionDataJson = versionData.json()['data']
	final = f"{versionDataJson['branch']}-shipping-{versionDataJson['buildVersion']}-{versionDataJson['version'][-6:]}"
	return final

def priceconvert(skinUuid, offers_data):
	for row in offers_data["Offers"]:
		if row["OfferID"] == skinUuid:
			for cost in row["Cost"]:
				return row["Cost"][cost]
	

def skins(entitlements_token, access_token, user_id, region):

	headers = {
		'X-Riot-Entitlements-JWT': entitlements_token,
		'Authorization': f'Bearer {access_token}',
	}

	r = requests.get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{user_id}', headers=headers)

	skins_data = json.loads(r.text)

	single_skins = skins_data['SkinsPanelLayout']["SingleItemOffers"]


	headers = {
		'X-Riot-Entitlements-JWT': entitlements_token,
		'Authorization': f'Bearer {access_token}',
		'X-Riot-ClientVersion': getVersion(),
		"X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
	}

	r = requests.get(f'https://api.henrikdev.xyz/valorant/v1/content')

	content_data = r.json()
	



	single_skins_images = []
	single_skins_tiers_uuids = []
	single_skins_name = []


 

	for skin in single_skins:
		
		r = requests.get(f"https://valorant-api.com/v1/weapons/skinlevels/{skin}")
		parsed_data = r.json()
		single_skins_images.append(parsed_data["data"]["displayIcon"])
		single_skins_tiers_uuids.append(parsed_data["data"]["uuid"])
		single_skins_name.append(parsed_data["data"]["displayName"])

	

	headers = {
		'X-Riot-Entitlements-JWT': entitlements_token,
		'Authorization': f'Bearer {access_token}',
		'X-Riot-ClientVersion': getVersion(),
		"X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
	}

	data = requests.get(f"https://pd.{region}.a.pvp.net/store/v1/offers/", headers=headers)

	offers_data = data.json()
	


	rowID = skins_data["FeaturedBundle"]["Bundle"]["DataAssetID"]
	r_bundle_data = requests.get(f"https://valorant-api.com/v1/bundles/{rowID}")
	bundle_data = r_bundle_data.json()
	
	
	bundle_name = bundle_data['data']['displayName']
	try:
		bundle_image = bundle_data['data']['displayIcon']
	except KeyError:
		bundle_image = "https://notyetinvalorant-api.com"

	daily_reset = skins_data["SkinsPanelLayout"]["SingleItemOffersRemainingDurationInSeconds"]

	skin_counter = 0


	for skin in single_skins:

		if skin_counter == 0:
			skin1_name = single_skins_name[skin_counter]
			skin1_image = single_skins_images[skin_counter]
			skin1_price = priceconvert(skin, offers_data)
		elif skin_counter == 1:
			skin2_name = single_skins_name[skin_counter]
			skin2_image = single_skins_images[skin_counter]
			skin2_price = priceconvert(skin, offers_data)
		elif skin_counter == 2:
			skin3_name = single_skins_name[skin_counter]
			skin3_image = single_skins_images[skin_counter]
			skin3_price = priceconvert(skin, offers_data)
		elif skin_counter == 3:
			skin4_name = single_skins_name[skin_counter]
			skin4_image = single_skins_images[skin_counter]
			skin4_price = priceconvert(skin, offers_data)
		skin_counter += 1

	if daily_reset >= 3600:
		daily_reset_in_ = round(daily_reset / 3600, 0) 
		time_unit = "Hrs"
	 
	else:
		daily_reset_in_ = round(daily_reset / 60, 2) 
		time_unit = "Mins"
		
	skins_list = {
		"bundle_name": bundle_name,
		"bundle_image": bundle_image,
		"skin1_name": skin1_name,
		"skin1_image":skin1_image,
		"skin1_price":skin1_price,
		"skin2_name": skin2_name,
		"skin2_image": skin2_image,
		"skin2_price": skin2_price,
		"skin3_name": skin3_name,
		"skin3_image": skin3_image,
		"skin3_price": skin3_price,
		"skin4_name": skin4_name,
		"skin4_image": skin4_image,
		"skin4_price": skin4_price,
		"SingleItemOffersRemainingDurationInSeconds": daily_reset_in_,
		"time_units":time_unit
	}

	return skins_list



def check_item_shop(username, password):
	user_data = username_to_data(username, password)
	access_token = user_data[0]
	entitlements_token = user_data[1]
	user_id = user_data[2]
	skin_data = skins(entitlements_token, access_token, user_id)
	skin_list = [skin_data["skin1_name"], skin_data["skin2_name"], skin_data["skin3_name"], skin_data["skin4_name"], skin_data["SingleItemOffersRemainingDurationInSeconds"]]
	return skin_list
