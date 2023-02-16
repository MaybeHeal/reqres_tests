import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators import ReqresLocators
from reqres_api import get_request, post_request, put_request, patch_request, delete_request


def check_request_status_code(browser, api_request, expected, data):
    # Создание явного ожидания для браузера до 5сек
    wait = WebDriverWait(browser, 5)

    # Поиск необходимого API запроса в браузере по data-id
    request_element = browser.find_element(By.CSS_SELECTOR, f'[data-id="{api_request}"]')

    # Список всех используемых API запросов
    requests_list = {'get': get_request,
                     'post': post_request,
                     'put': put_request,
                     'patch': patch_request,
                     'delete': delete_request}

    # Переход в браузере к необходимому API запросу
    request_element.click()

    # Ожидание появления элемента с ответом на запрос
    wait.until(EC.visibility_of_element_located(ReqresLocators.OUTPUT_RESPONSE))

    # Получение атрибуса data-http в котором указан вид запроса
    request_type = request_element.get_attribute('data-http')

    # Получение элемента из списка с необходимой функцией запроса
    response = requests_list[request_type]

    # Получение ссылки для отправки запроса
    request_url = browser.find_element(*ReqresLocators.REQUEST_URL).text

    # Если данные для отправки запроса не пустые, то они добавляются в вызов функции
    if data is None:
        actual = response(request_url)
    else:
        actual = response(request_url, data)

    # Сравнение результатов
    assert actual.status_code == expected, f'Status codes do not match. AR: {actual.status_code}, ER: {expected}'

    # Преобразование полученного ответа в текст
    actual = actual.text

    # Если ответ не пустой, то происходит преобразование в JSON формат
    if actual:
        actual = json.loads(actual)
    return actual


def check_response_output(browser, response):
    # Получение ответа на запрос и преобразование его в текст
    web_response = browser.find_element(*ReqresLocators.OUTPUT_RESPONSE).text

    # Если ответ не пустой, то происходит преобразование в JSON формат
    if web_response:
        web_response = json.loads(web_response)

    # Сравнение результатов
    assert response == web_response, f'Responses do not match. Response: {response} Web_response: {web_response}'
