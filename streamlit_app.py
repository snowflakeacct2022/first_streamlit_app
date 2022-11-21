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

#Create a function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
  # Assigning Normalized json to fruityvice_normalized
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
#New section to display Fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input("What fruit information would you like ?")
  if not fruit_choice:
    streamlit.write("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()
    #streamlit.write("The user entered" , fruit_choice)
    
streamlit.header("The fruit load list contains:")
#snowflake related function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
    return my_cur.fetchall()

#Add button to load fruit list
if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_row)


#snowflake add fruit function
def insert_fruit_load_list(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES('" + new_fruit + "')")
    my_cnx.close()
    return "Thanks for adding " + new_fruit 
  
add_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add fruit to list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_fruit_load_list(add_fruit)
  streamlit.text(back_from_function)

streamlit.stop()


