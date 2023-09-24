import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import tweepy

class ModelTwitter():
    def train_model(self):
        data = {}
        data['fake'] = pd.read_csv('Datasets/twitter_fake_users.csv')
        data['real'] = pd.read_csv("Datasets/twitter_real_users.csv")

        data['fake'] = data['fake'].drop(["id", "name", "screen_name", "created_at", "lang", "location", "default_profile", "default_profile_image", "geo_enabled", "profile_banner_url", "profile_use_background_image", "profile_background_image_url_https", "profile_text_color", "profile_image_url_https", "profile_sidebar_border_color", "profile_background_tile", "profile_sidebar_fill_color", "profile_background_image_url", "profile_background_color", "profile_link_color", "utc_offset", "dataset", "updated", "description", "profile_image_url", "url"], axis=1)

        data['real'] = data['real'].drop(["id", "name", "screen_name", "created_at", "lang", "location", "default_profile", "default_profile_image", "geo_enabled", "profile_banner_url", "profile_use_background_image", "profile_background_image_url_https", "profile_text_color", "profile_image_url_https", "profile_sidebar_border_color", "profile_background_tile", "profile_sidebar_fill_color", "profile_background_image_url", "profile_background_color", "profile_link_color", "utc_offset", "dataset", "updated", "description", "profile_image_url", "url"], axis=1)

        data['fake'] = data['fake'].values
        data['real'] = data['real'].values

        for i in range(len(data["real"])):
            if type(data['real'][i][5]) == str:
                data['real'][i][5] = 1

        for i in range(len(data["fake"])):
            if type(data['fake'][i][5]) == str:
                data['fake'][i][5] = 1


        data["real"] = data["real"].astype(np.float64)
        data["fake"] = data["fake"].astype(np.float64)

        nans = np.isnan(data["real"])
        data["real"][nans] = 0

        nans = np.isnan(data["fake"])
        data["fake"][nans] = 0

        X = np.zeros((len(data["fake"]) + len(data["real"]), 8))
        Y = np.zeros(len(data["fake"]) + len(data["real"]))

        for i in range(len(data["real"])):
            X[i] = data["real"][i]/max(data["real"][i])
            Y[i] = -1

        for i in range(len(data["fake"])):
            bound = max(data["fake"][i])
            if bound == 0:
                bound = 1
            
            X[len(data["real"])+i] = data["real"][i]/bound # Normalizing Data [0 <--> 1]
            Y[len(data["real"])+i] = 1

        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.24, random_state=42)

        model = RandomForestClassifier(n_estimators=20)
        model.fit(x_train, y_train)
        return model

    def tpredict(self, username):
        consumer_key = 'cxSdxJ4DAvHEFOfkzSiAW9ZhM'
        consumer_secret = 'fJe08TAApTbq9YOz6fc3VrE0O9hGK8h8fCNjSURmpoTiL0Tmv6'
        access_token = '1417469551390822405-mNq3MVxkatbkBYKQzfyrspIy1iFGB0'
        access_token_secret = 'XTR09LN3qPcdW35JIPNmz4mZ2IJgl1NpP3YeHQjKItZqW'


        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        #username = input("Enter the username: ")
        model = self.train_model()
        try:
            user = api.get_user(screen_name=username)
            x = np.array([[user.statuses_count, user.followers_count, user.friends_count, user.favourites_count, user.listed_count, user.time_zone, user.protected, user.verified]])
            x = x.astype(np.float64)
            nans = np.isnan(x)
            x[nans] = 0
            y = model.predict(x)
            return "Real" if y[0] == 1 else "Fake"

        except:
            return False

