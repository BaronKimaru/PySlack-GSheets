from terminaltables import AsciiTable
import psycopg2
import json
import requests
from threading import currentThread
from app.dbconnect import connect
conn = connect()

#### THIS COMES INTO USE IF YOU ARE JUST LOOKING TO WORK WITH FLASK & PYTHON, NO SHEETS ######


def indexOf(string, pattern):
    try:
        ret = string.index(pattern)
        print('found pattern')
        return ret
    except ValueError as e:
        print('no pattern')
        return -1


def call_db_student_details_worker(response_url, requested_id):
    print(currentThread().getName(), 'Starting db_student_details_worker')
    if (indexOf(requested_id, ':')) > -1:
        message = {'text': 'range'}
        ranges = requested_id.split(':')
        print(ranges)

        if (len(ranges) > 2):
            message = {'text': 'too many arguments'}

        else:
            conn = connect()
            if conn:
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                sql_select = "SELECT student_name,studentid_pp_no FROM dev_test.tbl_students where id BETWEEN %s and %s"
                cur.execute(sql_select, ranges)
                rows = cur.fetchall()
                table_data = rows
                table = AsciiTable(table_data)
                print(table.table)
                tabled_rows = '' + table.table + ''
                cur.close()

                message = {'text': tabled_rows}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(
                    response_url, data=json.dumps(message), headers=headers)
                print(currentThread().getName(),
                      'Ending db_student_details_worker')
                return response

    elif (indexOf(requested_id, ',')) > -1:
        message = {'text': 'options'}
        options = requested_id.split(',')
        options = tuple(options)
        print(options)
        conn = connect()
        if conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql_select = """SELECT student_name,studentid_pp_no FROM dev_test.tbl_students where id IN %s"""
            cur.execute(sql_select, (options,))
            rows = cur.fetchall()
            table_data = rows
            table = AsciiTable(table_data)
            print(table.table)
            tabled_rows = '' + table.table + ''
            cur.close()

            message = {'text': tabled_rows}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                response_url, data=json.dumps(message), headers=headers)
            print(currentThread().getName(),
                  'Ending db_student_details_worker')
            return response

    else:
        message = {'text': 'single'}
        conn = connect()
        if conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            sql_select = """SELECT student_name,studentid_pp_no FROM dev_test.tbl_students WHERE id = %s"""
            cur.execute(sql_select, (requested_id,))
            rows = cur.fetchall()
            table_data = rows
            table = AsciiTable(table_data)
            print(table.table)
            tabled_rows = '' + table.table + ''
            cur.close()

            message = {'text': tabled_rows}
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                response_url, data=json.dumps(message), headers=headers)
            print(currentThread().getName(),
                  'Ending db_student_details_worker')
            return {"text": response}
