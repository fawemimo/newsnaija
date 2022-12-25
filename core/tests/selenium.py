import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module")
def chrome_browser_instance(request):

    options = Options()
    options.headless = False
    browser = webdriver.Chrome(options=Options())
    yield browser
    browser.close()
