from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
import tweepy
import re

import config

# Define your Twitter API credentials
consumer_key = config.twitter_key
consumer_secret = config.twitter_secret
access_token = config.twitter_token_access
access_token_secret = config.twitter_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Select a Social Media Platform:")

        # Create buttons for different platforms
        twitter_button = Button(text="Twitter")
        twitter_button.bind(on_release=self.open_twitter_screen)

        instagram_button = Button(text="Instagram")
        instagram_button.bind(on_release=self.open_instagram_screen)

        linkedin_button = Button(text="LinkedIn")
        linkedin_button.bind(on_release=self.open_linkedin_screen)

        facebook_button = Button(text="Facebook")
        facebook_button.bind(on_release=self.open_facebook_screen)

        layout.add_widget(label)
        layout.add_widget(twitter_button)
        layout.add_widget(instagram_button)
        layout.add_widget(linkedin_button)
        layout.add_widget(facebook_button)

        self.add_widget(layout)

    def open_twitter_screen(self, instance):
        self.manager.current = 'twitter'

    def open_instagram_screen(self, instance):
        self.manager.current = 'instagram'

    def open_linkedin_screen(self, instance):
        self.manager.current = 'linkedin'

    def open_facebook_screen(self, instance):
        self.manager.current = 'facebook'

class TwitterScreen(Screen):
    def __init__(self, **kwargs):
        super(TwitterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="Enter Twitter Profile URL:")
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
        twitter_url = self.text_input.text
        print(twitter_url)
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


    def bckBtn(self, instance):
        self.manager.current = 'home'

class TwitterResult(Screen):
    def __init__(self, **kwargs):
        super(TwitterResult, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="Twitter Profile Info Will Be Shown Here")
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
        self.manager.current = 'twitter'


class InstagramScreen(Screen):
    def __init__(self, **kwargs):
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

    def get_profile_info(self, instance):
        instagram_url = self.text_input.text
        print(instagram_url)
        # Extract the Instagram username from the URL
        username = extract_username_from_url(instagram_url)
        if username:
            user_details = get_user_details(username)
            if user_details:
                print(f"User Details: {user_details}")
                # Set the profile_info property of the App
                MyApp.profile_info = user_details
                # Switch to the second screen
                self.manager.current = 'instagram_result'
            else:
                print("Error: Failed to retrieve user details")
        else:
            print("Invalid Instagram URL")


    def bckBtn(self, instance):
        self.manager.current = 'home'

class InstagramResult(Screen):
    def __init__(self, **kwargs):
        super(InstagramResult, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="Instagram Profile Info")
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
        self.manager.current = 'instagram'

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

class MyApp(App):
    profile_info = None

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))

        sm.add_widget(TwitterScreen(name='twitter'))
        sm.add_widget(TwitterResult(name='twitter_result'))

        sm.add_widget(InstagramScreen(name='instagram'))
        sm.add_widget(InstagramResult(name='instagram_result'))

        sm.add_widget(LinkedInScreen(name='linkedin'))
        sm.add_widget(LinkedInResult(name='linkedin_result'))

        sm.add_widget(FacebookScreen(name='facebook'))
        sm.add_widget(FacebookResult(name='facebook_result'))

        return sm

if __name__ == '__main__':
    MyApp().run()
