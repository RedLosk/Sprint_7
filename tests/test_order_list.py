import allure
import requests
import endpoints

class TestGetOrder:

    @allure.title('Получение списка заказа')
    def test_get_orders_list(self):

        with allure.step('Получение списка заказа'):
            response = requests.get(endpoints.ORDER_CREATE)

        assert isinstance(response.json()["orders" ], list)