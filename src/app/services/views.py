
from flask import Flask, jsonify, request, abort
from threading import Thread, currentThread
from pprint import pprint
from app.utils.utils_slack_sheets import call_db_student_details_worker

from . import service_blueprint



# checks if the text Entered is separated by " : " or " , " or is just single
# if its none of the abforementioned, it generates an error.
# Same goes if it receives too many arguments


# tests out whether the slack command is coming through or not
@service_blueprint.route('/student_details/', methods=['POST'])
def student_details():
    """Gets the month in question"""
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
        message = "General Error"

    finally:
        return jsonify(message), 200
		
		