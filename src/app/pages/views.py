
from flask import Flask, jsonify, request, abort
from pprint import pprint



from . import pages_blueprint

# tests out whether the slack command is coming through or not
@pages_blueprint.route('/', methods=['GET', 'POST'])
def home():
	""" Tests connection to my Flask app"""	
	message = None
	try:
		if request.method == "POST":
			print("POST REQUEST-Home")
			if request.get_data():
				pprint("Retrieved request data to home function. Payload below")
				the_request_data = request.get_data()
				pprint(the_request_data)
				text = request.form["text"]
				if text == "txn":
					pprint("Comms between home function & slack working perfectly.")
					message = "Slack Database Txn App working."
				else:
					message = "Ensure you enter 'txn' as the input."
					
		message= "GET REQUEST - Home"
		
	except Exception as e:
		message = f"general error: {e}"
		
	finally:
		return jsonify(message)