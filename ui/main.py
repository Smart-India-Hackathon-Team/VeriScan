from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
Window.size = (350, 600)
import tweepy
import re

import config as config

import instaloader
import pandas as pd

from model_twitter import ModelTwitter
from model_instagram import ModelInstagram

# Define your Twitter API credentials
consumer_key = config.twitter_key
consumer_secret = config.twitter_secret
access_token = config.twitter_token_access
access_token_secret = config.twitter_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

bot = instaloader.Instaloader() # instaloader initialization

# Function to extract Twitter username from URL
def extract_username_from_url(url):
    match = re.search(r'(?:https?://twitter\.com/)?@?([A-Za-z0-9_]+)', url)
    if match:
        return match.group(1)
    return None

# Function to get user details by username
def get_user_details(username):
    try:
        user = api.get_user(screen_name=username)  # Change here
        return user._json
    except tweepy.TweepyException as e:
        return {'error': str(e)}

Builder.load_file("home.kv")
Builder.load_file("twitter.kv")
Builder.load_file("twitterresult.kv")
Builder.load_file("instagram.kv")
Builder.load_file("instagramresult.kv")
Builder.load_file("twitterdetect.kv")
Builder.load_file("instagramdetect.kv")
class HomeScreen(Screen):
    pass

    def open_twitter_screen(self):
        self.manager.current = 'twitter'

    def open_instagram_screen(self):
        self.manager.current = 'instagram'

    def open_linkedin_screen(self):
        self.manager.current = 'linkedin'

    def open_facebook_screen(self):
        self.manager.current = 'facebook'

class TwitterScreen(Screen):
    
    def get_profile_info(self,twitter_url):
        # Extract the Twitter username from the URL
        username = extract_username_from_url(twitter_url)
        if username:
            user_details = get_user_details(username)
            if user_details:
                print(f"User Details: {user_details}")
                # Set the profile_info property of the App
                MyApp.profile_info = user_details
                # Switch to the second screen
                self.manager.current = 'twitter_result'

            else:
                print("Error: Failed to retrieve user details")
        else:
            print("Invalid Twitter URL")


    def bckBtn(self):
        self.manager.current = 'home'

class Twitterresult(Screen):
    result_label = None  # Define result_label as a class attribute

    def on_pre_enter(self):
        profile_info = App.get_running_app().profile_info
        if profile_info:
            # Extract and display important information
            user_name = profile_info.get('name', '')
            screen_name = profile_info.get('screen_name', '')
            followers_count = profile_info.get('followers_count', 0)
            friends_count = profile_info.get('friends_count', 0)
            statuses_count = profile_info.get('statuses_count', 0)

            info_text = f"Name: {user_name}\n"
            info_text += f"Username: {screen_name}\n"
            info_text += f"Followers: {followers_count}\n"
            info_text += f"Friends: {friends_count}\n"
            info_text += f"Statuses: {statuses_count}\n"

            # Access the result_label using its id and update its text
            self.ids.result_label.text = info_text


    def bckBtn(self):
        self.manager.current = 'twitter'

    def detect(self):
        self.manager.current = 'twitter_detect'

class Twitterdetect(Screen):
    '''def __init__(self, **kwargs):
        super(Twitterdetect, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="Result")

        block_button = Button(text="Block", background_color=(1, 0, 0, 1))
        block_button.bind(on_release=self.block)

        back_button = Button(text="Back")
        back_button.bind(on_release=self.bckBtn)

        layout.add_widget(self.result_label)
        layout.add_widget(block_button)
        layout.add_widget(back_button)

        self.add_widget(layout)'''

    # DUMMY DATA - Have to replace it with ML Model
    def on_pre_enter(self):

        model_instance = ModelTwitter()
        profile_info = App.get_running_app().profile_info
        username = profile_info.get('screen_name', '')
        prediction = model_instance.tpredict(username)

        if prediction:
            info_text = f"Prediction: {prediction}\n"
            self.ids.result_label.text = info_text

        # if profile_info:
        #     # Extract and display important information
        #     user_name = profile_info.get('name', '')
        #     screen_name = profile_info.get('screen_name', '')
        #     followers_count = profile_info.get('followers_count', 0)
        #     friends_count = profile_info.get('friends_count', 0)
        #     statuses_count = profile_info.get('statuses_count', 0)

        #     info_text = f"Name: {user_name}\n"
        #     info_text += f"Username: {screen_name}\n"
        #     info_text += f"Followers: {followers_count}\n"
        #     info_text += f"Friends: {friends_count}\n"
        #     info_text += f"Statuses: {statuses_count}\n"

        #     self.result_label.text = info_text

    def bckBtn(self, instance):
        self.manager.current = 'twitter_result'

    def block(self, instance):
        profile_info = App.get_running_app().profile_info
        screen_name = profile_info.get('screen_name', '')
        try:
            # Get the user's ID using their screen name
            user = api.get_user(screen_name=screen_name)  # Provide screen_name as a keyword argument
            user_id = user.id_str

            # Block the user by their user_id
            api.create_block(user_id=user_id)  # Pass user_id as a keyword argument

            print(f"User @{screen_name} has been blocked successfully.")
        except tweepy.TweepyException as e:
            print(f"Error blocking user @{screen_name}: {e.reason}")

