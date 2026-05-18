from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# Teste correto usando wait
def test_create_user_e2e_wait():

    driver = webdriver.Chrome()

    driver.get("http://localhost:5000")

    input_name = driver.find_element(By.ID, "name")
    input_name.send_keys("Maylon")

    driver.find_element(By.ID, "submit").click()

    from selenium.webdriver.support.ui import WebDriverWait

    wait = WebDriverWait(driver, 5)

    wait.until(
        lambda d: any("Maylon" in el.text for el in d.find_elements(By.TAG_NAME, "li"))
    )

    users = driver.find_elements(By.TAG_NAME, "li")

    assert any("Maylon" in user.text for user in users)

    driver.quit()

# NOVOS TESTES E2E
def test_e2e_create_user_vinicius():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000")

    driver.find_element(By.ID, "name").send_keys("Vinicius Souza")
    driver.find_element(By.ID, "submit").click()

    wait = WebDriverWait(driver, 5)
    wait.until(lambda d: "Vinicius Souza" in d.page_source)

    assert "Vinicius Souza" in driver.page_source
    driver.quit()


def test_e2e_multiple_users():
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000")

    for name in ["Paulo Cesar", "João Lima"]:
        input_box = driver.find_element(By.ID, "name")
        input_box.clear()
        input_box.send_keys(name)
        driver.find_element(By.ID, "submit").click()

    wait = WebDriverWait(driver, 5)
    wait.until(lambda d: "Paulo Cesar" in d.page_source and "João Lima" in d.page_source)

    assert "Paulo Cesar" in driver.page_source
    assert "João Lima" in driver.page_source

    driver.quit()