from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection
def connect_database():
    return mysql.connector.connect(
        host="localhost",  # Change as needed
        user="root",  # Change as needed
        password="hari",  # Change as needed
        database="contactmanagement"  # Updated database name
    )

# Get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        conn = connect_database()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        conn.close()
        return jsonify(contacts)
    except Exception as e:
        return jsonify({"error": str(e)})

# Add new contact
@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    gender = data.get('gender')
    age = data.get('age')
    address = data.get('address')
    contact = data.get('contact')

    if not firstname or not lastname or not gender or not age or not address or not contact:
        return jsonify({"error": "All fields are required!"})

    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contacts (Firstname, Lastname, Gender, Age, Address, Contact)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (firstname, lastname, gender, age, address, contact))
        conn.commit()
        conn.close()
        return jsonify({"message": "Contact added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Delete contact
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Contact deleted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
