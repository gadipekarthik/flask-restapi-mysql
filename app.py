from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Replace with connection details from environment variables
config = {
    'host': 'mysql',
    'user': 'root',
    'password': 'test123',
    'database': 'test_db'
}

@app.route('/')
def index():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM employees')  # Replace with your table name
    result = cursor.fetchall()
    connection.close()

    # Convert data to JSON format
    data = []
    for row in result:
        data.append(dict(zip([col[0] for col in cursor.description], row)))

    return jsonify(data)  # Return data as JSON

@app.route('/data', methods=['POST'])
def insert_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Get data from JSON request body
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400  # Bad request

    # Extract data from JSON
    name = data.get('name')
    age = data.get('age')
    salary = data.get('salary')

    # Validate data (optional)
    # ...

    # Prepare SQL statement (consider using parameterized queries for security)
    sql = f"INSERT INTO employees (name, age, salary) VALUES (%s, %s, %s)"

    try:
        cursor.execute(sql, (name, age, salary))
        connection.commit()
        return jsonify({'message': 'Data inserted successfully'}), 201  # Created
    except mysql.connector.Error as err:
        connection.rollback()
        return jsonify({'error': str(err)}), 500  # Internal server error
    finally:
        connection.close()




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run development server