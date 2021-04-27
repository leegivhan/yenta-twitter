import configparser
from tweepy import API, Cursor, OAuthHandler, TweepError

# Read in configs
configs = configparser.ConfigParser()
configs.read('./config.ini')
keys = configs['TWITTER']
consumer_key = keys['CONSUMER_KEY']
consumer_secret = keys['CONSUMER_SECRET']
access_token = keys['ACCESS_TOKEN']
access_secret = keys['ACCESS_SECRET']
screen_name = keys['SCREEN_NAME']

# Authenticate Tweepy connection with Twitter API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Get Twitter ID for each follower
ids = []
for fid in Cursor(api.followers_ids, screen_name=screen_name, count=5000).items():
    ids.append(fid)

# print(ids)

# Get more details for each follower
info = []
for i in range(0, len(ids), 100):
    try:
        chunk = ids[i:i+100]
        info.extend(api.lookup_users(user_ids=chunk))
    except:
        import traceback
        traceback.print_exc()
        print('Something went wrong, skipping...')

# Process data to usable csv file format
import pandas as pd

data = [x._json for x in info]
df = pd.DataFrame(data)
df = df[['id', 'name', 'screen_name', 'location', 'description', 'url', 'followers_count', 'friends_count', 'created_at', 'verified']]
df.to_csv('followers.csv', index=False)
