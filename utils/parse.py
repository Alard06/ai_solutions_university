import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Union
from .general import GeneralParse

class TestInsideTheLesson(GeneralParse):
    """Класс для прохождения теста внутри лекции."""
    def __init__(self, login: str, password: str):
        super().__init__(login, password)


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



class TestOutsideTheLesson(GeneralParse):
    """Класс для прохождения теста вне лекции."""
    def __init__(self, login: str, password: str):
        super().__init__(login, password)


    def test_solution(self):
        """Обрабатывает один вопрос теста"""
        self.find_element_start_test()

        question_text, answers = self.find_elements_tests()
        
        if not question_text or not answers:
            print("Тест завершен или вопрос не найден.")
            result = input("Введите ! для выхода...")
            return result != "!"
            
        correct_answer = self.find_answer(question_text, answers)

        if correct_answer in answers:
            index = answers.index(correct_answer)
            answer_elements = self.driver.find_elements(By.CSS_SELECTOR, ".answer input[type='radio']")
            
            if index < len(answer_elements):
                answer_elements[index].click()
                print(f"Выбран ответ: {correct_answer}")

                try:
                    next_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.ID, "mod_quiz-next-nav"))
                    )
                    next_button.click()
                    return True
                except Exception:
                    print("Не удалось найти кнопку 'Следующая страница'")
                    return False
        else:
            print("Правильный ответ не найден среди предложенных.")
            return False

    def find_elements_tests(self):
        """Извлекает текст вопроса и варианты ответов."""
        try:
            question_text = self.driver.find_element(By.CLASS_NAME, "qtext").text
            answer_elements = self.driver.find_elements(By.CSS_SELECTOR, ".answer .flex-fill")
            answers = [answer.text.strip() for answer in answer_elements]
            return question_text, answers
        except Exception:
            print("Не удалось найти вопрос или варианты ответа.")
            return None, None

    def find_element_start_test(self):
        """Ищет и нажимает кнопку начала теста, если она есть."""
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Попытка теста')]"))
            )
            button.click()

        except Exception:
            try:
                button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Продолжить текущую попытку')]"))
                )
                button.click()
            except Exception:
                print("Не удалось найти кнопку 'Попытка теста'")
