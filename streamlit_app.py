import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

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
try:
  fruit_choice = streamlit.text_input("What fruit information would you like ?")
  if not fruit_choice:
    streamlit.write("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
    # Assigning Normalized json to fruityvice_normalized
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
    streamlit.write("The user entered" , fruit_choice)
    
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
fruit_add = streamlit.text_input("What fruit would you like to add?")
streamlit.write("Thanks for adding " , fruit_add)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES('from streamlit')")
