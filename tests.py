import unittest
from unittest.mock import Mock, patch

from main import BoredAPIWrapper, cur


class TestBoredAPIWrapper(unittest.TestCase):
    def test_dataBase(self):
        # Prepare test data
        user_filters = "my_program new --type education --participants 1 --price_min 0.1 --price_max 30 --accessibility_min 0.1 --accessibility_max 0.5"
        
        # Initialize BoredAPIWrapper object with mock data
        method = BoredAPIWrapper(None, None, None, None, None, None, None)
        method.dataBase(user_filters)
        
        # Check if the record has been saved to the database
        cur.execute("SELECT * FROM commands WHERE filters = ?", (user_filters,))
        result = cur.fetchone()
        
        # Check if the record is saved correctly
        self.assertIsNotNone(result, "The record has not been added to the database")


    def test_parse_with_error(self):
        # Initialize BoredAPIWrapper object with mock data
        method = BoredAPIWrapper(None, None, None, None, None, None, None)

        # Create a mock response object for a failed request
        mock_response = Mock()
        mock_response.status_code = 404

        # Use patch to replace requests.get with the mock response
        with patch('requests.get', return_value=mock_response):
            method.parse()

        # Check if result_response is None
        self.assertIsNone(method.result_response)


if __name__ == '__main__':
    unittest.main()