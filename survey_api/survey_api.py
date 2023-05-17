import requests
from bs4 import BeautifulSoup
import logging
import json
from base64 import b64encode as b64encode

from survey_api.credentials import API_KEY_ID, API_KEY_SECRET
from survey_api.parameters import CUSTOMER_EXPORT_API_URL, CUSTOMER_ID

# Defines a class and methods for interacting with the Survey Page
class SurveyPage():
    def __init__(self, url_survey):
        self.url_survey = url_survey
        self.client = requests.session()
        self.response = self.client.get(self.url_survey)
    
    def submit_survey(self, answers):
        # Submit a survey response with the specified answers and return the result of the request

        # Get the csrf_token from the Survey page code
        csrf_token = self.get_csrf_token()

        # Add the csrf_token to the answers
        answers[csrf_token] = csrf_token
        
        # Define the cookie (I think it's static)
        cookie = "session=eyJjc3JmX3Rva2VuIjoiM2ZkODdhMzU2ZDM0OWUyZDdkNGUzYTE0ZDg5MjE0YmZhNGZjMTI2ZCJ9.ZF-ZsA.RhxOGd73igYPDg0torEbX7ME-ok"
        
        # Create the request's header
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Cookie": f"session={self.client.cookies['session']}",
            "X-CSRF-Token": csrf_token
        }
    
        # Send the request with the data as specified before
        response = requests.post(self.url_survey, data=answers, cookies={"session": cookie}, headers=headers)
        
        return response
        
    def get_csrf_token(self):
        # Get the csrf_token from the HTML code

        # Parse the HTML code
        soup = BeautifulSoup(self.response.content, "html.parser")

        # Get the value of the csrf_token
        csrf_token = soup.find("input", id="csrf_token").get("value")

        if csrf_token:
            # print(f"The value of the input tag with id 'csrf_token' and name 'csrf_token' is '{csrf_token}'")
            return csrf_token
        else:
            return None

   
# Defines a class and methods for interacting with the Customer Export API
class CustomerExportAPI():
    def __init__(self, customer_id):
        self.customer_id = customer_id

    def __get_private_auth_str(self, api_key_id, api_key_secret):
        # Return a base64-encoded string of the API key and secret
        
        credentials = f"{api_key_id}:{api_key_secret}"
        encoded_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")
        return encoded_credentials

    def __create_header(self):
        # Return headers for API requests
        
        encoded_credentials = self.__get_private_auth_str(API_KEY_ID, API_KEY_SECRET)
        
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
            "Content-type": "application/json"
        }
        return headers

    def get_customer_data(self):
        # Retrieve all data stored for a specific customer

        url = CUSTOMER_EXPORT_API_URL
        headers = self.__create_header()
        payload = {"customer_ids": {"registered": f"{self.customer_id}"}}
        response = requests.post(url, json=payload, headers=headers)
        return json.loads(response.text)
    
    def get_survey_link(self):
        # Retrieve the personalized survey link for the specified customer ID
        
        data = self.get_customer_data()
        url_survey = data["properties"]["survey link"]
        logging.info(f"Survey link: {url_survey}")
        return url_survey