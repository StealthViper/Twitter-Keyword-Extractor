from flask import Flask, json, request, render_template
import tweepy
from rake_nltk import Rake

r = Rake()

app = Flask(__name__)
# Load our config from an object, or module (config.py)
app.config.from_object('config')

ckey="btd3eVabgd5WQIvn74ocBNpCH"
csecret="iej1Eg8d8YgB5WHNsQON0ylAaDIL999dcXqgS5Pkfk3YwTbkVo"
atoken="1237299604489515008-nIfT9GYOpmglUwci9g29mcmMC4ytLS"
asecret="KirjyytOYk43t9hzU1YGhR63YcIhOFkXn4TJVXGqpZbdC"

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
tweepy_api = tweepy.API(auth)


@app.route('/')
def hello_world():
    return "<h1>Hello World</h1>"


@app.route('/tweets_harvester/<string:username>')
def tweets(username):
    # 'tweets' is passed as a keyword-arg (**kwargs)
    # **kwargs are bound to the 'tweets.html' Jinja Template context
    return render_template("tweets.html", tweets=get_tweets(username))

def get_tweets(username):
    tweets = tweepy_api.user_timeline(screen_name=username)

    result_list = []
    for t in tweets:
        a = r.extract_keywords_from_text(t.text)
        b = r.get_ranked_phrases()
        c = listToString(b)
        result_list.append(
            {'tweet': t.text,
             'created_at': t.created_at,
             'username': username,
             'headshot_url': t.user.profile_image_url,
             'keywords': c
             }
        )

    return result_list


def listToString(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))








