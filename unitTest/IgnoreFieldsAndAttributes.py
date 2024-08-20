import unittest
import json
import sys
import os

# Add the path to the CompareJsonCustom module to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'CompareJsonCustom')))

from CompareJsonCustom import CompareJsonCustom

class TestCompareJsonCustom(unittest.TestCase):

    def test_removal(self):
        # Define a sample JSON data structure
        json_reference_data = {
            "isAudit": False,
            "rsltLvl": 1,
            "currn": "USD",
            "docDt": "2024-08-07",
            "txCalcTp": 1,
            "trnDocNum": "",
            "lines": [
                {
                    "debCredIndr": 1,
                    "goodSrvCd": "2039082",
                    "grossAmt": 7602.00,
                    "lnItmId": "1",
                    "lnItmNum": 10,
                    "qnty": 2,
                    "qntyUMCd": "ST",
                    "trnTp": 1,
                    "custVendCd": "0000300025",
                    "orgCd": "HANA3000",
                    "dlvrAmt": 0.00,
                    "dlvrDt": "2024-08-07",
                    "dropShipInd": 3,
                    "bTGeoCd": 1914,
                    "lOAGeoCd": 22831,
                    "lORGeoCd": 1914,
                    "lSPGeoCd": 1914,
                    "lUGeoCd": 1914,
                    "sFGeoCd": 22831,
                    "sTGeoCd": 1914
                }
            ],
            "tdcReqrd": True,
            "tdmRequired": True
        }

        json_expected_data = {
            "isAudit": False,
            "rsltLvl": 1,
            "currn": "USD",
            "docDt": "2024-08-07",
            "txCalcTp": 1,
            "trnDocNum": "",
            "lines": [
                {
                    "debCredIndr": 1,
                    "goodSrvCd": "2039082",
                    "grossAmt": 7602.00,
                    "lnItmId": "1",
                    "lnItmNum": 10,
                    "qnty": 2,
                    "qntyUMCd": "ST",
                    "trnTp": 1,
                    "custVendCd": "0000300025",
                    "orgCd": "HANA3000",
                    "dlvrAmt": 0.00,
                    "dlvrDt": "2024-08-07",
                    "dropShipInd": 3,
                    "bTGeoCd": 1914,
                    "lOAGeoCd": 22831,
                    "lORGeoCd": 1914,
                    "lSPGeoCd": 1914,
                    "lUGeoCd": 1914,
                    "sFGeoCd": 22831,
                    "sTGeoCd": 1914
                }
            ],
            "tdcReqrd": True,
            "tdmRequired": True
        }

        # Define the fields to ignore during the removal process
        ignore_fields = {
            "isAudit": [""],
            "docDt": [""],
            "trnDocNum": [""]
        }

        # Define the attributes to ignore during the removal process
        ignore_attributes = {
            "lines": ["dlvrDt"]
        }

        # Instanciar a classe CompareJsonCustom
        compare_json = CompareJsonCustom()

        # Print JSON data before removal
        print("Request JSON data before removal:")
        print(json.dumps(json_reference_data, indent=2))
        print("Expected Results JSON data before removal:")
        print(json.dumps(json_expected_data, indent=2))

        # Pass ignore_fields and ignore_attributes to the removal functions
        compare_json.remove_ignored_fields(json_reference_data, json_expected_data, ignore_fields)
        compare_json.remove_ignored_attributes(json_reference_data, json_expected_data, ignore_attributes)

        # Print JSON data after removal
        print("Request JSON data after removal:")
        print(json.dumps(json_reference_data, indent=2))
        print("Expected Results JSON data after removal:")
        print(json.dumps(json_expected_data, indent=2))

if __name__ == "__main__":
    unittest.main()
