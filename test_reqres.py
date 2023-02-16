import json

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators import ReqresLocators
from reqres_func import check_request_status_code, check_response_output


def api_requests():
    """
        Функция для парсинга API запросов с сайта.
        Возвращает список кортежей с данными для использования в параметризации теста.
    """
    # Открытие браузера
    browser = webdriver.Chrome()

    # Переход по ссылке
    browser.get('https://reqres.in')

    # Создание явного ожидания для браузера до 5сек
    wait = WebDriverWait(browser, 5)

    # Список элементов с API запросами
    list_requests = browser.find_elements(*ReqresLocators.REQUESTS_LIST)
    param_list = []

    # Цикл для составления списка кортежей. Кортежи имеют вид: (<Запрос>, <статус код>, <данные для отправки в запросе>)
    for element in list_requests:

        # Переход к нужно API в браузере
        element.click()

        # Получение уникального data-id запроса на сайте
        element_data_id = element.get_attribute('data-id')

        # Ожидание появления элемента с ответом на запрос
        wait.until(EC.visibility_of_element_located(ReqresLocators.OUTPUT_RESPONSE))

        # Получение статус кода, который должен быть получен при запросе
        response_code = int(browser.find_element(*ReqresLocators.RESPONSE_STATUS_CODE).text)

        # Получение данных для отправки в запросе, если имеются
        if browser.find_element(*ReqresLocators.OUTPUT_REQUEST).get_attribute('hidden'):
            data = None
        else:
            data = json.loads(browser.find_element(*ReqresLocators.OUTPUT_REQUEST).text)

        # Создание кортежа и добавление его в список
        param_tuple = (element_data_id, response_code, data)
        param_list.append(tuple(param_tuple))

    # Закрытие браузера
    browser.quit()
    return param_list


# Список кортежей для использования в параметризации
request_list = api_requests()


@pytest.mark.parametrize('api_request, status_code, data', request_list)
def test_api_request(browser, api_request, status_code, data):
    # Step 1: Проверка возврата необходимых статус кодов в API запросе
    response = check_request_status_code(browser, api_request, status_code, data)

    # Step 2: Сравнение полученных данных из Step 1 с данными на сайте
    check_response_output(browser, response)
