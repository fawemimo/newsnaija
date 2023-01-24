import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase

@pytest.fixture(scope="module")
def chrome_browser_instance(request):

    options = webdriver.ChromeOptions()
    options.headless = False
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.close()
