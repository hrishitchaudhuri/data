import requests
import urllib
import os

from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
  "ENTER_NEO4J_URL_HERE",
  auth=basic_auth("NEO4J_UNAME", "NEO4J_PASSWD"))

session = driver.session(database="DBNAME")

TWITTER_BEARER = "AUTH_TOKEN"

q = urllib.parse.quote_plus("bitcoin") #replace w appropriate query

count = 100
result_type = "recent"
lang = "en"
since_id = -1


url = "https://api.twitter.com/1.1/search/tweets.json?q=%s&count=%s&result_type=%s&lang=%s&since_id=%s" % (q, count, result_type, lang, since_id)
req = requests.get(url, headers = {"accept":"application/json","Authorization":"Bearer " + TWITTER_BEARER})

tweets = req.json()["statuses"]
print(tweets)

since_id = tweets[0].get('id')

query = """
UNWIND $tweets AS t
WITH t
ORDER BY t.id
WITH t,
	t.entities AS e,
        t.user AS u,
        t.retweeted_status AS retweet

MERGE (tweet:Tweet {id:t.id})
SET tweet.text = t.text,
	tweet.created_at = t.created_at,
        tweet.favorites = t.favorite_count

MERGE (user:User {screen_name:u.screen_name})
SET user.name = u.name,
       	user.location = u.location,
        user.followers = u.followers_count,
        user.following = u.friends_count,
       	user.statuses = u.statusus_count,
        user.profile_image_url = u.profile_image_url

MERGE (user)-[:POSTS]->(tweet)
MERGE (source:Source {name:t.source})
MERGE (tweet)-[:USING]->(source)

FOREACH (h IN e.hashtags |
	MERGE (tag:Hashtag {name:TOLOWER(h.text)})
       	MERGE (tag)-[:TAGS]->(tweet)
)

FOREACH (u IN e.urls |
   	MERGE (url:Link {url:u.expanded_url})
        MERGE (tweet)-[:CONTAINS]->(url)
)

FOREACH (m IN e.user_mentions |
      	MERGE (mentioned:User {screen_name:m.screen_name})
        ON CREATE SET mentioned.name = m.name
        MERGE (tweet)-[:MENTIONS]->(mentioned)
)

FOREACH (r IN [r IN [t.in_reply_to_status_id] WHERE r IS NOT NULL] |
     	MERGE (reply_tweet:Tweet {id:r})
        MERGE (tweet)-[:REPLY_TO]->(reply_tweet)
)

FOREACH (retweet_id IN [x IN [retweet.id] WHERE x IS NOT NULL] |
     	MERGE (retweet_tweet:Tweet {id:retweet_id})
        MERGE (tweet)-[:RETWEETS]->(retweet_tweet)
)
"""

session.run(query, {'tweets':tweets})
print("DONE")
