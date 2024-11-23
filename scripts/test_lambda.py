import json
import requests
import base64
import sys
from pprint import pprint as pp


def invoke_lambda(payload, port=9000):
    """
    Invokes the local Lambda function using the Lambda Runtime Interface Emulator
    """
    # Convert payload to base64 if it's a string
    if isinstance(payload, str):
        payload = {"body": payload}

    # Convert payload to JSON string
    payload_json = json.dumps(payload)

    # Endpoint for Lambda Runtime Interface Emulator
    url = f"http://localhost:{port}/2015-03-31/functions/function/invocations"

    try:
        # Make the request to the local Lambda
        response = requests.post(url, data=payload_json)

        # Check if request was successful
        response.raise_for_status()

        # Parse and return the response
        return response.json()

    except requests.exceptions.RequestException as e:
        pp(f"Error invoking Lambda: {str(e)}")
        sys.exit(1)


def main():
    # Sample test payloads
    test_cases = [
        {"name": "Simple string payload", "payload": "Hello World"},
        {
            "name": "JSON payload",
            "payload": {
                "message": "Test message",
                "data": {"key1": "value1", "key2": "value2"},
            },
        },
        {
            "name": "API Gateway payload",
            "payload": {
                "resource": "/test",
                "path": "/test",
                "httpMethod": "POST",
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "Test message"}),
            },
        },
    ]

    # Run test cases
    for test_case in test_cases:
        pp(f"\nRunning test case: {test_case['name']}")
        pp("-" * 50)

        response = invoke_lambda(test_case["payload"])
        pp(f"Response: {json.dumps(response, indent=2)}")
        pp("-" * 50)


if __name__ == "__main__":
    main()
