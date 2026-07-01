import logging
from fastapi import FastAPI, Response, Cookie
from environs import Env
from models import User, Feedback, UserCreate



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

@app.post("/create_user")
def read_root(user_create: UserCreate):
    return user_create

sample_product_1 = {
    "product_id": 123,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 599.99
}

sample_product_2 = {
        "product_id": 456,
        "name": "Phone Case",
        "category": "Accessories",
        "price": 19.99
    }

sample_product_3 = {
    "product_id": 789,
    "name": "Iphone",
    "category": "Electronics",
    "price": 1299.99
}

sample_product_4 = {
    "product_id": 101,
    "name": "Headphones",
    "category": "Accessories",
    "price": 99.99
}

sample_product_5 = {
    "product_id": 202,
    "name": "Smartwatch",
    "category": "Electronics",
    "price": 299.99
}

sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

@app.get("/product/{product_id}")
def read_root(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product

    return {"error": "Product not found"} 

@app.get("/products/search")
def read_root(keyword: str, category: str | None = None, limit: int | None = 10):
    result = []
    for product in sample_products:
        if product["category"] == category and keyword.lower() in product["name"].lower():
            result.append(product)

    return result[:limit]

import uuid
id = ''
user_data = {
    "username": "user123",
    "password": "password123"
}

@app.post("/login")
def read_root(user: User, response: Response):
    print(user)
    if user.username == "user123" and user.password == "password123":
        global id
        id= uuid.uuid4()
        response.set_cookie(key="session_token", value=id, max_age=3600, httponly=True)

        return {"message": "Login successful"}

@app.get("/user")
def read_root(session_token = Cookie()):
    if session_token and session_token == str(id):
        return user_data
    
    return {"error": "invalid_token_value"}