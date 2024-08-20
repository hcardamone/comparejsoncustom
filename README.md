# CompareJsonCustom

`CompareJsonCustom` is a Python package designed to compare two JSON objects and check if one is a subset of the other, with the ability to ignore specified attributes during the comparison.

## Installation

To install the `CompareJsonCustom` package, follow these steps:

1. **Install Package**:
   ```bash
   pip install .
   ```

This command will install the package in your Python environment. Make sure you are in the root directory of the package where .\resources\custom_library\CompareJsonCustom\setup.py is located.

## Usage

After installing the CompareJsonCustom package, you can use it in your Python scripts as follows:

1. **Import the Class**

```python
    from CompareJsonCustom import CompareJsonCustom
```

2. **Create an Instance of the Class**

```python
    compare_json = CompareJsonCustom()
```

3. **Prepare Your JSON Data**

```python
subset = {
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

fullset = {
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
```

4. **Call the verify_json_content Method**

```python
try:
    result = compare_json.verify_json_content(subset, fullset)
    print("JSON verification result:", result)
except ValueError as e:
    print("Verification failed:", e)
The verify_json_content method will check if the subset is a subset of fullset. If there are missing keys or items, it will raise a ValueError.
```

## Example

Here is a complete example of how to use the CompareJsonCustom class in a Python script unit test:

```bash
cd ~/resources/custom_library/unitTest
$ python -m unittest TestCompareJsonCustom
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
