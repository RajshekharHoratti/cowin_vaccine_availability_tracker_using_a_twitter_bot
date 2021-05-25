import os
import time
import tweepy
import requests
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
dotenv_path = BASE_DIR + '/../../.env'
load_dotenv(dotenv_path)

current_date = datetime.today().strftime('%d-%m-%Y')
district_id_bbmp = 294 # BBMP


def twitter_bot(pincode,avaliable_date):
    auth = tweepy.OAuthHandler(os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_KEY_SECRET"))
    auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth)
    message = f"Vaccine Avaliable at Pincode: {pincode} on {avaliable_date}"
    api.update_status(message)


def cowin_api_bbmp():
    #NOTE: Cowin api can be called 100 times for every 5mins
    browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36','Cache-Control': 'no-cache'}
    response = requests.get(url=f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id={district_id_bbmp}&date={current_date}", headers=browser_header)
    print("COWIN API RESPONSE STATUS CODE:", response.status_code)
    if response.status_code == 200:
        center_list = response.json()
        for center in center_list['centers']:
            for item in center['sessions']:
                #NOTE: Change the min_age_limit to 45 or 18 as per your need
                if item['min_age_limit'] == 18:
                    pincode = center['pincode']
                    avaliable_date = item['date']
                    # TWITTER BOT
                    twitter_bot(pincode, avaliable_date)
    else:
        print("COWIN API ERROR", response.status_code)


while True:
    # Calling api every 1.5 seconds
    cowin_api_bbmp()
    time.sleep(1.5)