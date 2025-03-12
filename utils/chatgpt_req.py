from openai import OpenAI
from dotenv import load_dotenv
import httpx
import os


class ChatGPT:
    """
    Класс для работы с ChatGPT API.
    """

    def __init__(self):
        load_dotenv()
        
        proxy_url = "http://QCbDT52oW8QR:RNW78Fm5@pool.proxy.market:10344"

        self.http_client = httpx.Client(proxy=proxy_url)
        self.client = OpenAI(
            api_key=os.getenv("API_KEY_CHATGPT"),
            http_client=self.http_client
        )

    def get_answer(self, question: str) -> str:
        """
        Получает ответ на тестовый вопрос.
        :param question: str - вопрос
        :return: str - ответ
        """
        completion = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "Ты в роле профи в области программирования и DevOps. Ты должен выбирать правильный вариант ответа из предложенных вариантов. Отвечай только одним вариантом, без пояснений."},
            {"role": "user", "content": question}
        ]
        )
        return completion.choices[0].message.content

