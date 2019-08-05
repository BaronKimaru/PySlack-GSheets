from terminaltables import AsciiTable
from pprint import pprint
import psycopg2
from psycopg2 import extras
import json
import requests
from threading import currentThread
from app.sheetsapi import getCreds
from app.dbconnect import connect

service = getCreds()
conn = connect()

######### THIS IS AN INTEGRATION WITH SLACK, GOOGLE SHEETS USIGN THE FLASK FRAMEWORK ##########


def createsheets(slacksheettitle):
    sheet_id = None
    spreadsheet_url = None
    sheet_title = None
    sheet_name = None
    try:
        data = {'properties': {'title': slacksheettitle}}
        # if response = sheets.spreadsheets().create(body=data).execute()['properties']['title'] == slacksheettitle:
        #     pass
        # else:
        response = service.spreadsheets().create(body=data).execute()
        print("\n**********************Created Sheet Successfully**********************\n")
        sheet_id = response['spreadsheetId']
        spreadsheet_url = response['spreadsheetUrl']
        sheet_title = response['properties']['title']
        sheet_name = response['sheets'][0]['properties']['title']

    except Exception as e:
        pprint(e), pprint(type(e))
        pprint("General error")

    return sheet_id, spreadsheet_url, sheet_title, sheet_name


def getdbdata(last_txn_receiving):
    """This script will fetch data from the database and populate the already created sheet with the relevant data."""
    try:
        fields = ('ID', 'STDNAME', 'STDIDNUM', 'STDGENDER',
                  'STDPHONEONE', 'STDPHONETWO', 'STDEMAIL', 'STDBOXADDR')
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql_select = "SELECT id, student_name, studentid_pp_no, is_male, primary_phoneno,secondary_phoneno_one, email_address,box_address FROM dev_test.tbl_students limit 2 where id = %s"
        cur.execute(sql_select, [last_txn_receiving])
        rows = cur.fetchall()
        cur.close()
        rows.insert(0, fields)
        spreadsheet_data = {'values': str(rows)}

    except Exception as e:
        pprint(e), pprint(type(e))
        pprint("General Error")

    return spreadsheet_data


def updatesheets(sheet_id, range_rows, spreadsheet_data):
    """Fetches data from the google sheet created earlier on"""
    rows = None
    try:
        print("\n******************Writing Data to sheet...********************\n")
        # update the slackdata    ->    sheets.spreadsheets().values().update()
        rows = service.spreadsheets().values().update(spreadsheetId=sheet_id,
                                                      range=range_rows, body=spreadsheet_data, valueInputOption="RAW")
        rows.execute()
        print("\n*******************Data Written to sheet***********************\n")
        pprint(rows)

    except Exception as e:
        pprint(e), pprint(type(e))
        pprint("General error")

    return rows


def getsheets(sheets_id, sheet_name):
    """Fetches data from the google sheet created earlier on"""
    row = None
    try:
        # get data from updateddata()method  #get the slackdata    ->    sheets.spreadsheets().values().get()
        # data = {'values': [row[:6]] for row in rows if rows}
        rows = service.spreadsheets().values().get(spreadsheetId=sheets_id,
                                                   range=sheet_name).execute().get('values')
        for row in rows:
            pprint(row)

    except Exception as e:
        pprint(e), pprint(type(e))
        pprint("General error")

    return row


def indexOf(string, pattern):
    try:
        ret = string.index(pattern)
        print('found pattern')
        return ret
    except ValueError as e:
        print('no pattern')
        return -1

###########MAIN WORKER FUNCTION BEING CALLED BY THREAD##########


