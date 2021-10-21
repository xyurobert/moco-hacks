from flask import Flask, render_template, redirect, url_for
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_cors import CORS, cross_origin
from profanityFilter import getAllTweets, getProfaneTweets, tweetsToHTML, deleteAllTweets

app = Flask(__name__)
CORS(app)
app.secret_key = "supersekrit"
blueprint = make_twitter_blueprint(
    api_key="(removed)",
    api_secret="(removed)",
    redirect_url="/tweets"
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route('/front')
def render_front_page():
    return render_template("front.html")

@app.route('/tweets')
def render_tweets_page():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    
    response = twitter.get("account/settings.json")
    username = response.json()["screen_name"]

    tweets = getProfaneTweets(username)
    # sampleString = tweetsToHTML(tweets)

    # return str(tweets)

    return render_template("tweets.html", profaneTweets=tweets)

@app.route('/get-tweets/<username>')
def get_tweets(username):
    tweets = gatherTweets(username)
    #return render_template("tweets.html", tweets=tweets, username=username)
    return str(tweets)

@app.route('/delete-all')
@cross_origin()
def delete_all():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    
    response = twitter.get("account/settings.json")
    username = response.json()["screen_name"]

    tweets = getProfaneTweets(username)
    tweetIDs = []
    for tweet in tweets:
        tweetIDs.append(tweet['id'])

    deleteAllTweets(tweetIDs)
    return 'Deleted Profane Tweets'

@app.route('/delete-tweet/<int:tweet_id>')
def delete_tweet(tweet_id):
    deleteSingleTweet(tweet_id)
    return 'Deleted Profane Tweets'


if __name__ == '__main__':
    app.run()
