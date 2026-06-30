import logging
from fastapi import FastAPI
from environs import Env
from models import User, Feedback



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
env = Env()
env.read_env()

# user_data = {
#     "age": 1,
#     "name": "John Doe"
# }

# my_user: User = User(**user_data)


@app.post("/user")
def read_root(user: User):
    # logger.info('tete', env("Test"))
    # return {"message": "Hello, World!"}
    age = user.age
    # if age > 18:
    return { "is_adult": user.age > 18, **user.model_dump() }
    # return user

@app.post("/feedback")
def read_root(feedback: Feedback, is_premium: bool = False):
    stop_words = ["редиска", "бяка", "козявка"]
    if any(word in feedback.message.lower() for word in stop_words):
        return { "message": "Ваш отзыв содержит недопустимые слова. Пожалуйста, исправьте его." }
    responce_message = f"Спасибо, {feedback.name}! Ваш отзыв сохранён."
    if is_premium:
        responce_message += " Ваш отзыв будет рассмотрен в приоритетном порядке.."
    return { "message": responce_message }
