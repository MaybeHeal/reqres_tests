from selenium.webdriver.common.by import By


class ReqresLocators:
    REQUESTS_LIST = (By.CSS_SELECTOR, '.endpoints > ul > li')
    REQUEST_URL = (By.CSS_SELECTOR, '[data-key="url"]')
    RESPONSE_STATUS_CODE = (By.CSS_SELECTOR, '.response-code')
    OUTPUT_RESPONSE = (By.CSS_SELECTOR, '[data-key="output-response"]')
    OUTPUT_REQUEST = (By.CSS_SELECTOR, '[data-key="output-request"]')