def call_db_student_details_worker(response_url, requested_id):
    ranges = None
    options = None
    try:
        print(currentThread().getName(), 'Starting db_student_details_worker')
        if (indexOf(requested_id, ':')) > -1:
            message = {'text': 'range'}
            ranges = requested_id.split(':')
            print(ranges)

            if (len(ranges) > 2):
                message = {'text': 'too many arguments'}

            else:
                # Create Spreadsheet
                sheets_id, spreadsheet_url, sheet_title, sheet_name = createsheets(
                    "STUDENT DETAILS")
                range_row = 'A1'

                # Connect to Database & execute command
                fields = ('ID', 'STUDENT NAME',
                          'STUDENT IDNUM')
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                sql_select = "SELECT id, student_name,studentid_pp_no FROM dev_test.tbl_students where id BETWEEN %s and %s"
                cur.execute(sql_select, (ranges))
                rows = cur.fetchall()
                cur.close()
                rows.insert(0, fields)
                pprint(rows)
                data = {'values': rows}

                # update the rows
                updatesheets(sheets_id, range_row, data)
                print("\n**************Updated Sheet Successfully*******************\n")

                # get the rows from the Sheet to appear in terminal
                print("*************Attempting to Access sheets Now...**************\n")
                getsheets(sheets_id, sheet_name)
                print("\n*****************Sheets Accessed***************************\n")

                message = {
                    'text': 'Slack Database Txn.\n Response Incoming.',
                    'attachments': [
                        {
                            "color": "#3AA3E3",
                            "title": "Spreadsheet URL...",
                            'text': spreadsheet_url
                        }
                    ]
                }
                headers = {'Content-Type': 'application/json'}
                response = requests.post(
                    response_url, data=json.dumps(message), headers=headers)
                print(currentThread().getName(),
                      'Ending db_student_details_worker')

        elif (indexOf(requested_id, ',')) > -1:
            message = {'text': 'options'}
            options = requested_id.split(',')
            options = tuple(options)
            print(options)

            # Create Spreadsheet
            sheets_id, spreadsheet_url, sheet_title, sheet_name = createsheets(
                "STUDENT DETAILS")
            range_row = 'A1'

            # Connect to Database & execute command
            fields = ('ID', 'STUDENT NAME',
                      'STUDENT IDNUM')
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql_select = """SELECT id, student_name,studentid_pp_no FROM dev_test.tbl_students where id IN %s"""
            cur.execute(sql_select, [options])
            rows = cur.fetchall()
            cur.close()
            rows.insert(0, fields)
            pprint(rows)
            data = {'values': rows}

            # update the rows
            updatesheets(sheets_id, range_row, data)
            print("\n**************Updated Sheet Successfully*******************\n")

            # get the rows from the Sheet to appear in terminal
            print("*************Attempting to Access sheets Now...**************\n")
            getsheets(sheets_id, sheet_name)
            print("\n*****************Sheets Accessed***************************\n")

            message = {
                'text': 'Slack Database Txn.\n Response Incoming.',
                'attachments': [
                    {
                        "color": "#3AA3E3",
                        "title": "Spreadsheet URL...",
                        'text': spreadsheet_url
                    }
                ]
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                response_url, data=json.dumps(message), headers=headers)
            print(currentThread().getName(),
                  'Ending db_student_details_worker')

        else:
            message = {'text': 'single'}

            # Create Spreadsheet
            sheets_id, spreadsheet_url, sheet_title, sheet_name = createsheets(
                "STUDENT DETAILS")
            range_row = 'A1'

            # Connect to Database & execute command
            fields = ('ID', 'STUDENT NAME',
                      'STUDENT IDNUM')
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql_select = """SELECT id, student_name,studentid_pp_no FROM dev_test.tbl_students where id = %s"""
            cur.execute(sql_select, (requested_id,))
            rows = cur.fetchall()
            cur.close()
            rows.insert(0, fields)
            pprint(rows)
            data = {'values': rows}

            # update the rows
            updatesheets(sheets_id, range_row, data)
            print("\n**************Updated Sheet Successfully*******************\n")

            # get the rows from the Sheet to appear in terminal
            print("*************Attempting to Access sheets Now...**************\n")
            getsheets(sheets_id, sheet_name)
            print("\n*****************Sheets Accessed***************************\n")

            message = {
                'text': 'Slack Database Txn.\n Response Incoming.',
                'attachments': [
                    {
                        "color": "#3AA3E3",
                        "title": "Spreadsheet URL...",
                        'text': spreadsheet_url
                    }
                ]
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                response_url, data=json.dumps(message), headers=headers)
            print(currentThread().getName(),
                  'Ending db_student_details_worker')

    except Exception as err:
        pprint(err)
        response = "General Error"

    return response