class InstagramScreen(Screen):
    '''def __init__(self, **kwargs):
        super(InstagramScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Enter Instagram Profile URL:")
        self.text_input = TextInput(hint_text="Enter URL here")
        button = Button(text="Get Profile Info")
        button.bind(on_release=self.get_profile_info)
        back_button = Button(text="Back")
        back_button.bind(on_release=self.bckBtn)  # Corrected binding here
        layout.add_widget(label)
        layout.add_widget(self.text_input)
        layout.add_widget(button)
        layout.add_widget(back_button)
        self.add_widget(layout)

        self.username = None'''
    
    def get_profile_info(self, instagram_url):
        print(instagram_url)
        # Extract the Instagram username from the URL
        pattern = r'https://www\.instagram\.com/([A-Za-z0-9_\.]+)'
        match = re.search(pattern, instagram_url)
        self.username = match.group(1)
        self.manager.current = 'instagram_result'

    def bckBtn(self):
        self.manager.current = 'home'

class Instagramresult(Screen):
    def on_pre_enter(self):
        instagram_screen = App.get_running_app().root.get_screen('instagram')  # Access InstagramScreen instance
        username = instagram_screen.username
        profile = instaloader.Profile.from_username(bot.context, username)
        print(profile)
        if profile:
            info_text = f"Name: {profile.username}\n"
            info_text += f"Username: {profile.username}\n"
            info_text += f"Followers: {profile.followers}\n"
            info_text += f"Following: {profile.followees}\n"
            info_text += f"Number of Posts: {profile.mediacount}\n"
            info_text += f"Bio: {profile.biography}\n"
            info_text += f"External Url: {profile.external_url}\n"

            self.ids.result_label.text = info_text

    def bckBtn(self):
        self.manager.current = 'instagram'

    def detect(self):
        self.manager.current = 'instagram_detect'


class Instagramdetect(Screen):
    '''def __init__(self, **kwargs):
        super(Instagramdetect, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="Result")

        block_button = Button(text="Block", background_color=(1, 0, 0, 1))
        block_button.bind(on_release=self.block)

        back_button = Button(text="Back")
        back_button.bind(on_release=self.bckBtn)

        layout.add_widget(self.result_label)
        layout.add_widget(block_button)
        layout.add_widget(back_button)

        self.add_widget(layout)'''

    # DUMMY DATA - Have to replace it with ML Model
    def on_pre_enter(self):
        print("test")
        instagram_screen = App.get_running_app().root.get_screen('instagram')  # Access InstagramScreen instance

        model_instance = ModelInstagram()
        username = instagram_screen.username
        prediction = model_instance.ipredict(username)

        if prediction:
            info_text = f"Prediction: {prediction}\n"
            self.ids.result_label.text = info_text

    def bckBtn(self):
        self.manager.current = 'instagram_result'

    def block(self):
        pass

