import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CompareJsonCustom')))

import unittest
import json
import logging
from CompareJsonCustom import CompareJsonCustom

class TestCompareJsonCustomFailure(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up the environment for all tests"""
        cls.compare_json = CompareJsonCustom()
        cls.subset = {
            "order_id": "12345",
            "customer": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "555-4321"
            },
            "items": [
                {"product_id": "XYZ", "quantity": 2}
            ]
        }
        cls.fullset = {
            "order_id": "54321",
            "customer": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "555-1234"
            },
            "items": [
                {"product_id": "abc", "quantity": 2},
                {"product_id": "def", "quantity": 1}
            ],
            "shipping_address": {
                "street": "123 Elm St",
                "city": "Somewhere",
                "state": "CA",
                "zip": "90210"
            }
        }
        # Configure logger
        cls.logger = logging.getLogger("TestCompareJsonCustom")
        cls.logger.setLevel(logging.INFO)

    def print_json(self, label, data):
        """Helper method to print JSON data"""
        self.logger.debug(f"{label}:")
        self.logger.debug(json.dumps(data, indent=2))
        self.logger.debug("\n" + "=" * 78)

    def print_test_info(self):
        """Helper method to print the current test function name"""
        test_name = self._testMethodName
        print("\n" + "=" * 78)
        print(f"Running test: {test_name}")

    def print_test_result(self, success):
        """Helper method to print the test result"""
        result = "PASSED" if success else "FAILED"
        print(f"Test '{self._testMethodName}' {result}.")
        print("=" * 78 + "\n")

    def test_verify_json_content(self):
        """Test when the JSON subset is a subset of the full set"""
        self.print_test_info()
        self.print_json("Subset", self.subset)
        self.print_json("Fullset", self.fullset)
        
        try:
            result = self.compare_json.verify_json_content(self.subset, self.fullset)
            if not result:
                print("Differences found:")
                for diff in self.compare_json.missing_keys:
                    print(diff)
            self.assertTrue(result)
            self.print_test_result(success=True)
        except ValueError as e:
            print(e)
            self.print_test_result(success=False)
            self.fail("verify_json_content raised ValueError unexpectedly!")

class CustomTextTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        """Prints additional information when a test passes"""
        super().addSuccess(test)
        print(f"Test '{test}' PASSED.")
        print("=" * 78 + "\n")

    def addFailure(self, test, err):
        """Prints additional information when a test fails"""
        super().addFailure(test, err)
        print(f"Test '{test}' FAILED.")
        print(f"Error: {err}")
        print("=" * 78 + "\n")

    def addError(self, test, err):
        """Prints additional information when a test encounters an error"""
        super().addError(test, err)
        print(f"Test '{test}' ERROR.")
        print(f"Error: {err}")
        print("=" * 78 + "\n")

class CustomTextTestRunner(unittest.TextTestRunner):
    """Custom test runner to use the CustomTextTestResult class"""
    resultclass = CustomTextTestResult

if __name__ == '__main__':
    unittest.main(testRunner=CustomTextTestRunner())
