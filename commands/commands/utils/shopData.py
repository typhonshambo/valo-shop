import json
import requests
from typing import Union

import riot_auth
from riot_auth import RiotAuth

#logger
from commands.ready.logging_config import setup_logging
logger = setup_logging()

#adding latest riot user agent
RiotAuth.RIOT_CLIENT_USER_AGENT = "RiotClient/86.0.1.1443.3366 %s (Windows;10;;Professional, x64)"

async def username_to_data(username, password):

	try:
		auth = riot_auth.RiotAuth()
		CREDS = username, password

		await auth.authorize(*CREDS)
		header = {
			"Authorization" : "Bearer " + auth.access_token
		}
		data = {
			"id_token": auth.id_token
		}
		
		r = requests.put(f"https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant", headers=header, json=data)
		data = r.json()
		region = data['affinities']['live']
		
		return [auth.access_token, auth.entitlements_token, auth.user_id, region]

	except Exception as e:
		logger.error(f"Failed to Auth : {e}")
		return None



def userBalance(entitlements_token, access_token, user_id, region):
	try:
		headers = {

			'X-Riot-Entitlements-JWT': entitlements_token,
			'Authorization': f'Bearer {access_token}',
			'X-Riot-ClientVersion': getVersion(),
			"X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
		}

		r = requests.get(f'https://pd.{region}.a.pvp.net/store/v1/wallet/{user_id}', headers=headers)

		balance_data = json.loads(r.text)

		vp = balance_data["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"]
		rp = balance_data["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"]
		
		return [vp, rp]

	except Exception as e:
		logger.error(f"Failed to get user balance PUUID : {user_id}: {e}")
		return None


def getVersion():
	try:
		versionData = requests.get("https://valorant-api.com/v1/version")
		versionDataJson = versionData.json()['data']
		final = f"{versionDataJson['branch']}-shipping-{versionDataJson['buildVersion']}-{versionDataJson['version'][-6:]}"
		return final
	except Exception as e:
		logger.error(f"Failed to get version : {e}")
		return None
	


def skin_auth(
		entitlements_token:str, 
		access_token:str, 
		user_id:str, 
		region:str
	)->Union[dict, None]:
	'''
	Get the skin data from the valorant API
	Args:
		entitlements_token : str : User entitlements token
		access_token : str : User access token
		user_id : str : User ID
		region : str : User region
	
	Returns:
		skins_data : json : Skin data from the valorant API
	'''
	try:
		headers = {
			'X-Riot-Entitlements-JWT': entitlements_token,
			'Authorization': f'Bearer {access_token}',
			'X-Riot-ClientVersion': getVersion(),
			'X-Riot-ClientPlatform' : 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
		}
		r = requests.get(f'https://pd.{region}.a.pvp.net/store/v2/storefront/{user_id}', headers=headers)
		skins_data = json.loads(r.text)

		logger.info(f"Skin auth success! : {user_id}")
		return skins_data
	except Exception as e:
		logger.error(f"Failed to get skin auth : {e}")
		return None
	

