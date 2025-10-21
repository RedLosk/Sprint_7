import pytest
import allure
import requests
import endpoints
from helpers import order_data

class TestCreationOrder:
    @allure.title('Cоздания заказа с разными цветами')
    @pytest.mark.parametrize("color_option", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_creation_order_using_color(self, color_option):

        order_data_with_color = order_data()
        order_data_with_color["color"] = color_option

        with allure.step('Создание заказа'):
            response = requests.post(endpoints.ORDER_CREATE, json=order_data_with_color)

        assert  "track" in response.json()
