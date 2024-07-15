from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from fake_useragent import UserAgent
from db import Question

import requests
from bs4 import BeautifulSoup


Base = declarative_base()
user_agent = UserAgent()
headers = {
    "Accept": "*/*",
    "User-Agent": user_agent.random  # Call the method to get a random user agent
}

engine = create_engine('sqlite:///example.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def questions1():
    url1 = "https://lifehacker.ru/kak-razgovorit-cheloveka/"
    req = requests.get(url1, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    questions = soup.find_all("li")
    for i in questions:
        print(f"Добавлен вопрос {i.text}")
        question = Question(question_text=i.text)  # Use a singular variable name to avoid confusion
        session.add(question)
        session.commit()

questions1()

# The rest of your commented code here remains the same
