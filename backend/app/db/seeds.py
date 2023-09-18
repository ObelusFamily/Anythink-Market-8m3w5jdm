from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
import random
import string
import os
from faker import Faker


# Database connection
database_url: str = os.environ['DATABASE_URL']
engine: Engine = create_engine(database_url, echo=False)

user_insert_statement = text("""
    INSERT INTO users(username, email, salt, bio, hashed_password) 
    VALUES(:username, :email, :salt, :bio, :hashed_password) 
    ON CONFLICT DO NOTHING
""")
select_last_user_id = text("""
    SELECT * FROM users ORDER BY id DESC LIMIT 1
""")
item_statement = text("""
    INSERT INTO items(slug, title, description, seller_id) 
    VALUES(:slug, :title, :description, :seller_id) 
    ON CONFLICT DO NOTHING
""")
select_last_item_id = text("""
    SELECT * FROM items ORDER BY id DESC LIMIT 1
""")
comment_statement = text("""
    INSERT INTO comments(body, seller_id, item_id)
    VALUES(:body, :seller_id, :item_id) 
    ON CONFLICT DO NOTHING
""")

fake = Faker()

with engine.connect() as con:
  for i in range(100):
    
    user: dict[str, str] = {'username': fake.name(), 'email':fake.email(), 'salt': 'abc', 'bio': fake.text(), 'hashed_password':'12345689'}
    con.execute(user_insert_statement, **user)
    
    result = con.execute(select_last_user_id)
    for row in result:
      generated_user_id = row['id']
    
    item: dict[str, str] = {'slug':f'slug-{i}', 'title':f'title{i}','description':f'{fake.text()}', 'seller_id':generated_user_id}
    con.execute(item_statement, **item)
    
    item_result = con.execute(select_last_item_id)
    for row in item_result:
      generated_item_id = row['id']
    comment: dict[str, str] = {'body': f'{fake.text()}', 'seller_id': generated_user_id, 'item_id': generated_item_id}
    con.execute(comment_statement, **comment)