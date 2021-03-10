#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 16:02:27 2021

@author: bijoythomas
"""

import tweepy 
import config as cfg
from datetime import datetime
import concurrent.futures

c_key = cfg.twitter_keys["consumer_key"]
c_secret = cfg.twitter_keys["consumer_secret"]


def login(c_key, c_secret):
    """
        Login to User's Account
            1. Create Auth Object
            2. Manually Retrieve Unique Pin via Authorization URL
            3. Get Access Token
            4. Authenticate Access Token
            5. Print confirmation of login 
        
        @param c_key: consumer key from Twitter Developer
        @param c_secret: consumer secret key from Twitter Developer
        @return "logged in" Tweepy API object
    """

    #Create auth object with consumer key and consumer secret key
    auth = tweepy.OAuthHandler(c_key, c_secret, callback='oob')
    
    #Manually Retrieve Unique Pin via Authorization URL
    auth_url = auth.get_authorization_url()
    print(auth_url)
    print()
    print("Copy and paste the link above in your browser and follow the steps below.")
    print("1. Login to your account")
    print("2. Allow access to the app")
    print("3. Copy the 7 digit pin onto clipboard")
    print("4. Paste the PIN below and press enter")
        
    #Get Access Token
    pin = input('PIN: ').strip()
    auth.get_access_token(pin)
    
    #Authenticate Access Token
    try:
        auth.set_access_token(auth.access_token, auth.access_token_secret)
    except:
        print("Login failed. Try again.")
        
    #Print confirmation of login
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    print("Successfully logged in as: @{}".format(api.me().screen_name))
    
    return api

        
def thread_delete(api_connect, tweet_delete_list):
    """
        Perform 'destroy_status' (aka Delete Tweet) method via multithreading
        
        @param api_connect: Tweepy API Object
        @param tweet_delete_list: List of Tweet IDs to be deleted
    """
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(api_connect.destroy_status, tweet_delete_list)
            
    except ValueError as e:
        print("Error processing tweets: {}".format(e))
        
    
def delete_tweets(api):
    """
        Delete User's Tweets as specified
            1. Ask user for a date parameter
            2. Print number of tweets older than date parameter
            3. Request confirmation from user for bulk deletion 
            4. Commence bulk deletion
            
        @param api: Tweepy API Object
    """
    
    print("\nWelcome to the bulk tweet deleter. This script will permanently delete your tweets equal to or older than a specified date.")
    date = input("Please enter your desired date and press enter (MM/DD/YYYY): ")
    print("Processing...") 
    
    #Declare variables 
    tweet_count = 0
    tweet_ids = []
    
    #Parse and format input date
    parsed_input_date = datetime.strptime(date, '%m/%d/%Y')
    input_date = datetime.strftime(parsed_input_date, '%m/%d/%Y')

    for tweet in tweepy.Cursor(api.user_timeline).items():
        try:
            #Parse and format tweet dates
            parsed_tweet_date = datetime.strptime(str(tweet.created_at),'%Y-%m-%d %H:%M:%S') 
            tweet_date = datetime.strftime(parsed_tweet_date, '%m/%d/%Y')

            if tweet_date <= input_date:
                tweet_count +=1
                tweet_ids.append(tweet.id)
        except:
             print("Invalid date entry. Try again.")
             return
         
    #Handle edge case of 0 tweets older than specified date    
    if len(tweet_ids) != 0:
        print("There are {count} tweets equal to or older than {date}. ".format(count=tweet_count, date=date))
    else:
        print("There are 0 tweets equal to or older than {}. ".format(date))
        return
    
    #Get confirmation from user for permanent deletion
    response = input("Are you sure you want to delete these tweets? (Y/N): ").upper().strip()
    
    if response == 'Y':
        print("\nDeleting tweets...")
        thread_delete(api, tweet_ids)
    else:
        print("I get it, it's hard to let go of tweets. See you next time.")
        return
            
    print("\n{} tweets deleted.".format(tweet_count))
    

if __name__ == "__main__":
    api = login(c_key, c_secret)
    delete_tweets(api)
    