# survey-api-tests

## Task 1
Your task is to write automated API tests for a simple use case of submitting a Survey described below. You can choose to implement these tests in either Python or GoLang

### Project Overview
This project is part of task from BloomReach for the QA Engineer position. This is a small test automation framework for testing the Survey feature of the Bloomreach platform. The framework is written in Python and uses the Requests library for HTTP requests.

### Getting Started
1. Clone the repository:
``` bash
git clone https://github.com/JulioRamos/survey-api-tests.git
```

2. Install the dependencies:
``` bash
pip install -r requirements.txt
```

3. Set the credentials.py to match your Bloomreach API Key ID and Secret:
``` python
API_KEY_ID = 'YOUR_API_KEY_ID'
API_KEY_SECRET = 'YOUR_API_KEY_SECRET'
```

4. Run the tests:
``` bash
python -m unittest discover -s tests/
```

### Framework Structure
The framework has the following structure:
├── README.md  
├── requirements.txt  
├── survey_api  
├   ├── survey_api.py  
│   ├── credentials.py  
│   └── parameters.py  
└── tests  
    └── test_survey_api  


* survey_api: contains the survey_api.py module which defines the API client for interacting with the Survey API, the credentials.py, that stores the API Keys; and the parameters.py, which stores global variables.
* tests: contains the test cases for the Survey API.

### Test Cases
The framework includes the following test cases:
test_submit_survey_happy_path_all_fields: tests that when a customer submits a survey with all required fields, an event is tracked asynchronously to the customer's profile for each answered question of the survey, and the tracked event contains the expected information.
test_submit_survey_happy_path_optional_field_missing: tests when a customer submits a survey with one missing non-required field (favorite movie). In this scenario, the tracked event must contain the relevant data but the movie should be empty.
test_submit_survey_missing_required_field: tests that when a customer submits a survey with missing required fields. In this scenario, the tracked event must not contain any of the data that the customer tried to submit.

## Task 2
Think about what other scenarios could be tested and define at least 3 such test scenarios in writing. You do not need to implement these tests

* Testing the response of the API when invalid data is submitted. For example, you could test what happens when you submit a survey with no answers, or when you submit answers that are not in the correct format.
* Testing the response of the API when there is an error. For example, you could test what happens when the API is down, or when you submit a request that is too large.
* Testing the performance of the API. For example, you could test how long it takes to submit a survey with a large number of answers.

These are just a few examples of other scenarios that could be tested. The specific tests that you implement will depend on the specific API that you are testing.

## Issues
I created the method for submiting a survey (survey_api.py > SurveyPage().submit_survey()), but I was not able to execute it properly. So right now the framework relays on data that is already stored. This is the reason that the test case  test_submit_survey_happy_path_optional_field_missing is failing

## Contributing
Contributions are welcome! If you have any suggestions or find any issues, please open an issue or pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
