import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chatgpt_req import ChatGPT
from typing import Union

class Parse:
    def __init__(self, login: str, password: str):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 2)
        self.login = login
        self.password = password
        self.chatgpt = ChatGPT()

    def start_test_loop(self, url: str):
        """Запускает цикл прохождения теста."""
        self.driver.get(url)
        if self.driver.current_url != url:
            self.login_page()
            self.driver.get(url)

        while True:
            if not self.test_solution():
                break

    def test_solution(self):
        """Решает один вопрос теста и переходит к следующему."""
        try:
            self.handle_continue_button()
            
            question_text, answers = self.find_elements_tests()
            if not question_text or not answers:
                print("Тест завершен или вопрос не найден.")
                result = input("Введите ! для выхода...")
                if result == "!":
                    return False
                else:
                    return True

            correct_answer = self.find_answer(question_text, answers)
            if correct_answer in answers:
                index = answers.index(correct_answer)
                answer_elements = self.driver.find_elements(By.CLASS_NAME, "form-check-label")
                answer_elements[index].click()
                print(f"Выбран ответ: {correct_answer}")

                submit_button = self.driver.find_element(By.ID, "id_submitbutton")
                submit_button.click()

                progress = self.get_progress()
                if progress is not None:
                    if int(progress) == 100:
                        input("Нажмите Enter для выхода...")
                        return False
                print(f'Текущий url: {self.driver.current_url}')
                return True
            else:
                print("Правильный ответ не найден среди предложенных.")
                input("Нажмите Enter для выхода...")
                return False

        except Exception as e:
            print(f"Ошибка: {e}")
            input("Нажмите Enter для выхода...")
            return False

    def handle_continue_button(self):
        """Проверяет наличие кнопки 'Хотите продолжить' и нажимает её, если есть."""
        try:
            continue_message = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Вы уже работали с этой лекцией')]")
            if continue_message:
                print("Обнаружено сообщение о продолжении лекции.")

                yes_button = self.driver.find_element(By.XPATH, "//a[contains(@class, 'btn-primary')]")
                yes_button.click()
                print("Кнопка 'Да' нажата.")

            continue_text_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Хотите продолжить')]"))
            )
            print("Текст найден:", continue_text_element.text)

            yes_button = self.driver.find_element(By.XPATH, "//a[contains(@class, 'btn-primary')]")
            yes_button.click()
            print("Кнопка 'Да' нажата.")
        except Exception:
            print("Элемент 'Хотите продолжить' не найден.")


    def find_elements_tests(self):
        """Извлекает текст вопроса и варианты ответа."""
        try:
            question_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//form[contains(@id, 'mform')]//div[@class='no-overflow']"))
            )
            question_text = question_element.text.strip()
            print("Вопрос:", question_text)

            answer_elements = self.driver.find_elements(By.CLASS_NAME, "form-check-label")
            answers = [answer.text.strip() for answer in answer_elements if answer.text.strip()]
            return question_text, answers

        except Exception:
            print("Не удалось найти вопрос или варианты ответа.")
            return None, None

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


    def get_progress(self) -> Union[str, None]:
        """Извлекает процент выполнения из прогресс-бара."""
        try:
            progress_element = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "progress-bar"))
            )
            progress = progress_element.get_attribute("aria-valuenow")
            print(f"Прогресс: {progress}%")
            return progress
        except Exception:
            print("Не удалось получить прогресс.")
            return None
        

    def find_answer(self, question_text: str, answers: list) -> str:
        """Определяет правильный ответ на вопрос."""
        text = question_text + '\n' + '\n'.join(answers)
        return self.chatgpt.get_answer(text)

    def close_driver(self):
        """Метод для закрытия драйвера."""
        self.driver.quit()


# Запуск парсера
parse = Parse(login="stu-ipo-21-16", password="rkH-34Q-B2a-aQw")
parse.start_test_loop("http://edu.verish.net/mod/lesson/view.php?id=35&pageid=45")
