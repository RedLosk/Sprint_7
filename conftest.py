import pytest
import string
import random
import requests
import endpoints

@pytest.fixture()
def courier_data():
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    return {"login" : generate_random_string(), "password" : generate_random_string(), "firstName" : generate_random_string()}


@pytest.fixture()
def courier_cleanup():
    created_couriers = []

    yield created_couriers

    for courier in created_couriers:
        login_response = requests.post(endpoints.COURIER_LOGIN, data={"login" : courier["login"], "password" : courier["password"]})
        courier_id = login_response.json()["id"]
        delete_url = endpoints.COURIER_DELETE.format(id = courier_id)
        requests.delete(delete_url)
