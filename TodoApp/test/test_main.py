'''
    allows us to create an instance of the app and test it to see if it runs  
	1.	from fastapi.testclient import TestClient:
	•	This part of the statement is used to import the TestClient class from the fastapi.testclient module.
	•	TestClient is a testing client provided by FastAPI that allows you to make requests to your FastAPI application as if you were a client. This is particularly useful for writing unit tests and integration tests for your API endpoints.
	2.	as TestClient:
	•	The as TestClient part of the statement creates an alias for the imported TestClient class. In this case, the alias is the same as the original class name, which might seem redundant. However, this is sometimes done to maintain naming consistency within the code or to avoid conflicts with other imported classes or functions with the same name.
'''

from fastapi.testclient import TestClient as TestClient
# imports our main file into this file
import main
# using status to check if everything is running as expected  
from fastapi import status
# client becomes an instance of our application like app and calls on our application
client = TestClient(main.app)

# we need to install pip i httpx

def test_return_health_check():
    response = client.get('/healthy')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}