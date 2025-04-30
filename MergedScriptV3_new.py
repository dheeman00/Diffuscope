# This script is used for the data extraction (Project: NetInf)
# The folders with numbers is the tweetID
# There are 5 different folders saving the information
# Note: The script will omit any RT made by the actual query user


# check if the required library are installed
try:
    import tweepy
except ImportError:
    print("Trying to install required module: tweepy \n")
    os.system('python3 -m pip install tweepy')
    import tweepy
try:
    import pandas as pd
except ImportError:
    print("Trying to install required module: pandas \n")
    os.system('python3 -m pip install pandas')
    import pandas as pd

try:
    import json
except ImportError:
    print("Trying to install required module: json \n")
    os.system('python3 -m pip install json')
    import json


import os
import time

class TwitterClient:

    ##default constructor##
    def __init__(self, ConsumerKey=None, ConsumerSecret=None, AccessKey=None,
                 AccessSecret=None, twitter_username=None):

        self.ConsumerKey = ConsumerKey
        self.ConsumerSecret = ConsumerSecret
        self.AccessKey = AccessKey
        self.AccessSecret = AccessSecret
        auth = tweepy.OAuthHandler(self.ConsumerKey, self.ConsumerSecret)
        auth.set_access_token(self.AccessKey, self.AccessSecret)

        self.api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True,
                              retry_errors=[401, 404, 500, 503],
                              retry_count=5, retry_delay=5)
        self.twitter_user = twitter_username

        # saving the information on the desired folder
        # self.today = time.strftime("%Y-%m-%d")
        # folder_path = "./Test/" + self.today
        folder_path = "./Test"
        tweet_folder = "/RetweetCollection/"
        commonPath = folder_path + tweet_folder + self.twitter_user

        # create the folders
        folder_tweet = "/Tweets"
        folder_retweeters = "/Retweeters"
        folder_followers = "/Followers"
        folder_followings = "/Followings"
        folder_profile = "/Profile"
        folder_history = "/History"

        folders = [folder_tweet, folder_retweeters, folder_followers, folder_followings, folder_profile, folder_history]
        self.all_folder_paths = []
        for folder in folders:
            path = commonPath + folder
            try:
                self.all_folder_paths.append(path)
                folder_path_check = os.path.isdir(path)
                if folder_path_check:
                    print('The folder path already exists {0}'.format(folder))
                else:
                    os.makedirs(path)
                    print("Created the folder path {0}".format(folder))
            except FileExistsError as err:
                print("Error while generating the folder", err)

        self.filename = None

    ##Collect the most recent tweet from user timeline
    ## num_tweets = 1 (to get the initial tweet)
    def get_user_timeline_tweets(self, num_tweets):

        # get the raw tweet from the API
        tweets_raw = []
        get_tweet_id = None
        
        for tweet in tweepy.Cursor(self.api.user_timeline, id=self.twitter_user, tweet_mode='extended').items(
                num_tweets):
            tweets_raw.append(tweet)
            get_tweet_id = str(tweet.id)

        # storing the return tweet
        tweets = []
        for info in tweets_raw:
            if info.full_text.startswith("RT @"):
                #print('The script stops as the first tweet in the user profile is a retweet')
                #pass 
                break  # updated
            else:
                # collecting the tweet data
                tweets.append(info._json)

                # saving the raw tweet information in json
                # open file to save information
                self.filename = self.twitter_user + "_tweets_" + ".json"
                folder_path = self.all_folder_paths[0] + "/" + get_tweet_id
                
                try:
                    folder_path_check = os.path.isdir(folder_path)
                    if folder_path_check:
                        pass
                    else:
                        os.makedirs(folder_path)
                except FileExistsError as err:
                    print("Error while generating the folder", err)
                
                # saving in json file
                completePath_json = os.path.join(folder_path, self.filename)
                SaveFile = open(completePath_json, 'w')
                all_data = json.dumps(info._json)
                SaveFile.write(all_data)
                SaveFile.write("\n")
                SaveFile.close()

        return tweets

    ##Collect the required information from the retweets
    ## tweet_list = contain tweet IDs in a list
    def get_required_information(self, tweet_list):
        tweet_created_at = []
        tweet_id = []
        tweet_text = []
        tweet_user_id = []
        tweet_screen_name = []

        get_tweet_id = None
        for i in tweet_list:
            tweet_created_at.append(str(i['created_at']))
            tweet_id.append(str(i['id']))            
            tweet_text.append(i['full_text'])
            tweet_user_id.append(str(i['user']['id']))
            tweet_screen_name.append(i['user']['screen_name'])

            get_tweet_id = str(i['id'])

        # saving the information
        df_record = pd.DataFrame({"created_at": tweet_created_at, "id": tweet_id,
                                  "text": tweet_text, "user_id": tweet_user_id,
                                  "screen_name": tweet_screen_name})

        # saving the outcome in xlsx format
        filename = self.twitter_user + "_tweets_" + ".xlsx"
        # updated
        folder_path = self.all_folder_paths[0] + "/" + get_tweet_id
        completePath = os.path.join(folder_path, filename)
        try:
            folder_path_check = os.path.isdir(folder_path)
            if folder_path_check:
                pass
            else:
                os.makedirs(folder_path)
        except FileExistsError as err:
            print("Error while generating the folder", err)
        df_record.to_excel(completePath, sheet_name='tweet_info', index=False,
                           encoding='utf-8')

        del filename
        del completePath

        return df_record

    # get the retweeter's information for the tweetID
    # tweet_id = ID of the tweet
    # number of retweet IDs against each tweet. Max 100
    def get_retweeters(self, tweet_id, count=None):

        # initialize the parameters
        retweet_time = []
        retweet_id = []
        retweet_text = []
        retweet_user_id = []
        retweet_user_screen_name = []
        all_retweets = []  # this list collects all the information

        # Returns up to 100 of the first retweets of the given tweet
        try:
            if count is None:
                # this will return what ever the API provides by default
                retweets = self.api.retweets(id=tweet_id)
                # print(retweets)
                all_retweets.extend(retweets)

            else:
                retweets = self.api.retweets(id=tweet_id, count=count)
                # print(retweets)
                all_retweets.extend(retweets)

            if retweets is None:
                return []

        except tweepy.error.TweepError as err:
            print('Error generated by the API')
            print(err.reason)

        # print(all_retweets)

        ##Collecting the required information
        for i in all_retweets:
            retweet_time.append(str(i.created_at))
            retweet_id.append(str(i.id))
            retweet_text.append(i.text)
            retweet_user_id.append(str(i.user.id))
            retweet_user_screen_name.append(i.user.screen_name)

        retweeters_info_df = pd.DataFrame({"created_at": retweet_time, "tweet_id": tweet_id, "retweet_id": retweet_id,
                                           "retweet_text": retweet_text, "retweet_user_id": retweet_user_id,
                                           "retweet_screen_name": retweet_user_screen_name})
        # saving the outcome in xlsx format
        filename = self.twitter_user + "_retweeters_" + ".xlsx"
        completePath = self.all_folder_paths[1] + "/" + str(tweet_id)
        try:
            folder_path_check = os.path.isdir(completePath)
            if folder_path_check:
                pass
            else:
                os.makedirs(completePath)
        except FileExistsError as err:
            print("Error while generating the folder", err)

        completePathUpdated = os.path.join(completePath, filename)
        retweeters_info_df.to_excel(completePathUpdated, sheet_name='retweeters', index=False,
                                    encoding='utf-8')
        del filename
        del completePath
        del completePathUpdated

        return retweeters_info_df

    ##Returns the IDs of users being following by the specified user
    def get_following_network_id(self, user, tweetID):

        filename = user + "_following_" + ".txt"
        completePath = self.all_folder_paths[3] + "/" + str(tweetID)
        try:
            folder_path_check = os.path.isdir(completePath)
            if folder_path_check:
                pass
            else:
                os.makedirs(completePath)
        except FileExistsError as err:
            print("Error while generating the folder", err)

        completePathUpdated = os.path.join(completePath, filename)
        output_file = open(completePathUpdated, 'w')

        counter = 0
        reset_counter = 0
        loop_counter = True
        backoff_timer = 2  # counter for timer
        while loop_counter:
            try:
                for followeringID in tweepy.Cursor(self.api.friends_ids, screen_name=user, count=5000).items():
                    time.sleep(0.01)
                    reset_counter += 1
                    # this is reducing the waiting time
                    if reset_counter % 74000 == 0:
                        reset_counter = 0
                        time.sleep(30)

                    counter += 1
                    # saving the txt file
                    output_file.write(str(followeringID) + '\n')
                break

            except tweepy.TweepError as err:
                if err.api_code == 50 or err.api_code == 63:  # 50 not found, 63 suspended
                    print('No information to extract')
                    break

                time.sleep(60 * backoff_timer)
                sleep_time = 60 * backoff_timer
                print('Error Generated by Tweepy API sleep {0} seconds.'.format(round(sleep_time, 2)))
                print(err.reason)
                backoff_timer += 1
                continue

            except Exception as e:
                print("Exception arisen other than the API")
                print(e)
                continue

        output_file.close()
        print("Completed: {0} --- Followings Collected {1}".format(user, counter))

        del filename
        del completePath
        del completePathUpdated

    ##Returns the IDs of users follower the specified user
    def get_followers_network_id(self, user, tweetID):

        filename = user + "_followers_" + ".txt"
        completePath = self.all_folder_paths[2] + "/" + str(tweetID)
        try:
            folder_path_check = os.path.isdir(completePath)
            if folder_path_check:
                pass
            else:
                os.makedirs(completePath)
        except FileExistsError as err:
            print("Error while generating the folder", err)

        completePathUpdated = os.path.join(completePath, filename)
        output_file = open(completePathUpdated, 'w')

        counter = 0
        reset_counter = 0
        loop_counter = True
        backoff_timer = 2  # counter for timer
        while loop_counter:
            try:
                for followerID in tweepy.Cursor(self.api.followers_ids, screen_name=user, count=5000).items():
                    time.sleep(0.01)
                    reset_counter += 1
                    # this is reducing the waiting time
                    if reset_counter % 74000 == 0:
                        reset_counter = 0
                        time.sleep(30)

                    counter += 1
                    # saving the txt file
                    output_file.write(str(followerID) + '\n')
                break

            except tweepy.TweepError as err:
                if err.api_code == 50 or err.api_code == 63:  # 50 not found, 63 suspended
                    print('No information to extract')
                    break

                time.sleep(60 * backoff_timer)
                sleep_time = 60 * backoff_timer
                print('Error Generated by Tweepy API sleep {0} seconds.'.format(round(sleep_time, 2)))
                print(err.reason)
                backoff_timer += 1
                continue

            except Exception as e:
                print("Exception arisen other than the API")
                print(e)
                continue

        output_file.close()
        print("Completed: {0} --- Followers Collected {1}".format(user, counter))

        del filename
        del completePath
        del completePathUpdated

    ##collect retweeter's history
    def get_retweeter_history(self, user, tweetID):
        tweet_info = []  # this is extracting all the information
        tweet_created_at = []
        tweet_id = []
        tweet_text = []
        tweet_user_id = []
        tweet_screen_name = []

        counter = 0
        cursor = tweepy.Cursor(self.api.user_timeline, id=user, monitor_rate_limit=True, tweet_mode='extended')
        try:
            for page in cursor.pages():
                for tweet in page:
                    tweet_info.append(tweet)
                    counter += 1

        except tweepy.error.TweepError as err:
            if err.api_code == 50 or err.api_code == 63:  # 50 not found, 63 suspended
                print('No information to extract')
                pass
            else:
                print("Error {}".format(err.reason))
                pass

        print("Collected History User: {0} --- Number Tweets: {1}".format(user, counter))

        for j in tweet_info:
            tweet_created_at.append(str(j.created_at))
            tweet_id.append(str(j.id))
            tweet_text.append(j.full_text)
            tweet_user_id.append(str(j.user.id))
            tweet_screen_name.append(j.user.screen_name)

        retweeters_history_df = pd.DataFrame({"created_at": tweet_created_at, "id": tweet_id,
                                              "text": tweet_text, "user_id": tweet_user_id,
                                              "screen_name": tweet_screen_name})
        # saving the outcome in xlsx format
        filename = user + "_history_" + ".xlsx"
        completePath = self.all_folder_paths[5] + "/" + str(tweetID)
        try:
            folder_path_check = os.path.isdir(completePath)
            if folder_path_check:
                pass
            else:
                os.makedirs(completePath)
        except FileExistsError as err:
            print("Error while generating the folder", err)

        completePathUpdated = os.path.join(completePath, filename)
        retweeters_history_df.to_excel(completePathUpdated, sheet_name='retweeter_history', index=False,
                                       encoding='utf-8')

        del filename
        del completePath
        del completePathUpdated

    ##this function is used to extract user profile information
    def retweeters_profile(self, user, num_tweet, tweetID):
        id_str = None
        name = None
        location = None
        followers_count = None
        friends_count = None
        created_at = None
        favourites_count = None
        statuses_count = None
        try:
            # extracting the retweeter profile information
            for k in tweepy.Cursor(self.api.user_timeline, screen_name=user).items(num_tweet):
                id_str = str(k.user.id_str)
                name = k.user.screen_name
                location = k.user.location
                followers_count = str(k.user.followers_count)
                friends_count = str(k.user.friends_count)
                created_at = str(k.user.created_at)
                favourites_count = str(k.user.favourites_count)
                statuses_count = str(k.user.statuses_count)
        except tweepy.error.TweepError as err:
            if err.api_code == 50 or err.api_code == 63:  # 50 not found, 63 suspended
                print('No information to extract')
                pass
            else:
                print("Error {}".format(err.reason))
                pass

        retweeters_profile_df = pd.DataFrame(
            {'created_at': [created_at], 'id': [id_str], 'name': [name], 'location': [location],
             'followers_count': [followers_count], 'followings_count': [friends_count],
             'favourites_count': [favourites_count], 'statuses_count': [statuses_count]})

        # saving the outcome in xlsx format
        filename = user + "_profile_" + ".xlsx"
        completePath = self.all_folder_paths[4] + "/" + str(tweetID)
        try:
            folder_path_check = os.path.isdir(completePath)
            if folder_path_check:
                pass
            else:
                os.makedirs(completePath)
        except FileExistsError as err:
            print("Error while generating the folder", err)

        completePathUpdated = os.path.join(completePath, filename)
        retweeters_profile_df.to_excel(completePathUpdated, sheet_name='retweeter_profile', index=False,
                                       encoding='utf-8')
        print('Collected Profile: {0}'.format(user))

        del filename
        del completePath
        del completePathUpdated


