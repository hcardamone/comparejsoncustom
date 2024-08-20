import json
import logging

# Logger configuration to display in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompareJsonCustom:
    def __init__(self):
        # Initialize the list of missing keys and the dictionaries for ignored fields and attributes
        self.missing_keys = []
        self.ignore_fields = {}
        self.ignore_attributes = {}

    def verify_json_content(self, subset, fullset, ignore_fields_file=None, ignore_attributes_file=None):
        self.missing_keys = []

        # Load ignored fields from a file or dictionary
        if isinstance(ignore_fields_file, dict):
            self.ignore_fields = ignore_fields_file
        elif isinstance(ignore_fields_file, str):
            with open(ignore_fields_file, 'r') as f:
                self.ignore_fields = json.load(f)
        else:
            self.ignore_fields = {}

        # Load ignored attributes from a file or dictionary
        if isinstance(ignore_attributes_file, dict):
            self.ignore_attributes = ignore_attributes_file
        elif isinstance(ignore_attributes_file, str):
            with open(ignore_attributes_file, 'r') as f:
                self.ignore_attributes = json.load(f)
        else:
            self.ignore_attributes = {}

        # Remove ignored attributes and fields from both JSONs
        self.remove_ignored_fields(subset, fullset, self.ignore_fields)
        self.remove_ignored_attributes(subset, fullset, self.ignore_attributes)
        
        # Check if the subset is a subset of the fullset
        self.is_json_subset(subset, fullset)

        # Log the JSONs and results
        logger.info(f"JSON Request: {json.dumps(subset, indent=2)}")
        logger.info(f"JSON Reference: {json.dumps(fullset, indent=2)}")

        if self.missing_keys:
            logger.info("Missing keys or items found:")
            missing_json = {"missing": self.missing_keys}
            logger.info(json.dumps(missing_json, indent=2))
            logger.info(f"Total missing keys or items: {len(self.missing_keys)}")

            raise ValueError(
                "JSON content validation failed. "
                "Missing keys or items found. See log for details."
            )

        logger.info("The JSON request content is valid.")
        return True

    def is_json_subset(self, subset, fullset, path="root"):
        # Check if the subset is a valid subset of the fullset
        if isinstance(subset, dict) and isinstance(fullset, dict):
            for key, value in subset.items():
                if key not in fullset:
                    self.missing_keys.append(
                        {"path": f"{path}.{key}", "expected": value, "found": None}
                    )
                else:
                    self.is_json_subset(value, fullset[key], path=f"{path}.{key}")
        elif isinstance(subset, list) and isinstance(fullset, list):
            for item in subset:
                item_found = False
                for full_item in fullset:
                    if self.is_json_subset(item, full_item, path=path):
                        item_found = True
                        break
                if not item_found:
                    self.missing_keys.append(
                        {"path": f"{path}", "expected": item, "found": None}
                    )
        else:
            if subset != fullset:
                self.missing_keys.append(
                    {"path": f"{path}", "expected": subset, "found": fullset}
                )

        return True

    def remove_ignored_attributes(self, subset, fullset, ignore_attributes):
        # Remove ignored attributes from both JSONs
        if isinstance(subset, dict) and isinstance(fullset, dict):
            for key in list(subset.keys()):
                if key in ignore_attributes:
                    ignored_attrs = ignore_attributes[key]
                    if isinstance(ignored_attrs, list):
                        if isinstance(subset[key], dict):
                            for attr in ignored_attrs:
                                subset[key].pop(attr, None)
                                fullset[key].pop(attr, None)
                        elif isinstance(subset[key], list):
                            for item1, item2 in zip(subset[key], fullset[key]):
                                if isinstance(item1, dict) and isinstance(item2, dict):
                                    for attr in ignored_attrs:
                                        item1.pop(attr, None)
                                        item2.pop(attr, None)
        # Process nested data recursively
                self.remove_ignored_attributes(subset[key], fullset[key], ignore_attributes)
        elif isinstance(subset, list) and isinstance(fullset, list):
            for item1, item2 in zip(subset, fullset):
                self.remove_ignored_attributes(item1, item2, ignore_attributes)

    def remove_ignored_fields(self, subset, fullset, ignore_fields):
        # Remove ignored fields from both JSONs
        if isinstance(subset, dict) and isinstance(fullset, dict):
            for key in list(subset.keys()):
                if key in ignore_fields:
                    del subset[key]
                    del fullset[key]
                else:
                    self.remove_ignored_fields(subset[key], fullset[key], ignore_fields)
        elif isinstance(subset, list) and isinstance(fullset, list):
            for item1, item2 in zip(subset, fullset):
                self.remove_ignored_fields(item1, item2, ignore_fields)