class LinkedInScreen(Screen):
    def __init__(self, **kwargs):
        super(LinkedInScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Enter LinkedIn Profile URL:")
        self.text_input = TextInput(hint_text="Enter URL here")
        button = Button(text="Get Profile Info")
        button.bind(on_release=self.get_profile_info)
        back_button = Button(text="Back")
        back_button.bind(on_release=self.bckBtn)  # Corrected binding here
        layout.add_widget(label)
        layout.add_widget(self.text_input)
        layout.add_widget(button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def get_profile_info(self, instance):
        linkedin_url = self.text_input.text
        print(linkedin_url)
        # Extract the linkedin username from the URL
        username = extract_username_from_url(linkedin_url)
        if username:
            user_details = get_user_details(username)
            if user_details:
                print(f"User Details: {user_details}")
                # Set the profile_info property of the App
                MyApp.profile_info = user_details
                # Switch to the second screen
                self.manager.current = 'linkedin_result'
            else:
                print("Error: Failed to retrieve user details")
        else:
            print("Invalid LinkedIn URL")


    def bckBtn(self, instance):
        self.manager.current = 'home'

class LinkedInResult(Screen):
    def __init__(self, **kwargs):
        super(LinkedInResult, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="LinkedIn Profile Info")
        back_button = Button(text="Back")
        back_button.bind(on_release=self.bckBtn)
        layout.add_widget(self.result_label)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def on_pre_enter(self):
        profile_info = App.get_running_app().profile_info
        if profile_info:
            # Extract and display important information
            user_name = profile_info.get('name', '')
            screen_name = profile_info.get('screen_name', '')
            followers_count = profile_info.get('followers_count', 0)
            friends_count = profile_info.get('friends_count', 0)
            statuses_count = profile_info.get('statuses_count', 0)

            info_text = f"Name: {user_name}\n"
            info_text += f"Username: {screen_name}\n"
            info_text += f"Followers: {followers_count}\n"
            info_text += f"Friends: {friends_count}\n"
            info_text += f"Statuses: {statuses_count}\n"

            self.result_label.text = info_text

    def bckBtn(self, instance):
        self.manager.current = 'linkedin'


class FacebookScreen(Screen):
    def __init__(self, **kwargs):
        super(FacebookScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Enter Facebook Profile URL:")
        self.text_input = TextInput(hint_text="Enter URL here")
        button = Button(text="Get Profile Info")
        button.bind(on_release=self.get_profile_info)
        back_button = Button(text="Back")
        back_button.bind(on_release=self.bckBtn)  # Corrected binding here
        layout.add_widget(label)
        layout.add_widget(self.text_input)
        layout.add_widget(button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def get_profile_info(self, instance):
        facebook_url = self.text_input.text
        print(facebook_url)
        # Extract the linkedin username from the URL
        username = extract_username_from_url(facebook_url)
        if username:
            user_details = get_user_details(username)
            if user_details:
                print(f"User Details: {user_details}")
                # Set the profile_info property of the App
                MyApp.profile_info = user_details
                # Switch to the second screen
                self.manager.current = 'facebook_result'
            else:
                print("Error: Failed to retrieve user details")
        else:
            print("Invalid Facebook URL")


    def bckBtn(self, instance):
        self.manager.current = 'home'

class FacebookResult(Screen):
    def __init__(self, **kwargs):
        super(FacebookResult, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="Facebook Profile Info")
        back_button = Button(text="Back")
        back_button.bind(on_release=self.bckBtn)
        layout.add_widget(self.result_label)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def on_pre_enter(self):
        profile_info = App.get_running_app().profile_info
        if profile_info:
            # Extract and display important information
            user_name = profile_info.get('name', '')
            screen_name = profile_info.get('screen_name', '')
            followers_count = profile_info.get('followers_count', 0)
            friends_count = profile_info.get('friends_count', 0)
            statuses_count = profile_info.get('statuses_count', 0)

            info_text = f"Name: {user_name}\n"
            info_text += f"Username: {screen_name}\n"
            info_text += f"Followers: {followers_count}\n"
            info_text += f"Friends: {friends_count}\n"
            info_text += f"Statuses: {statuses_count}\n"

            self.result_label.text = info_text

    def bckBtn(self, instance):
        self.manager.current = 'facebook'

class MyApp(MDApp):
    profile_info = None

    def build(self):
        self.title = "VeriScan"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        sm = ScreenManager()
        home_screen = HomeScreen(name= 'home')
        sm.add_widget(home_screen)

        twitter = TwitterScreen(name='twitter')
        sm.add_widget(twitter)

        sm.add_widget(TwitterScreen(name='twitter'))
        sm.add_widget(Twitterresult(name='twitter_result'))
        sm.add_widget(Twitterdetect(name='twitter_detect'))

        sm.add_widget(InstagramScreen(name='instagram'))
        sm.add_widget(Instagramresult(name='instagram_result'))
        sm.add_widget(Instagramdetect(name='instagram_detect'))

        sm.add_widget(LinkedInScreen(name='linkedin'))
        sm.add_widget(LinkedInResult(name='linkedin_result'))

        sm.add_widget(FacebookScreen(name='facebook'))
        sm.add_widget(FacebookResult(name='facebook_result'))
        
        return sm

if __name__ == '__main__':
    MyApp().run()
