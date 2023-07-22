import json
from gradio_client import Client

client = Client("https://sai004-articleapi.hf.space/")

def get_links(user_input):
    result = client.predict(user_input,api_name="/predict")
    with open(result, 'r') as file:
        # Read the file and convert it to a list
        file_content = file.read()
        data_list = eval(file_content)

    return data_list

def validate(user_input):
    result = client.predict(user_input,api_name="/predict_1")
    with open(result, 'r') as file:
        # Read the file and convert it to a list
        file_content = file.read()
        data_list = eval(file_content)
    return data_list
