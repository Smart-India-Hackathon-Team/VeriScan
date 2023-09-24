import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import instaloader

class ModelInstagram():
    def train_model(self):
        data = {}
        data['fake'] = pd.read_csv('Datasets/instagram_fake_users.csv')
        data['real'] = pd.read_csv("Datasets/instagram_real_users.csv")
        data['real'] = data['real'].drop(['isFake'], axis = 1)
        data['fake'] = data['fake'].drop(['isFake'], axis = 1)

        data['fake'] = data['fake'].values
        data['real'] = data['real'].values

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
            
            X[len(data["real"])+i] = data["real"][i]/bound 
            Y[len(data["real"])+i] = 1

        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.24, random_state=42)

        model = RandomForestClassifier(n_estimators=20)
        model.fit(x_train, y_train)
        score = model.score(x_test, y_test)
        y_predicted = model.predict(x_test)
        return model
    
    def ipredict(self, username):
        bot = instaloader.Instaloader()
        model = self.train_model()
        try:
            user = instaloader.Profile.from_username(bot.context, username)
            digits = 0
            length = 0
            for i in user.username:
                if i.isdigit():
                    digits+=1
                length+=1
            x = np.array([[user.followers, user.followees, len(user.biography),user.mediacount, 1 if(user.profile_pic_url) else 0, int(user.is_private), digits, length]])
            nans = np.isnan(x)
            x[nans] = 0
            y = model.predict(x)
            return "Real" if y[0] == 1 else "Fake"
        except:
            return False
