import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


@pytest.mark.selenium
def test_admin_login(live_server, db_fixture_setup, chrome_browser_instance):

    browser = chrome_browser_instance

    browser.get(("%s%s" % (live_server.url, "/admin/login/")))

    username = browser.find_element(By.NAME, "username")
    password = browser.find_element(By.NAME, "password")
    submit = browser.find_element(By.XPATH, '//input[@value="Log in"]')

    username.send_keys("admin")
    password.send_keys("admin01")
    submit.send_keys(Keys.RETURN)

    assert "Site adminstration" in browser.page_source
