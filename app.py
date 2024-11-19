import jwt
import datetime
import logging
from flask import Flask, jsonify, Response, request
from constants import (
    ISSUER,
    SECRET_KEY,
    HTTP_POST, HTTP_DELETE,
    MESSAGE_TOKEN_BLACKLISTED, 
    MESSAGE_TOKEN_UNBLACKLISTED,
    ERROR_TOKEN_EXPIRED,
    ERROR_NO_TOKEN_PROVIDED,
    ERROR_CANNOT_ADD_INVALID_ISSUER,
    ERROR_CANNOT_DELETE_INVALID_ISSUER,
    MESSAGE_TOKEN_NO_LONGER_BLACKLISTED
)

app = Flask(__name__)

black_list = [] # List of black listed tokens

handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

app.logger.addHandler(handler)


@app.before_request
def before_request():
    if request.endpoint != "login":
        header = request.headers.get("Authorization")
        token = header.split()[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            app.logger.error("No token provided")
            return jsonify({"success": False, "error": ERROR_TOKEN_EXPIRED}), 400

@app.route("/info")
def info() -> Response:
    if request.headers.get("Authorization") is None:
        app.logger.error("No token provided")
        return jsonify({"success": False, "error": ERROR_NO_TOKEN_PROVIDED}), 400

    header = request.headers.get("Authorization")
    token = header.split()[1]
    decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256")

    if token not in black_list:
        app.logger.info("Token no longer blacklisted")
        return jsonify({ "token": token, "message": MESSAGE_TOKEN_NO_LONGER_BLACKLISTED}), 200

    app.logger.info("Token is blacklisted")
    return jsonify({ "success": True, "token": token, "message": decoded}), 200

@app.route("/blacklist", methods=["POST", "DELETE"])
def blacklist() -> Response:
    if request.method == HTTP_POST:
        app.logger.info("POST token to blacklist")
        if request.headers.get("Authorization") is None:
            return jsonify({"success": False, "error": ERROR_NO_TOKEN_PROVIDED}), 400
        header = request.headers.get("Authorization")
        token = header.split()[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        
        if decoded["iss"] != ISSUER:
            app.logger.error("Token is not valid. Incorrect issuer")
            return jsonify({"success": False, "error": ERROR_CANNOT_ADD_INVALID_ISSUER}), 400

        if token not in black_list:
            black_list.append(token)
        
        app.logger.info("Token added to blacklist")
        
        return jsonify({"success": True, "token": token, "message": MESSAGE_TOKEN_BLACKLISTED})

    elif request.method == HTTP_DELETE:
        app.logger.info("DELETE token from blacklist")
        
        if request.headers.get("Authorization") is None:
            return jsonify({"success": False, "error": ERROR_NO_TOKEN_PROVIDED}), 400
        
        header = request.headers.get("Authorization")
        token = header.split()[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256")

        if decoded["iss"] != ISSUER:
            app.logger.error("Cannot delete token. Incorrect issuer")
            return jsonify({"success": False, "error": ERROR_CANNOT_DELETE_INVALID_ISSUER}), 400
        
        if token in black_list:
            black_list.remove(token)

        app.logger.info("Token removed from blacklist")

        return jsonify({"success": True, "token": token, "message": MESSAGE_TOKEN_UNBLACKLISTED})
    

@app.route("/login", methods=["POST"])
def login() -> Response:
    """
    Added login route to simulate a user sign-in and receving a token
    """
    app.logger.info("User login")
    access_payload = { 
        "iss": ISSUER,
        #simulate an access token expiration in 30 minutes / Refresh token expiration would be much longer
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    }
    encoded = jwt.encode(access_payload, SECRET_KEY, algorithm="HS256")
    app.logger.info("User logged in successfully")
    return jsonify({ "token": encoded })
