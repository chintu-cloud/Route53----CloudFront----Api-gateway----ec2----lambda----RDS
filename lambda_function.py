import json
import os
import pymysql

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

def lambda_handler(event, context):
    try:
        return page_router(
            event['httpMethod'],
            event.get('queryStringParameters'),
            event.get('body')
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def page_router(httpmethod, querystring, formbody):
    if httpmethod == 'GET':
        # Serve the HTML form
        with open('index.html', 'r') as f:
            htmlContent = f.read()
        return {
            'statusCode': 200,
            'headers': {"Content-Type": "text/html"},
            'body': htmlContent
        }

    elif httpmethod == 'POST':
        # Insert form data to RDS
        insert_record(formbody)
        # Serve success page
        with open('success.html', 'r') as f:
            htmlContent = f.read()
        return {
            'statusCode': 200,
            'headers': {"Content-Type": "text/html"},
            'body': htmlContent
        }

def insert_record(formbody):
    # Parse URL-encoded form body into dictionary
    data_pairs = [pair.split('=') for pair in formbody.split('&')]
    data_dict = {k: v for k, v in data_pairs}

    # Connect to RDS
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            # Insert into your actual columns: username, email
            sql = "INSERT INTO dev (username, email) VALUES (%s, %s)"
            cursor.execute(sql, (data_dict.get('username'), data_dict.get('email')))
        conn.commit()
    finally:
        conn.close()
