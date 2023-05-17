from flask import Blueprint, request, jsonify
from modules.chatgpt.controller import GPTWebController

gpt = Blueprint(name="gpt", import_name=__name__)


# curl -X GET -H "Content-Type:application/json" -d '{"model":"GPT-4"}' http://localhost:9099/gpt/setup
@gpt.route('/gpt/setup', methods=['GET'])
def setup():
    if request.content_type != "application/json":
        return jsonify({"status":500})

    # get args.
    modelName = None
    if request.data:
        args:dict = request.json
        modelName = args.get("model")

    gwc = GPTWebController()

    gwc.login()
    gwc.skip_tutorial()
    if modelName:
        gwc.set_model(modelName=modelName)

    return jsonify({"status":200})


# curl -X GET -H "Content-Type:application/json" http://localhost:9099/gpt/login
@gpt.route('/gpt/login', methods=['GET'])
def login():
    if request.content_type != "application/json":
        return jsonify({"status":500})

    gwc = GPTWebController()
    if gwc.login():
        gwc.skip_tutorial()
        return jsonify({"status":200})

    return jsonify({"status":400})


# curl -X POST -H "Content-Type:application/json" -d '{"message":"some message"}' http://localhost:9099/gpt/message
@gpt.route('/gpt/message', methods=['POST'])
def send_message():
    if request.content_type != "application/json":
        return jsonify({"status":500})
    
    if not request.data:
        return jsonify({"status":400, "message":"need a question"})
    message = request.json["message"]
    
    gwc = GPTWebController()
    response = gwc.send_message(message=message)
    print(response)

    return jsonify({"code":200, "result":response})


@gpt.route('/gpt/new-chat', methods=['GET'])
def new_chat():
    if request.content_type != "application/json":
        return jsonify({"status":500})
    
    # get args.
    modelName = None
    if request.data:
        args:dict = request.json
        modelName = args.get("model")

    gwc = GPTWebController()
    gwc.new_chat()
    if modelName:
        gwc.set_model(modelName=modelName)

    return jsonify({"status":200})

    
