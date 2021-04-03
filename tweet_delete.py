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
    print("Copy and paste the link above in your browser and follow the steps below:\n\n\
          1. Login to your Twitter account.\n\
          2. Authorize access to your account.\n\
          3. Copy the 7 digit pin onto your clipboard.\n\
          4. Paste the PIN below and press Enter.")
        
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

def delete_tweets(api):
    """
        Delete User's Tweets as specified
            1. Ask user for a date parameter
            2. Print number of tweets older than date parameter
            3. Request confirmation from user for bulk deletion 
            4. Commence bulk deletion
            
        @param api: Tweepy API Object
    """
    
    def delete(tweet_list):
        delete_count = 0
        error_delete = []
        
        for tweet in tweet_list:
            try:
                api.destroy_status(tweet)
                delete_count+=1
            except:
                error_delete.append(tweet)
                
        return delete_count, error_delete
    
    print("\nWelcome to the bulk tweet deleter. This script will permanently delete your tweets equal to or older than a specified date.")
    date = input("Please enter your desired date and press enter (MM/DD/YYYY): ")
    print("\nProcessing...") 
    
    #Declare variables
    tweet_ids = []
    
    #Parse and format input date
    parsed_input = datetime.strptime(date + ' 23:59:59', '%m/%d/%Y %H:%M:%S')

    for tweet in tweepy.Cursor(api.user_timeline).items():
        try:
            #Perform comparison between tweet.created_at attribute and input date
            #print("{counter} || {tweet} || {created} || {inputDate}".format(counter=counter, tweet=tweet_count, created=tweet.created_at, inputDate=parsed_input))
            if tweet.created_at <= parsed_input:
                tweet_ids.append(tweet.id)
                
        except:
             print("Invalid date entry. Try again.")
             return
         
    #Handle edge case of 0 tweets older than specified date    
    if len(tweet_ids) != 0:
        print("\nThere are {count} tweets equal to or older than {date}. ".format(count=len(tweet_ids), date=date))
    else:
        print("\nThere are 0 tweets equal to or older than {}. ".format(date))
        return
    
    #Get confirmation from user for permanent deletion
    response = input("Are you sure you want to delete these tweets? (Y/N): ").upper().strip()
    
    #Multithread processing for deletion
    if response == 'Y':
        print("\nDeleting tweets...")
        try:
            tweet_ids = [tweet_ids]
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = executor.map(delete, tweet_ids)
                deleted = tuple(result)
                
        except ValueError as e:
            print(e)
        
    else:
        print("I get it, it's hard to let go of tweets. See you next time.")
        return
    
    print("\n{} tweets deleted.".format(deleted[0][0]))
    
    if len(deleted[0][1]) == 0:
        print("There were no errant deletes.")
    else:
        print("The following Tweet IDs were unable to be deleted:", deleted[0][1])
    
if __name__ == "__main__":
    api = login(c_key, c_secret)
    delete_tweets(api)
    