if __name__ == '__main__':

    # initial ID to extract the retweets
    user = 'JoeBiden' # example username
    # please include your key information here
    client = TwitterClient(ConsumerKey="",
                           ConsumerSecret="",
                           AccessKey="",
                           AccessSecret="",
                           twitter_username=user)
    print('Collecting the initial tweet data')
    tweets = client.get_user_timeline_tweets(num_tweets=1)
    # print(tweets)
    if len(tweets) == 0:
        print('The script stops as the first tweet in the user profile is a retweet')
        exit()
    
    # extracting the information
    user_actual_tweet = client.get_required_information(tweet_list=tweets)

    # Collecting the tweet IDs
    tweetID = user_actual_tweet.iloc[:, 1]
    # print(tweetID)

    for i in tweetID:
        # collecting upto 100 retweets (max provided by the API)
        retweeter = client.get_retweeters(tweet_id=i, count=100)

        # collecting retweeters information
        retweeterIDs = retweeter.iloc[:, 5]
        counter = 0
        print("Collecting Information for {0} Users".format(len(retweeterIDs)))
        print("\n")
        for userName in retweeterIDs:
            print("Collecting Data User: {0}".format(userName))
            # collect followers
            client.get_followers_network_id(user=userName, tweetID=i)
            # collect followings
            client.get_following_network_id(user=userName, tweetID=i)
            # collect profile
            client.retweeters_profile(user=userName, num_tweet=1, tweetID=i)
            # collect history
            client.get_retweeter_history(user=userName, tweetID=i)

            print("{0} -- Collected users data: {1}".format(counter, userName))
            counter += 1
            time.sleep(30)
            print("\n")

    print("Data Collected")
    print("EOF")
