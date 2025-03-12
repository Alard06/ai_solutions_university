from utils.general import GeneralParse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ParseTestNotLesson(GeneralParse):
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

    def close_driver(self):
        """Закрывает веб-драйвер."""
        self.driver.quit()
