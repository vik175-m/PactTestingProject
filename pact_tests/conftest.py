import pytest
from pact import Consumer, Provider

# Create a consumer and a provider
pact = Consumer('UserClient').has_pact_with(Provider('UserService'), port=1235)

# Where to store the pact files and enable logging for pact service
pact.log_dir = "./pact_logs"
pact.pact_dir = "./pacts"
pact.verbose = True

@pytest.fixture
def consumer_pact():
    """
    Fixture to start and stop the mock service.
    """
    pact.start_service()  # Start the mock service
    yield pact
    pact.stop_service()   # Stop the mock service after tests