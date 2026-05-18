import threading
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from app import create_app

BASE_URL = "http://127.0.0.1:5000"
server_thread = None


def ensure_server_running():
    global server_thread

    if server_thread and server_thread.is_alive():
        return

    app = create_app()

    def run():
        app.run(port=5000)

    server_thread = threading.Thread(target=run, daemon=True)
    server_thread.start()

    for _ in range(30):
        try:
            requests.get(BASE_URL)
            return
        except Exception:
            time.sleep(0.2)

    raise RuntimeError("Flask server failed to start for E2E tests")


def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def test_create_user_e2e_wait():
    ensure_server_running()
    driver = get_driver()
    wait = WebDriverWait(driver, 5)

    try:
        driver.get(BASE_URL)

        input_name = wait.until(lambda d: d.find_element(By.ID, "name"))
        input_name.send_keys("Maylon")

        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Maylon" in d.find_element(By.ID, "users").text)

        users = driver.find_element(By.ID, "users").text
        assert "Maylon" in users

    finally:
        driver.quit()


def test_e2e_create_user_vinicius():
    ensure_server_running()
    driver = get_driver()
    wait = WebDriverWait(driver, 5)

    try:
        driver.get(BASE_URL)

        driver.find_element(By.ID, "name").send_keys("Vinicius Souza")
        driver.find_element(By.ID, "submit").click()

        wait.until(lambda d: "Vinicius Souza" in d.find_element(By.ID, "users").text)

        assert "Vinicius Souza" in driver.find_element(By.ID, "users").text

    finally:
        driver.quit()


def test_e2e_multiple_users():
    ensure_server_running()
    driver = get_driver()
    wait = WebDriverWait(driver, 5)

    try:
        driver.get(BASE_URL)

        for name in ["Paulo Cesar", "João Lima"]:
            input_box = driver.find_element(By.ID, "name")
            input_box.clear()
            input_box.send_keys(name)
            driver.find_element(By.ID, "submit").click()

        wait.until(
            lambda d: "Paulo Cesar" in d.find_element(By.ID, "users").text
            and "João Lima" in d.find_element(By.ID, "users").text
        )

        users = driver.find_element(By.ID, "users").text

        assert "Paulo Cesar" in users
        assert "João Lima" in users

    finally:
        driver.quit()
