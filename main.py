from flask import Flask, request, jsonify
import psycopg2

from config import config

app = Flask(__name__)

# Route to get a User
@app.route('/get-user/<user_id>')
def get_user(user_id):
    # connection = psycopg2.connect(host='localhost', port='5432', database='store', user='postgres', password='admin')
    user_data = {
            "user_id": user_id,
            "name": None,
            "email": None
        }

    try:
        connection = None
        params = config()
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()
        crsr.execute(f'SELECT * FROM users WHERE id={user_id};')
        user = crsr.fetchone()
        user_data['email'] = user[2]
        user_data['name'] = user[1]
        crsr.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

    return jsonify(user_data),200

# Route to send a new User
@app.route('/create-user/<username>/<email>')
def create_user(username,email):
    try:
        connection = None
        params = config()
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()
        crsr.execute("""
            INSERT INTO users (first_name, email)
            VALUES (%s, %s);
            """,
            (username,email))
        crsr.execute(f'SELECT * FROM users WHERE id > 1000;')
        crsr.fetchone()

        # Make the changes persist in the database
        connection.commit()

        # Close comunication with the database
        crsr.close()
        connection.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return '404'
    finally:
        if connection is not None:
            connection.close()

    return '200'

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)