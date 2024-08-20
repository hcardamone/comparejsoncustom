import unittest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CompareJsonCustom')))

from CompareJsonCustom import CompareJsonCustom

class TestCompareJsonCustom(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Sets up the environment for all tests"""
        cls.compare_json = CompareJsonCustom()
        cls.subset = {
            "order_id": "12345",
            "customer": {
                "name": "John Doe",
                "email": "john.doe@example.com"
            },
            "items": [
                {"product_id": "abc", "quantity": 2}
            ]
        }
        cls.fullset = {
            "order_id": "12345",
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
    
    def print_json(self, label, data):
        """Helper method to print JSON data"""
        print(f"{label}:")
        print(json.dumps(data, indent=2))
    
    def print_test_info(self):
        """Helper method to print the current test function name"""
        test_name = self._testMethodName
        print(f"\n==============================================================================")
        print(f"Running test: {test_name}")
    
    def print_test_result(self, success):
        """Helper method to print the result of the test"""
        result = "PASSED" if success else "FAILED"
        print(f"Test '{self._testMethodName}' {result}.")
        print(f"==============================================================================\n")
    
    def test_verify_json_content_success(self):
        """Test when the JSON subset is a subset of the fullset"""
        self.print_test_info()
        self.print_json("Subset", self.subset)
        self.print_json("Fullset", self.fullset)
        
        try:
            result = self.compare_json.is_json_subset(self.subset, self.fullset)
            self.assertTrue(result)
            self.print_test_result(success=True)
        except ValueError:
            self.print_test_result(success=False)
            self.fail("is_json_subset raised ValueError unexpectedly!")
    
    def test_remove_ignored_attributes(self):
        """Test the removal of ignored attributes"""
        self.print_test_info()
        data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "admin",
                "password": "password"
            },
            "api": {
                "endpoint": "https://api.example.com",
                "timeout": 30
            }
        }
        ignore_attributes = {
            "database": ["password"]
        }
        
        self.compare_json.remove_ignored_attributes(data, ignore_attributes)
        
        expected_data = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "admin"
            },
            "api": {
                "endpoint": "https://api.example.com",
                "timeout": 30
            }
        }
        
        self.print_json("Processed Data", data)
        self.assertEqual(data, expected_data)
        self.print_test_result(success=(data == expected_data))
    
    def test_is_json_subset(self):
        """Test if a JSON is a subset of another"""
        self.print_test_info()
        self.print_json("Subset", self.subset)
        self.print_json("Fullset", self.fullset)
        
        self.compare_json.is_json_subset(self.subset, self.fullset)
        self.assertEqual(self.compare_json.missing_keys, [])
        self.print_test_result(success=(self.compare_json.missing_keys == []))
    
    def test_is_json_subset_missing_key(self):
        """Test when a JSON has a missing key"""
        self.print_test_info()
        subset = {
            "order_id": "12345",
            "customer": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "age": 30
            }
        }
        fullset = self.fullset  # Reuse the fullset defined in setUpClass
        
        self.print_json("Subset", subset)
        self.print_json("Fullset", fullset)
        
        self.compare_json.is_json_subset(subset, fullset)
        expected_missing_keys = [{"path": "root.customer.age", "expected": 30, "found": None}]
        self.assertEqual(self.compare_json.missing_keys, expected_missing_keys)
        self.print_test_result(success=(self.compare_json.missing_keys == expected_missing_keys))
    
    def test_is_json_subset_missing_item(self):
        """Test when an item is missing in a list"""
        self.print_test_info()
        subset = [
            {"product_id": "item789", "quantity": 50}
        ]
        fullset = [
            {"product_id": "item789", "quantity": 50},
            {"product_id": "item790", "quantity": 30}
        ]
        
        self.print_json("Subset", subset)
        self.print_json("Fullset", fullset)
        
        self.compare_json.is_json_subset(subset, fullset)
        self.assertEqual(self.compare_json.missing_keys, [])
        self.print_test_result(success=(self.compare_json.missing_keys == []))


class CustomTextTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        """Prints additional information when a test passes"""
        super().addSuccess(test)
        print(f"Test '{test}' PASSED.")
        print(f"==============================================================================\n")

    def addFailure(self, test, err):
        """Prints additional information when a test fails"""
        super().addFailure(test, err)
        print(f"Test '{test}' FAILED.")
        print(f"Error: {err}")
        print(f"==============================================================================\n")

    def addError(self, test, err):
        """Prints additional information when a test encounters an error"""
        super().addError(test, err)
        print(f"Test '{test}' ERROR.")
        print(f"Error: {err}")
        print(f"==============================================================================\n")


class CustomTextTestRunner(unittest.TextTestRunner):
    """Custom test runner to use the CustomTextTestResult class"""
    resultclass = CustomTextTestResult


if __name__ == '__main__':
    unittest.main(testRunner=CustomTextTestRunner())
