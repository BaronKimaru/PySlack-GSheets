import psycopg2
import os

def connect(self):
		""" Connects to the the Database """
		conn = cur = None
		response = None
		try:
			conn  = psycopg2.connect(
									dbname = os.environ.get("DBWORKDATABASE"), 
									user = os.environ.get("DBWORKUSER"), 
									password = os.environ.get("DBWORKPASSWORD"), 
									host = os.environ.get("DBWORKHOST")
									)
			if conn:
				print(f"conn is: {conn}")
				cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
				if cur: 
					print(cur)
					response = f"Connection as {conn} & cursor as {cur}"
					
		except Exception as e:
			pprint(e)
			response = f"Error in Creating Spreadsheet: {e} "
			
		finally:
			return cur, conn, response
			
			
			
if __name__ == "__main__":
	connect()