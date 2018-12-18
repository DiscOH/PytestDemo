import pytest
from selenium import webdriver
from demo_libraries import selenium_library


@pytest.fixture(scope='class')
def chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    with webdriver.Chrome(options=options) as driver:
        yield driver


@pytest.fixture(scope='class')
def chrome_session(chrome_driver, request):
    yield selenium_library.Session(chrome_driver, request)
