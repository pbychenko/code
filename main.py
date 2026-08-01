import logging
from fastapi import FastAPI, Response, Cookie, HTTPException, status, Depends, status, HTTPException
# from environs import Env
from models import User, Feedback, UserCreate, Item
from fastapi.security import HTTPBasic, HTTPBasicCredentials




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = FastAPI()
security = HTTPBasic()
# env = Env()
# env.read_env()

# user_data = {
#     "age": 1,
#     "name": "John Doe"
# }

# my_user: User = User(**user_data)


# @app.post("/user")
# def read_root(user: User):
#     # logger.info('tete', env("Test"))
#     # return {"message": "Hello, World!"}
#     age = user.age
#     # if age > 18:
#     return { "is_adult": user.age > 18, **user.model_dump() }
#     # return user

# @app.post("/feedback")
# def read_root(feedback: Feedback, is_premium: bool = False):
#     stop_words = ["редиска", "бяка", "козявка"]
#     if any(word in feedback.message.lower() for word in stop_words):
#         return { "message": "Ваш отзыв содержит недопустимые слова. Пожалуйста, исправьте его." }
#     responce_message = f"Спасибо, {feedback.name}! Ваш отзыв сохранён."
#     if is_premium:
#         responce_message += " Ваш отзыв будет рассмотрен в приоритетном порядке.."
#     return { "message": responce_message }

# @app.post("/create_user")
# def read_root(user_create: UserCreate):
#     return user_create

# sample_product_1 = {
#     "product_id": 123,
#     "name": "Smartphone",
#     "category": "Electronics",
#     "price": 599.99
# }

# sample_product_2 = {
#         "product_id": 456,
#         "name": "Phone Case",
#         "category": "Accessories",
#         "price": 19.99
#     }

# sample_product_3 = {
#     "product_id": 789,
#     "name": "Iphone",
#     "category": "Electronics",
#     "price": 1299.99
# }

# sample_product_4 = {
#     "product_id": 101,
#     "name": "Headphones",
#     "category": "Accessories",
#     "price": 99.99
# }

# sample_product_5 = {
#     "product_id": 202,
#     "name": "Smartwatch",
#     "category": "Electronics",
#     "price": 299.99
# }

# sample_products = [sample_product_1, sample_product_2, sample_product_3, sample_product_4, sample_product_5]

# @app.get("/product/{product_id}")
# def read_root(product_id: int):
#     for product in sample_products:
#         if product["product_id"] == product_id:
#             return product

#     return {"error": "Product not found"} 

# @app.get("/products/search")
# def read_root(keyword: str, category: str | None = None, limit: int | None = 10):
#     result = []
#     for product in sample_products:
#         if product["category"] == category and keyword.lower() in product["name"].lower():
#             result.append(product)

#     return result[:limit]

import uuid
id = ''
user_data = {
    "username": "user123",
    "password": "password123"
}

# @app.post("/login")
# def read_root(user: User, response: Response):
#     # print(user)
#     if user.username == user_data["username"] and user.password == user_data["password"]:
#         global id
#         id= uuid.uuid4()

#         response.set_cookie(key="session_token", value=id, max_age=3600, httponly=True)

#         return {"message": "Login successful"}

# @app.get("/user")
# def read_root(session_token: str | None = Cookie(default=None)):
#     print('session_token', session_token)
#     if session_token and session_token == str(id):
#         return user_data
    
#     raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Unauthorized"
#         )

from typing import Annotated

from fastapi import Header, Request
@app.get("/headers")
def read_root(user_agent: str | None = Header(None), accept_language: str | None = Header(None)):
    # print(user_agent, accept_language)
    if not user_agent:
        raise HTTPException(status_code=400, detail="user_agent header is required")

    if not accept_language:
        raise HTTPException(status_code=400, detail="accept_language header is required")

    return {"user_agent": user_agent, "accept_language": accept_language}
    
# @app.get("/headers")
# def read_root(request: Request):
#     if "user-agent" not in request.headers:
#         raise HTTPException(status_code=400, detail="user_agent header is required")

#     if "accept-language" not in request.headers:
#         raise HTTPException(status_code=400, detail="accept_language header is required")

#     return {"user_agent": request.headers.get("user-agent"), "accept_language": request.headers.get("accept-language")}

USER_DATA = [
    User(**{"username": "user1", "password": "pass1"}),
    User(**{"username": "user2", "password": "pass2"})
]

# def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     for user in USER_DATA:
#         if user.username == credentials.username and user.password == credentials.password:
#             return user.username
    
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# @app.get('/login')
# def login(username: str = Depends(authenticate_user)):
#     return {"message": f"You got my secret, welcome, {username}!"}
import jwt
from datetime import datetime, timezone, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict

# OAuth2PasswordBearer извлекает токен из заголовка "Authorization: Bearer <token>"
# Параметр tokenUrl указывает маршрут, по которому клиенты смогут получить токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "mysecretkey"  # В реальной практике генерируйте ключ, например, с помощью 'openssl rand -hex 32', и храните его в безопасности
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Время жизни токена

# Функция для создания JWT токена с заданным временем жизни
def create_jwt_token(data: Dict):
    """
    Функция для создания JWT токена. Мы копируем входные данные, добавляем время истечения и кодируем токен.
    """
    to_encode = data.copy()  # Копируем данные, чтобы не изменить исходный словарь
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Задаем время истечения токена
    to_encode.update({"exp": expire})  # Добавляем время истечения в данные токена
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Кодируем токен с использованием секретного ключа и алгоритма

def get_user(username: str):
    """
    Функция для поиска пользователя по имени пользователя. 
    В реальном проекте это должно быть запросом к базе данных.
    """
    for user in USER_DATA:
        if user.username == username:
            return user
    return None

def get_user_from_token(token: str = Depends(oauth2_scheme)):
    """
    Функция для извлечения информации о пользователе из токена. Проверяем токен и извлекаем утверждение о пользователе.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Декодируем токен с помощью секретного ключа
        print('payload', payload)
        return payload.get("sub")  # Возвращаем утверждение о пользователе (subject) из полезной нагрузки
    except jwt.ExpiredSignatureError:
        pass  # Обработка ошибки истечения срока действия токена
    except jwt.InvalidTokenError:
        pass  # Обработка ошибки недействительного токена

@app.post("/login")
async def login(user_in: User):
    for user in USER_DATA:
        if user.username == user_in.username and user.password == user_in.password:
            token = create_jwt_token({"sub": user_in.username})

            return {"access_token": token, "token_type": "bearer"}
    # Если данные неверные, возвращаем ошибку
    return {"error": "Invalid credentials"}

@app.get("/protected_resource")
async def protected_resource(current_user: str = Depends(get_user_from_token)):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    user = get_user(current_user)
    if user:
        return 'access granted'
    # Если пользователь не найден, возвращаем ошибку
    return 'access denied'

from database import get_db_connection
import asyncpg

@app.post("/items")
async def create_item(item: Item, db: asyncpg.Connection = Depends(get_db_connection)):
    await db.execute('''
        INSERT INTO items(name) VALUES($1)
    ''', item.name)
    return {"message": "Item added successfully!"}

@app.post("/register")
async def create_item(user: User, db: asyncpg.Connection = Depends(get_db_connection)):
    # try:
    await db.execute('''
        INSERT INTO users(username, password) VALUES($1, $2)
    ''', user.username, user.password)

    # await db.commit()
    # catch Exception as e:
        # print('error', e)
    


    return {"message": "User registered successfully!"}