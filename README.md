# TweetDelete
This script deletes tweets equal to or older than a user inputted date.

## Dependencies

```
pip install tweepy
tweepy.__version__ = 3.10.0
```

## Setup

After installing tweepy, you will have to create an app through Twitter Developer to acquire the consumer key and consumer secret key. The approval process for app development is relatively quick, it should take you no longer than the time it takes to submit the approval application. 

## OAuth Process via Unique PIN

I intentionally developed the login function to go through the authentication process via a unique PIN to test third-party login functionality of the Twitter API. 

In this method, the user is given an authentication link to authorize the app's functionality on their personal account. When visiting the authentication link, the user is prompted to authorize access to their account via the Tweet Delete app. Once authorized, the user is presented with a unique pin that allows the app to access their account. 

## Example Console Output

### Before:

https://github.com/bijoyt3/TweetDelete/blob/main/assets/After.jpg?raw=true

### Execution:

```
https://api.twitter.com/oauth/authorize?oauth_token=[OAUTH TOKEN]

Copy and paste the link above in your browser and follow the steps below.
1. Login to your account
2. Allow access to the app
3. Copy the 7 digit pin onto clipboard
4. Paste the PIN below and press enter

PIN: [OAUTH PIN]
Successfully logged in as: @[SCREEN NAME]

Welcome to the bulk tweet deleter. This script will permanently delete your tweets equal to or older than a specified date.

Please enter your desired date and press enter (MM/DD/YYYY): 01/14/2020

Processing...

There are 50 tweets equal to or older than 01/14/2020. 

Are you sure you want to delete these tweets? (Y/N): Y

Deleting tweets...

50 tweets deleted.
```
### After:

![After]("https://github.com/bijoyt3/TweetDelete/blob/main/assets/Before.jpg?raw=true")

## Acknowledgements
Spent quite some time on the tweepy documentation page (https://docs.tweepy.org/en/latest/) and StackOverflow

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
