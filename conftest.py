import pytest
from selenium import webdriver


@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    browser.get('https://reqres.in')
    yield browser
    browser.quit()
