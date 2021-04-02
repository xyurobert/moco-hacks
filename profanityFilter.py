from typing import List
from imageRec import imageIsProfane
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter


import tweepy
# Glenn's API Key (do not change)
consumer_key = 'byEBbmGLc4scB59ZoG4Lszzc0'
consumer_secret = '271bxFZc4CFU7HRVYsCfQT7q4UfodM4eA20co9lDVY2hvCfNzp'
# Access Token is specific to the account you're controlling

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)
###########################################################  API STUFF ABOVE ###########################################################################

# Number of Tweets
number_of_tweets = 2 #to delete all tweets, number_of_tweets = number of tweets flagged

# Create Set of All Profs
prof = open(r"curse.txt","r+")
profList = prof.readlines()
profSet = set()

for profWord in profList:
    profSet.add(profWord.strip())

# Create List of All Profane Tweets
#for single in tweepy.Cursor(api.user_timeline).items(1):
    #numberOfTweets  = int(single._json['statuses_count'])

def deleteProfaneTweets():
    # go through X number of tweets
    number_of_tweets = 10 #to delete all tweets, number_of_tweets = number of tweets flagged
    for status in tweepy.Cursor(api.user_timeline).items(number_of_tweets):
        
        #print('Tweet: ', status._json['text'])
        tweet = status._json
        tweet_id = tweet['id']
        tweet_text = tweet['text']
        #print('ID:', tweet_id)
        #print('TEXT:', tweet_text)
        tweetWords = tweet_text.split() #List of words seperated by space into list
        
        for curr_Word in tweetWords:
            if curr_Word in profSet:
                # print("flag: ", curr_Word)
                profaneTweets.append(tweet_id)
                api.destroy_status(tweet_id)
                #URL = "https://twitter.com/" + status._json['screen_name'] + "/" + status._json['id']
 
def textIsProfane(text) -> bool:
    tweetWords = text.split()
    for curr_Word in tweetWords:
        if curr_Word in profSet:
            if 'RT' != tweetWords[0]: 
                return True
    return False

def getProfaneTweets(username):
    # go through X number of tweets
    profaneTweets = []
    tweets = getAllTweets(username)
    for tweet in tweets:
        badText = textIsProfane(tweet['text'])
        badImage = tweet['image'] != None and imageIsProfane(tweet['image'])
        if badText or badImage:
            profaneTweets.append(tweet)
    return profaneTweets

# id, text, name, username, postDate, image
def getAllTweets(username: str):
    # Lists of all Parameter
    tweetInfoList = []
    # text, name, usernames, urls, postDates, images
    statuses = twitter.get(f'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={username}')

    print(len(statuses.json()))
    for tweet_response in statuses.json():
        tweetInfo = {}
        tweetInfo['id'] = tweet_response['id']
        tweetInfo['text'] = tweet_response['text']
        if ('media' in tweet_response['entities']):
            tweetInfo['image'] = tweet_response['entities']['media'][0]['media_url']
        else:
            tweetInfo['image'] = None
        tweetInfo['name'] = tweet_response['user']['name']
        tweetInfo['username'] = tweet_response['user']['screen_name']

        rawDate = tweet_response['created_at']
        dateSplit = rawDate.split()
        outputDate = dateSplit[1] + " " + dateSplit[2] + ", " + dateSplit[5]

        tweetInfo['postDate'] = outputDate
        tweetInfoList.append(tweetInfo)
        # print(tweetInfo['text'])
    return tweetInfoList
        

# curr_id = 1373397978447286274
def deleteSingleTweet(curr_id: int):
    #The ID of tweet selected by the user (Still need to find a way to retrieve the ID of the selected Tweet)
    api.destroy_status(curr_id)

def deleteAllTweets(tweetIDs):
    for tweet_id in tweetIDs:
        response = twitter.post('https://api.twitter.com/1.1/statuses/destroy/' + str(tweet_id) + '.json')
        print(response.text)
    
# example = giveTweetsInfo('glennren')
# print(example)

# id, text, name, username, postDate, image
def tweetsToHTML(profaneTweets):
    html_str = ''
    for tweet in profaneTweets:

        html_str += '<li>' + tweet['text'] + '</li>'
    return html_str
