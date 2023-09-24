# VeriScan - Social Media User Authenticity Checker

VeriScan is a Python-based mobile application developed during the SIH Hackathon 2023. It leverages machine learning, specifically the scikit-learn library with a Random Forest model, to determine whether a social media user is real or fake. This app is built using the Kivy framework for the user interface and provides a simple and effective way to verify the authenticity of social media profiles.

## Table of Contents

- [Introduction](#veriscan---social-media-user-authenticity-checker)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Machine Learning Model](#machine-learning-model)
- [License](#license)

## Features

- Check the authenticity of social media profiles.
- Utilizes machine learning to predict the authenticity of a user.
- User-friendly interface built with Kivy for a seamless experience.
- Quick and efficient results.
- Fast and easy installation.

## Installation

To install VeriScan on your mobile device, follow these steps:

1. Clone this GitHub repository:
   ```
   git clone https://github.com/Smart-India-Hackathon-Team/VeriScan
   ```

2. Install the required Python packages using pip:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

4. The VeriScan app will open on your computer. You can then deploy it on your mobile device following Kivy's deployment guidelines.

## Usage

1. Launch the VeriScan app on your mobile device.

2. Select the social media app

3. Enter the profile url and press "Search" button to check profile information

3. Click the "Detect" button.

4. The app will use the machine learning model to predict whether the user is real or fake.

5. Make an informed decision based on the app's prediction.

## Machine Learning Model

VeriScan uses scikit-learn with a Random Forest model to predict the authenticity of social media users. The model has been trained on a dataset of real and fake social media profiles to make accurate predictions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<hr>

Developed by [Ananta, Arnav, Alviya, Karan, Siddharth, Tushita] for the SIH Hackathon 2023.
