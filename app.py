from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from os import environ


load_dotenv()
app = Flask(__name__)
key = Fernet.generate_key()  # Encrypt password

host = environ.get('DB_HOST')
port = environ.get('DB_POST')
dbname = environ.get('DB_NAME')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')


def get_connection():
    conection = connect(host=host,
                        port=port,
                        dbname=dbname,
                        user=user,
                        password=password)

    return conection


@app.get('/api/users')
def get_users():
    connection = get_connection()
    cursor = connection.cursor(
        cursor_factory=extras.RealDictCursor)  # Make it objects
    cursor.execute('SELECT * from users')
    users = cursor.fetchall()

    cursor.close()
    connection.close()
    return jsonify(users)


@app.get('/api/users/<id>')
def get_user_by_id(id: int):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)

    cursor.execute('SELECT * FROM USERS WHERE id = %s', (id,))
    user = cursor.fetchone()

    if user is None:
        return jsonify({'message': 'user not found'}), 404

    cursor.close()
    connection.close()

    return jsonify(user)


@app.post('/api/users')
def create_user():
    # User creation
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = Fernet(key).encrypt(
        bytes(new_user['password'], 'utf-8'))  # Encrypt password

    # Connection to db
    conection = get_connection()
    cursor = conection.cursor(cursor_factory=extras.RealDictCursor)

    cursor.execute('INSERT INTO users(username, email, password) VALUES (%s, %s, %s) RETURNING *',
                   (username, email, password))
    new_created_user = cursor.fetchone()
    print(new_created_user)

    conection.commit()
    cursor.close()
    conection.close()

    return jsonify(new_created_user)


@app.delete('/api/users/<id>')
def delete_users(id: int):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)

    cursor.execute('DELETE FROM users WHERE id = %s RETURNING *', (id, ))
    user = cursor.fetchone()

    if user is None:
        return jsonify({"message": 'user not found'}), 404

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(user)


@app.put('/api/users/<id>')
def update_users(id: int):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=extras.RealDictCursor)

    new_user_data = request.get_json()
    username = new_user_data['username']
    email = new_user_data['email']
    password = Fernet(key).encrypt(bytes(new_user_data['password'], 'utf-8'))

    cursor.execute(
        'UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s RETURNING *',
        (username, email, password, id))
    updated_user = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    if updated_user is None:
        return jsonify({'message', 'user not found'}), 404

    return jsonify(updated_user)


@app.get("/")
def home():
    return send_file('static/index.html')


if __name__ == "__main__":
    app.run(debug=True)
