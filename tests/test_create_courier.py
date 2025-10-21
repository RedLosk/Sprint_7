import allure
import requests
import endpoints

class TestCrearionCourier:
    @allure.title('Успешное создание курьера, корректный код ответа')
    def test_create_courier_success_correct_answer_code(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера'):
            response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert response.status_code == 201

    @allure.title('Успешное создание курьера, корректное тело ответа')
    def test_create_courier_success_correct_answer_body(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера через API'):
            response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert response.json() == {"ok": True}


    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier(self, courier_data, courier_cleanup):
        with allure.step('Создание первого курьера'):
            response1 = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Создание второго курьера'):
            response2 = requests.post(endpoints.COURIER_CREATE, data=courier_data)
            with allure.step('Удаление курьера'):
                courier_cleanup.append(courier_data)

            assert response2.json() == {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}

    @allure.title('Проверка, что нельзя создать курьера без логина')
    def test_create_courier_without_login(self, courier_data):
        payload = courier_data.copy()
        del payload["login"]

        with allure.step('Cоздание курьера без логина'):
            response = requests.post(endpoints.COURIER_CREATE, data=payload)

        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

    @allure.title('Проверка, что нельзя создать курьера без пароля')
    def test_create_courier_missing_password(self, courier_data):
        payload = courier_data.copy()
        del payload["password"]

        with allure.step('Cоздание курьера без пароля'):
            response = requests.post(endpoints.COURIER_CREATE, data=payload)

        assert response.json() == {"code": 400, "message": "Недостаточно данных для создания учетной записи"}