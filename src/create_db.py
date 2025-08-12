# backend/src/create_db.py
import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Connect to default DB
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS chat_app")
    cursor.execute("CREATE DATABASE chat_app")
    print("Database created!")
    conn.close()

    # Connect to new database
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()

    # ✅ Create ai_models table
    cursor.execute("""
        CREATE TABLE if not exists ai_models (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            display_name VARCHAR(50),
            avatar VARCHAR(100),
            description TEXT,
            member_since DATE DEFAULT NOW(),
            debates_finished INT DEFAULT 0,
            creativity INT DEFAULT 50,
            logic INT DEFAULT 70,
            speed INT DEFAULT 60,
            ethics INT DEFAULT 80
        )
    """)

    # ✅ Create messages table
    cursor.execute("""
        CREATE TABLE if not exists messages (
            id VARCHAR(36) PRIMARY KEY,
            text TEXT NOT NULL,
            sender VARCHAR(50) NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            model VARCHAR(50),
            target_model VARCHAR(50)
        )
    """)

    # Insert model data
    models_data = [
    ('GPT-4', 'GPT-4', 'gpt4.png', 'OpenAI flagship model', '2023-03-01', 42, 85, 90, 70, 80),
    ('Claude', 'Claude', 'claude.png', 'Anthropic’s ethical AI', '2023-05-15', 38, 90, 85, 65, 95),
    ('Llama', 'Llama', 'llama3.png', 'Meta’s open-source powerhouse', '2023-07-20', 55, 75, 70, 85, 60),
    ('Mistral', 'Mistral-7B', 'mistral.png', 'Mistral 7B Instruct model', '2024-02-10', 30, 80, 85, 90, 70),
    ('X', 'X', 'x.png', 'The thinker model', '2024-01-01', 29, 70, 80, 60, 75),
    ('PaLM 2', 'PaLM 2', 'palm.png', 'Google’s language model', '2023-04-05', 35, 70, 75, 70, 60),
    ('RoBERTa', 'RoBERTa', 'roberta.png', 'Robustly optimized BERT', '2023-06-12', 25, 60, 85, 50, 70),
    ('Cohere', 'Cohere', 'cohere.png', 'Cohere language model', '2023-05-20', 28, 70, 80, 65, 85),
    ('Qwen', 'Qwen', 'qwen.png', 'Strong logical skills', '2024-07-01', 8, 85, 75, 90, 70)
    ]

    cursor.executemany("""
        INSERT INTO ai_models 
        (name, display_name, avatar, description, member_since, debates_finished, creativity, logic, speed, ethics)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, models_data)

    conn.commit() # Commit the changes
    print("✅ Tables created and seed data inserted!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()