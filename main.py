
import os
from dotenv import load_dotenv
from utils.parse import Parse
load_dotenv()



login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")



parse = Parse(login, password)

url = str(input("Введите url: \n>>> "))

parse.start_test_loop(url)

parse.close_driver()

