# TweetDelete
This script deletes tweets equal to or older than a user inputted date.

## Dependencies

tweepy 3.10.0

```
pip install tweepy
```

## Example Console Output

### Before:

![Before]("https://user-images.githubusercontent.com/7709854/110645790-48160180-8184-11eb-86e7-5f901f79c56f.png")

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

There are 84 tweets equal to or older than 01/14/2020. 

Are you sure you want to delete these tweets? (Y/N): Y

Deleting tweets...

84 tweets deleted.
```
### After:

![After]("https://user-images.githubusercontent.com/7709854/110645790-48160180-8184-11eb-86e7-5f901f79c56f.png")

## Acknowledgements
Spent quite some time on the tweepy documentation page (https://docs.tweepy.org/en/latest/) and StackOverflow

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
