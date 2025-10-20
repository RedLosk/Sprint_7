import allure
import requests
import endpoints

class TestLoginCourier:
    @allure.title('Проверка, что курьер может авторизоваться')
    def test_login_courier_success(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера'):
            create_response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизация'):
            login_response = requests.post(endpoints.COURIER_LOGIN,
                                           data={"login": courier_data["login"], "password": courier_data["password"]})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert login_response.status_code == 200

    @allure.title('Нельзя авторизоваться без логина')
    def test_login_courier_without_login(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера через API'):
            create_response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизации без логина'):
            login_response = requests.post(endpoints.COURIER_LOGIN, data={"password": courier_data["password"]})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert login_response.json() == {"code": 400, "message": "Недостаточно данных для входа"}

    @allure.title('Проверка, что нельзя авторизоваться без пароля')
    def test_login_courier_without_password(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера'):
            create_response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизация без пароля'):
            password_response = requests.post(endpoints.COURIER_LOGIN, data={"login": courier_data["login"]})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert password_response.status_code == 504

    @allure.title('Проверка, что нельзя авторизоваться если логин не правильный')
    def test_login_courier_incorrect_login(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера'):
            create_response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизация с неправильным логином'):
            login_response = requests.post(endpoints.COURIER_LOGIN,
                                           data={"login": "wronglogin", "password": courier_data["password"]})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert login_response.json() == {"code": 404, "message": "Учетная запись не найдена"}

    @allure.title('Проверка, что нельзя авторизоваться если пароль неправильный')
    def test_login_courier_incorrect_password(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера'):
            create_response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизация с неправильным паролем'):
            password_response = requests.post(endpoints.COURIER_LOGIN,
                                              data={"login": courier_data["login"], "password": "wrongpassword"})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert password_response.json() == {"code": 404, "message": "Учетная запись не найдена"}

    @allure.title('Проверка, что нельзя авторизоваться под несуществующим курьером')
    def test_login_courier_wrong_user(self):
        with allure.step('Авторизация с несуществующим курьером'):
            response = requests.post(endpoints.COURIER_LOGIN,
                                     data={"login": "wronglogin1985", "password": "wrongpassword1074"})
        assert response.json() == {"code": 404, "message": "Учетная запись не найдена"}

    @allure.title('Успешная авторизация возвращает id')
    def test_login_courier_success_return_id(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера через API'):
            create_response = requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизация'):
            login_response = requests.post(endpoints.COURIER_LOGIN,
                                           data={"login": courier_data["login"], "password": courier_data["password"]})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert "id" in login_response.json()

    @allure.title("Системная ошибка, если логин пустой")
    def test_login_with_empty_login(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера'):
            requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизация с пустым логином'):
            response = requests.post(endpoints.COURIER_LOGIN, data={"login": "", "password": courier_data["password"]})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}

    @allure.title("Системная ошибка, если пароль пустой")
    def test_login_with_empty_password(self, courier_data, courier_cleanup):
        with allure.step('Создание курьера'):
            requests.post(endpoints.COURIER_CREATE, data=courier_data)

        with allure.step('Авторизация с пустым паролем'):
            response = requests.post(endpoints.COURIER_LOGIN, data={"login": courier_data["login"], "password": ""})

        with allure.step('Удаление курьера'):
            courier_cleanup.append(courier_data)
        assert response.json() == {"code": 400, "message": "Недостаточно данных для входа"}