def skin_bundle_data(
		skin_data:dict
) -> Union[dict, None]:
	'''
	Parse the skin data and provide the bundle data
	Args:
		skin_data : dict : Skin data from the valorant API
	Returns:
		bundle_data : dict : A dictionary containing the bundle details
	EXAMPLE:
	{
		"bundle_name": "Bundle Name",
		"bundle_image": "Bundle Image",
		"bundle_price": "Bundle Price"
	}
	'''
	try:
		rowID = skin_data["FeaturedBundle"]["Bundle"]["DataAssetID"]
		r_bundle_data = requests.get(f"https://valorant-api.com/v1/bundles/{rowID}")
		bundle_data = r_bundle_data.json()
		bundle_name = bundle_data['data']['displayName']
		bundle_image = bundle_data['data']['displayIcon']
		logger.info('Bundle fetch data success!')
		return {
			"bundle_name": bundle_name,
			"bundle_image": bundle_image,
			"bundle_price": skin_data['FeaturedBundle']['Bundles'][0]['TotalDiscountedCost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
		}
	except Exception as e:
		logger.error(f"Failed to get bundle data : {e}")
		return None

def skin_list_price(skin_data:dict) -> Union[list | None]:
	'''
	Parse the skin data and provide the skin id and prices available in the StoreFront
	Args:
		skin_data : dict : Skin data from the valorant API
	Returns:
		skin_panel: list | None : A list containing the skin details else None
		EXAMPLE:
		[
			{
				"skin_id": "Skin ID",
				"skin_price": "Skin price",
			}
		]
	'''
	try:
		skin_panel = []
		for items in skin_data['SkinsPanelLayout']['SingleItemStoreOffers']:
			skin_data = {
				"skin_id": items['OfferID'],
				"skin_price": items['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
			}
			skin_panel.append(skin_data)
		logger.info('Skin list and price fetch success!')
		return skin_panel
	except Exception as e:
		logger.error(f"Failed to get skin list and price : {e}")
		return None


def skinid_to_data(
	skinids:list
)-> Union[list | None]:
	'''
	Provides skin datas like displayIcon, Price, Name from skinID
	Args: 
		skinid : UUIDs and prices of skin
		EXAMPLE:
		[
			{
				"skin_id": "Skin id",
				"skin_price": "Skin price",
			}
		]
	Returns:
		skin_data : list : A list containing the skin details
		EXAMPLE:
		[
			{
				"skin_name": "Skin Name",
				"skin_image": "Skin Image",
				"skin_price": "Skin Price"
			},
		]
			
	'''
	skin_data = []
	try:
		for uuid in skinids:
			r = requests.get(f"https://valorant-api.com/v1/weapons/skinlevels/{uuid['skin_id']}")
			parsed_data = r.json()
			skin_details = {
				"skin_name": parsed_data["data"]["displayName"],
				"skin_image": parsed_data["data"]["displayIcon"],
				"skin_price": uuid["skin_price"]
			}
			skin_data.append(skin_details)
		logger.info('Skinid to data fetch success!')
		return skin_data
	except Exception as e:
		logger.error(f"Failed to get skin data : {e}")
		return None



def skins(
	entitlements_token:str,
	access_token:str,
	user_id:str,
	region:str
)-> Union[dict, None]:
	'''
	Provides the skin data in a dictionary format
	Args:
		entitlements_token : str : User entitlements token
		access_token : str : User access token
		user_id : str : User ID
		region : str : User region
	Returns:
		skins_view : dict : A dictionary containing the skin details
		EXAMPLE:
		{
			"bundle_name": "Bundle Name",
			"bundle_image": "Bundle Image",
			"bundle_price": "Bundle Price",
			"skin1_name": "Skin Name",
			"skin1_image": "Skin Image",
			"skin1_price": "Skin Price",
			"skin2_name": "Skin Name",
			"skin2_image": "Skin Image",
			"skin2_price": "Skin Price",
			"skin3_name": "Skin Name",
			"skin3_image": "Skin Image",
			"skin3_price": "Skin Price",
			"skin4_name": "Skin Name",
			"skin4_image": "Skin Image",
			"skin4_price": "Skin Price",
			"SingleItemOffersRemainingDurationInSeconds": "Time Remaining",
			"time_units": "Time Units"
		}
	'''

	
	auth_data = skin_auth(entitlements_token, access_token, user_id, region)
	bundle_data = skin_bundle_data(auth_data)
	skin_list = skin_list_price(auth_data)
	skin_data = skinid_to_data(skin_list)


	try:
		daily_reset = auth_data["SkinsPanelLayout"]["SingleItemOffersRemainingDurationInSeconds"]

		if daily_reset >= 3600:
			daily_reset_in_ = round(daily_reset / 3600, 0) 
			time_unit = "Hrs"
		
		else:
			daily_reset_in_ = round(daily_reset / 60, 2) 
			time_unit = "Mins"
	except Exception as e:
		logger.error('Failed to get daily reset time : {e}')
	
	try:
		skin_view = {
			"bundle_name": bundle_data['bundle_name'],
			"bundle_image": bundle_data['bundle_image'],
			"bundle_price": bundle_data['bundle_price'],

			"skin1_name": skin_data[0]['skin_name'],
			"skin1_image":skin_data[0]['skin_image'],
			"skin1_price":skin_data[0]['skin_price'],

			"skin2_name": skin_data[1]['skin_name'],
			"skin2_image":skin_data[1]['skin_image'],
			"skin2_price":skin_data[1]['skin_price'],

			"skin3_name": skin_data[2]['skin_name'],
			"skin3_image":skin_data[2]['skin_image'],
			"skin3_price":skin_data[2]['skin_price'],

			"skin4_name": skin_data[3]['skin_name'],
			"skin4_image":skin_data[3]['skin_image'],
			"skin4_price":skin_data[3]['skin_price'],

			"SingleItemOffersRemainingDurationInSeconds": daily_reset_in_,
			"time_units":time_unit
		}
	except Exception as e:
		logger.error(f"Failed to get skin view : {e}")
		skin_view = None
	

	return skin_view




async def check_item_shop(username, password):
	user_data = await username_to_data(username, password)
	access_token = user_data[0]
	entitlements_token = user_data[1]
	user_id = user_data[2]
	skin_data = skins(entitlements_token, access_token, user_id)
	skin_list = [skin_data["skin1_name"], skin_data["skin2_name"], skin_data["skin3_name"], skin_data["skin4_name"], skin_data["SingleItemOffersRemainingDurationInSeconds"]]
	return skin_list