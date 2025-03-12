
import os
import logging
from dotenv import load_dotenv
from utils.parse import Parse
from utils.parse_type_test import ParseTestNotLesson
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")



url = str(input("Введите url: \n>>> "))

test_type = str(input("Введите тип теста 1-лекция, 2-тест: \n>>> "))

if test_type == "1":
    parse = Parse(login, password)
    parse.start_test_loop(url)
elif test_type == "2":
    parse = ParseTestNotLesson(login, password)
    parse.start_test_loop(url)
else:
    print("Неверный тип теста")


parse.close_driver()
