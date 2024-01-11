import json
import requests
import re
from collections import OrderedDict
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager
import ssl
import socket

#importing RIOT_AUTO BY FLOXAY 
#pip install git+https://github.com/floxay/python-riot-auth.git
from riot_auth import RiotAuth
import asyncio
import sys

#adding latest riot user agent
RiotAuth.RIOT_CLIENT_USER_AGENT = "RiotClient/77.0.1.814.2013 %s (Windows;10;;Professional, x64)"

async def username_to_data(username, password):
  
	auth = riot_auth.RiotAuth()
	CREDS = username, password

	await auth.authorize(*CREDS)
	r = requests.get(f"https://api.henrikdev.xyz/valorant/v1/by-puuid/account/{auth.user_id}")
	data = r.json()
	region = data["data"]["region"]
	
	return [auth.access_token, auth.entitlements_token, auth.user_id, region]

def userBalance(entitlements_token, access_token, user_id, region):
	headers = {
		'X-Riot-Entitlements-JWT': entitlements_token,
		'Authorization': f'Bearer {access_token}',
	}

	r = requests.get(f'https://pd.{region}.a.pvp.net/store/v1/wallet/{user_id}', headers=headers)

	balance_data = json.loads(r.text)

	vp = balance_data["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
	rp = balance_data["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]
	
	return [vp, rp]


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
