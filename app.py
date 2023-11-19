# app.py

from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Replace these with your PostgreSQL connection details
db_params = {
    'dbname': 'datagram',
    'user': 'postgres',
    'password': '9854',
    'host': 'localhost',
    'port': '5432',
}

def create_table():
    conn = psycopg2.connect(**db_params)
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL
            )
        """)
    conn.commit()
    conn.close()

def fetch_posts():
    conn = psycopg2.connect(**db_params)
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title, content FROM posts")
        posts = cursor.fetchall()
    conn.close()
    return posts

def add_post(title, content):
    conn = psycopg2.connect(**db_params)
    with conn.cursor() as cursor:
        cursor.execute(
            sql.SQL("INSERT INTO posts (title, content) VALUES ({}, {}) RETURNING id")
            .format(sql.Literal(title), sql.Literal(content))
        )
        post_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return post_id

@app.route('/')
def index():
    posts = fetch_posts()
    return render_template('index.html', posts=posts)

@app.route('/add_post', methods=['GET', 'POST'])
def add_post_route():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        add_post(title, content)
        return redirect(url_for('index'))
    return render_template('add_post.html')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
