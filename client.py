from flask import Flask
from waitress import serve
from services.chat import gpt

# GPT Crawler
from modules.chatgpt.controller import GPTWebController

### Register services
app = Flask(__name__)
app.register_blueprint(blueprint=gpt)        # 앞서 api.py에서 선언한 Blueprint 개체를 서비스로 등록

# Root
@app.route("/", methods=["GET"])
def index():
    return "<h1>hello world</h1>"

### Error Handler
import json
from werkzeug.exceptions import HTTPException
@app.errorhandler(HTTPException)
def handle_exception(e:HTTPException):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "result": {},
        "status":{
            "code": e.code,
            "msg": e.name
        }
    })
    # e.description
    response.content_type = "application/json"
    return response

### Main
if __name__ == "__main__":
    GPTWebController()
    serve(app, host="0.0.0.0", port=9099)