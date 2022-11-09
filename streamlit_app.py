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

#Adding pick up list to customize smoothie
streamlit.multiselect('Pick up some fruits:', list(fruit_data_frame.index))

#Display dataframe
streamlit.dataframe(fruit_data_frame)
