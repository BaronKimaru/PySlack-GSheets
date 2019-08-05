
from flask import Flask, jsonify, request, abort
from pprint import pprint



from . import pages_blueprint

# tests out whether the slack command is coming through or not
@pages_blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Tests connection to my Flask app"""
    message = None
    try:
        if request.get_data():
            pprint("Retrieved request data to home function. Payload below")
            the_request_data = request.get_data()
            pprint(the_request_data)
            text = request.form["text"]
            if text == "txn":
                pprint("Comms between home function & slack working perfectly.")
                message = "Slack Database Txn App working."
                return jsonify(message)
            else:
                message = "No input retrieved. Ensure you enter 'txn' as the input."
                return jsonify(message)
				
    except Exception as e:
        pprint(e), pprint(type(e))
        message = "general error"
		
    finally:
        return jsonify(message), 200