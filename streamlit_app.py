import streamlit
import pandas
streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
#Reading csv file from S3 bucket into data frame
fruit_data_frame=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
fruit_data_frame=fruit_data_frame.set_index('Fruit');

#Adding pick up list to customize smoothie
display_fruits=streamlit.multiselect('Pick up some fruits:', list(fruit_data_frame.index),['Avocado','Strawberries'])
display_fruits=fruit_data_frame.loc[display_fruits]

#Display dataframe
streamlit.dataframe(display_fruits)

#New section to display Fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +"kiwi")
#streamlit.text(fruityvice_response.json())

# Assigning Normalized json to fruityvice_normalized
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# Assign data from fruityvice_normalized variable to daata frame and display
streamlit.dataframe(fruityvice_normalized)

