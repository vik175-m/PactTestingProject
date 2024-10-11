import requests
import pytest
from utils.myutils import load_test_data
from jsonschema import validate, ValidationError

def test_get_users(consumer_pact):
    """
    Consumer test to request a list of users from the provider.
    """
    expected_users = load_test_data('/Users/vikashmishra/Desktop/PactTestingProject/test_data/expected_data.json')
    user_schema = load_test_data('/Users/vikashmishra/Desktop/PactTestingProject/test_data/user_schema.json')

    # Define the expected interaction between the consumer and provider
    (consumer_pact
     .given('Users exist')
     .upon_receiving('a request for users')
     .with_request('get', '/api/users', query={'page': "1"})
     .will_respond_with(200, body=expected_users))

    # API call to the mock service
    with consumer_pact:
        result = requests.get('http://localhost:1235/api/users', params={'page': "1"})

    # Print the actual response
    print("Actual response JSON:", result.json())

    # Print the status code
    print("Status Code:", result.status_code)

    # Validate the response against the JSON schema
    try:
        validate(instance=result.json(), schema=user_schema)
        print("JSON schema validation passed.")
    except ValidationError as e:
        pytest.fail(f"Response did not match schema: {e.message}")

    # Compare the full response with expected data
    assert result.status_code == 200
    assert result.json() == expected_users