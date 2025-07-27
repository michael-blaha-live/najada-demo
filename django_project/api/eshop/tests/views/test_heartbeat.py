import pytest
from rest_framework.test import APIClient


class TestGetHeartBeat:
    def test_get_heartbeat(self, api_client):
        """
        GIVEN no DoughType instances exist in the database
        WHEN a GET request is made to /heartbeat
        THEN the API should return an 'healthy': True with 200 OK status.
        """
        response = api_client.get('/api/eshop/heartbeat/')

        assert response.status_code == 200
        assert response.json() == {'healthy': True}
