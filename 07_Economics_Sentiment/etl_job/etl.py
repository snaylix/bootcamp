'''
1. Extract data from MongoDB
- Connect to the database
- Query the data

2. Transform the data
- Sentiment Analysis (will see this in the afternoon)
- Possibly we could transform datatypes

3. Load it into Postgres
- Connect to postgres
- Insert Into postgres
'''

import time
import logging

from pymongo import MongoClient
from sqlalchemy import create_engine
import psycopg2

### Create connection to mongodb
# We want to talk to the database inside the mongodb container
# host is the name of the container
# port is the port inside the container
client = MongoClient(host='mongodb', port=27017)
# we want to connect to the twitter database
db_mongo = client.twitter
# connect to the tweets collection
tweets = db_mongo.tweets


### Create connection to postgresdb
# hostname : name of the other container!
db_pg = create_engine('postgres://postgres:xxxx@postgresdb:5432/postgres', echo=True)
#                   DB type    user     psw  host       port dbname


create_table = """
                CREATE TABLE IF NOT EXISTS tweets (
                user_name TEXT,
                text TEXT,
                sentiment NUMERIC
                );
               """

db_pg.execute(create_table)

def extract():
    '''Extracts tweets from the MongoDB database'''
    # Pull the tweets out of the mongodb database with .find()
    # you can filter the data in your query .find({condition})
    extracted_tweets = list(tweets.find())
    # extracted_tweets is a list of dictionaries
    return extracted_tweets

def transform(extracted_tweets):
    '''Transforms the data'''
    transformed_tweets = []
    for tweet in extracted_tweets:
        sentiment = 1 # later on you will calculate a sentiment
        # datatype of the tweet: dictionary
        tweet['sentiment'] = sentiment # adding a key: value pair with 'sentiment' as the key and the score as the value
        transformed_tweets.append(tweet)
        # transformed_tweets is a list of transformed dictionaries
    return transformed_tweets

def load(transformed_tweets):
    '''Load transformed data into the postgres database'''
    for tweet in transformed_tweets:
        insert_query = "INSERT INTO tweets VALUES (%s, %s, %s)"
        db_pg.execute(insert_query, (tweet['user_name'], tweet['text'], tweet['sentiment']))
        logging.critical('---Inserted a new tweet into postgres---')
        logging.critical(tweet)


while True:
    extracted_tweets = extract()
    transformed_tweets = transform(extracted_tweets)
    load(transformed_tweets)
    time.sleep(10)


'''
Right now the ETL job extracts the whole mongodb database in each run and appends it
to the tweets table in postgres.
This will cause a lot of duplicates in postgres.

Probably something we would want to do, is to only query the newest tweets from mongo
(or load all of the data but replace the tweets data in postgres)

- Usually the first option will be preferred. We call this an incremental load.
- There are situations in which you prefer a full load, for example if historical data
 can change.

How could we do that?
- you can filter the data in your query .find({condition})
- last five minutes (there is a timestamp in the tweets)
- findOne()
- find the last 100
- for the tweets that were extracted already, mark them as extracted .update() or .updateMany(); add 'extracted': 1
- query only for the ones that have not been extracted yet

'''
