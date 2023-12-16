from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select

import subprocess
from config import URL

HOME = "http://" + URL


def test_home_page_elements():
    subprocess.run(["python", "amazon.py", "&"])
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(HOME)
    driver.maximize_window()

    """ Check for links and form elements """
    home_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Home")
    driver.find_element(By.PARTIAL_LINK_TEXT, "Time")
    driver.find_element(By.PARTIAL_LINK_TEXT, "Date")

    age_form = driver.find_element(By.ID, "age-form")  # find age forms
    age_form.find_element(By.NAME, "date")
    age_form.find_element(By.NAME, "units")
    age_form.find_element(By.NAME, "submit-age")

    until_form = driver.find_element(By.ID, "until-form")  # until form
    until_form.find_element(By.NAME, "meal")
    until_form.find_element(By.NAME, "submit-until")

    """ Select links, check title, and return """
    home_link.click()

    driver.find_element(By.PARTIAL_LINK_TEXT, "Time").click()
    assert "time" in driver.title.lower()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Home").click()

    driver.find_element(By.PARTIAL_LINK_TEXT, "Date").click()
    assert "date" in driver.title.lower()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Home").click()

    driver.find_element(By.ID, "until-form"). \
        find_element(By.NAME, "submit-until").click()
    assert "meal" in driver.title.lower()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Home").click()

    """ Go to error page if calendar entry invalid """
    driver.find_element(By.PARTIAL_LINK_TEXT, "Home").click()
    age_form = driver.find_element(By.ID, "age-form")  # age form
    date_pick = age_form.find_element(By.NAME, "date")
    date_pick.click()  # select input
    date_pick.clear()  # clear any previous input
    date_pick.send_keys("032611111")
    age_form.find_element(By.NAME, "submit-age").click()
    assert "error" in driver.title.lower()
    driver.find_element(By.PARTIAL_LINK_TEXT, "Home").click()

    driver.close()
