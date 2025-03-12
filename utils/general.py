from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .chatgpt_req import ChatGPT
from selenium.webdriver.common.by import By


class GeneralParse:
    def __init__(self, login: str, password: str, wait: int = 4):
        self.login = login
        self.password = password
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, wait)
        self.chatgpt = ChatGPT()


    def login_page(self):
        """Метод для входа на страницу авторизации."""
        try:
            login_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
            login_input.send_keys(self.login)

            password_input = self.driver.find_element(By.XPATH, '//*[@id="password"]')
            password_input.send_keys(self.password)

            login_button = self.driver.find_element(By.XPATH, '//*[@id="loginbtn"]')
            login_button.click()
            print("Вход выполнен успешно.")
        except Exception:
            print("Ошибка при входе в систему.")

    def close_driver(self):
        """Метод для закрытия драйвера."""
        self.driver.quit()


    def find_answer(self, question_text: str, answers: list) -> str:
        """Определяет правильный ответ на вопрос.
        :param question_text: str - текст вопроса
        :param answers: list - список вариантов ответов
        :return: str - правильный ответ
        """
        text = question_text + '\n' + '\n'.join(answers)
        return self.chatgpt.get_answer(text)

    def start_test_loop(self, url: str) -> None:
        """Запускает цикл прохождения теста.
        :param url: str - URL страницы с тестом
        """
        self.driver.get(url)
        if self.driver.current_url != url:
            self.login_page()
            self.driver.get(url)

        while True:
            if not self.test_solution():
                break
