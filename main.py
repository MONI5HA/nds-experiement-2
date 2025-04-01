from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS, cross_origin
import honeywords
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
cors = CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this "super secret" to something else!
jwt = JWTManager(app)

DB_HOST = "localhost"
DB_NAME = "nds"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_PORT = 5432

def getDbConnection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    return conn

@app.route('/', methods = ['GET']) 
def home(): 
    return 'Welcome to the server! 👍'

@app.route('/api/register', methods = ['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        if not email or not password:
            return jsonify({"message": "Invalid Email or Password"})
        conn = getDbConnection()
        cur = conn.cursor()
        # create the basic user
        cur.execute("INSERT INTO users (email, username) VALUES (%s, %s) RETURNING id;", [email, username])
        insertedId = cur.fetchone()[0]
        print("inserted id: "+str(insertedId))
        # generate honey words
        passwordList, realIndex = honeywords.generate_honey_words('myspace', 1, password)
        # store decoy passwords to db
        for pwIndex in range(len(passwordList)):
            cur.execute("INSERT INTO honeywords (user_id, password_index, password_hash) VALUES (%s, %s, %s)", (insertedId, pwIndex, passwordList[pwIndex]))
        # update user to db
        cur.execute("UPDATE users set real_index=%s WHERE id=%s;", (realIndex, insertedId))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except psycopg2.IntegrityError as i:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"message": "password or email already exists!"}), 400
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@app.route('/api/login', methods = ['POST'])
def login():
    try:
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        print(f'Client IP: {client_ip}')
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({"message": "Invalid Email or Password"})
        conn = getDbConnection()
        cur = conn.cursor()
        # check if user exists
        cur.execute("SELECT * FROM users WHERE email=%s;", [email])
        user = cur.fetchall()[0]
        if not user:
            return jsonify({"message": "User not found"}) 
        # check if password is decoy
        cur.execute("SELECT password_index FROM honeywords WHERE password_hash=%s and user_id=%s;", [password, user[0]])
        passwordFetched = cur.fetchone()
        if not passwordFetched:
            # password incorrect
            cur.execute("INSERT INTO logs (email, origin_ip, decoy_detected) VALUES (%s, %s, %s)", (email, client_ip, 'false'))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"message": "Incorrect Password"})
        if passwordFetched[0] == user[3]:
            # password matched
            cur.execute("INSERT INTO logs (email, origin_ip, decoy_detected) VALUES (%s, %s, %s);", (email, client_ip, 'false'))
            conn.commit()
            cur.close()
            conn.close()
            # creating jwt token
            token = create_access_token(identity=user[0])
            return jsonify({"token": token })
        else:
            # decoy match
            cur.execute("INSERT INTO logs (email, origin_ip, decoy_detected) VALUES (%s, %s, %s)", (email, client_ip, 'true'))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"message": "DECOY"})
    except psycopg2.IntegrityError as i:
        print(i)
        # conn.rollback()
        # cur.close()
        # conn.close()
        return jsonify({"message": "password or email invalid!"}), 400
    except Exception as e:
        print(e)
        # conn.rollback()
        # cur.close()
        # conn.close()
        return jsonify({"message": "An error occurred: " + str(e)}), 500

@app.route('/api/logs', methods = ['GET'])
def fetchLogs():
    try:
        conn = getDbConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM logs;")
        return jsonify({"data": cur.fetchall()})
    except psycopg2.IntegrityError as i:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"message": "password or email already exists!"}), 400
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"message": "An error occurred: " + str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True)