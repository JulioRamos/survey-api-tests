import unittest
from survey_api.survey_api import SurveyPage, CustomerExportAPI
from survey_api.parameters import CUSTOMER_ID

    
# Unit tests for the survey API
class TestSurveyAPI(unittest.TestCase):

    def test_submit_survey_happy_path_all_fields(self):
        # Test the happy path for submitting a survey
        cea = CustomerExportAPI(CUSTOMER_ID)
        sp = SurveyPage(cea.get_survey_link())
        
        answers = {
            "question-0": "Green",
            "question-1": ["Pop", "Rock"],
            "question-2": "3",
            "question-3": "The Shawshank Redemption",
        }

        sp.submit_survey(answers)
        event_test_data = cea.get_customer_data()
        
        latest_events = {}
        latest_answer = {}
        for event in event_test_data["events"]:
            question_id = event["properties"]["question_id"]
            question_answer = event["properties"]["answer"]
            if question_id not in latest_events or latest_events[question_id]["timestamp"] < event["timestamp"]:
                latest_events[question_id] = event
                latest_answer[question_id] = question_answer
        
        # print (json.dumps(latest_events, indent=4))

        self.assertEqual(latest_answer[0], answers["question-0"]) # Color
        self.assertEqual(latest_answer[1], answers["question-1"]) # Music
        self.assertEqual(latest_answer[2], answers["question-2"]) # Harry Potter's Book Rate
        self.assertEqual(latest_answer[3], answers["question-3"]) # Movie
        
        # Assert that the latest events were sent in the same request
        self.assertEqual(len(set([event["timestamp"] for event in latest_events.values()])), 4)

        print ('Test Passed')

    def test_submit_survey_happy_path_optional_field_missing(self):
        # Test the happy path for submitting a survey with a blank answer for the favorite movie
        cea = CustomerExportAPI(CUSTOMER_ID)
        sp = SurveyPage(cea.get_survey_link())

        answers = {
            "question-0": "Green",
            "question-1": ["Pop", "Rock"],
            "question-2": "3",
        }

        sp.submit_survey(answers)
        event_test_data = cea.get_customer_data()
        
        latest_events = {}
        latest_answer = {}
        for event in event_test_data["events"]:
            question_id = event["properties"]["question_id"]
            question_answer = event["properties"]["answer"]
            if question_id not in latest_events or latest_events[question_id]["timestamp"] < event["timestamp"]:
                latest_events[question_id] = event
                latest_answer[question_id] = question_answer
        
        # print (json.dumps(latest_events, indent=4))

        self.assertEqual(latest_answer[0], answers["question-0"]) # Color
        self.assertEqual(latest_answer[1], answers["question-1"]) # Music
        self.assertEqual(latest_answer[2], answers["question-2"]) # Harry Potter's Book Rate

        # Assert that the latest events were sent in the same request
        self.assertEqual(len(set([event["timestamp"] for event in latest_events.values()])), 3)

        print ('Test Passed')

    def test_submit_survey_missing_required_field(self):
        # Check that no event were sent to the server after a failed submission
        cea = CustomerExportAPI(CUSTOMER_ID)
        sp = SurveyPage(cea.get_survey_link())

        answers = {
            "question-0": "",
            "question-1": ["Pop", "Rock"],
            "question-2": "3",
            "question-4": "This Data Should Not Be Stored",
        }

        # get the number of events before trying to submit data
        event_test_data_before_sub = cea.get_customer_data()
        
        # try to submit the data
        sp.submit_survey(answers)

        # get the number of events after trying to submit data
        event_test_data = cea.get_customer_data()

        # assert that the number of events before and after the submission are the same
        self.assertEqual(len(event_test_data_before_sub["events"]), len(event_test_data["events"]))

        print ('Test Passed')

if __name__ == "__main__":
    unittest.main()