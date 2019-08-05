from flask import Flask, jsonify, request, abort
from pprint import pprint
import psycopg2
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from threading import Thread, currentThread
from app.utils_slack_sheets import call_db_student_details_worker

app = Flask(__name__, instance_relative_config=True)

# tests out whether the slack command is coming through or not


@app.route('/', methods=['GET', 'POST'])
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


# checks if the text Entered is separated by " : " or " , " or is just single
# if its none of the abforementioned, it generates an error.
# Same goes if it receives too many arguments


@app.route('/student_details', methods=['POST'])  # , 'GET'
def student_details():
    """Get the month in question"""
    message = None
    try:
        if request.get_data():
            pprint("Request to retrieve Month in question received successfully")
            response_data = request.get_data()

            if response_data:
                pprint("Retrieved Payload shown below: ")
                pprint(response_data)
                response_url = request.form.get('response_url')
                pprint(response_url)
            try:
                requested_id = request.form.get('text')
                if requested_id:
                    pprint(requested_id)

                    message = {
                        "response_type": "in_channel",
                        "text": "Processing request: Acquiring Data for Specified Student. Please Wait...",
                        "attachments": [
                            {
                                "text": requested_id,
                                'color': '#450000'
                            }
                        ]
                    }

                    # call thread
                    t_student_details = Thread(name='call_db_student_details_worker', target=call_db_student_details_worker, args=[
                                               response_url, requested_id])
                    t_student_details.start()

            except KeyError as e:
                print("The error is: ", e), pprint(type(e))
                print('errors')
                message = "Key Error"

    except Exception as e:
        print("The error is: ", e), pprint(type(e))
        pprint("general Error")
        message = "General Error"

    finally:
        return jsonify(message), 200
