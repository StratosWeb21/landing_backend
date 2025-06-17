from flask import Flask, request, jsonify
import pandas as pd
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EXCEL_FILE = 'registrations.xlsx'

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["ID", "Ονοματεπώνυμο", "Τηλέφωνο", "Email", "Ημερομηνία"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    fullname = data.get('fullname')
    phone = data.get('phone')
    email = data.get('email')

    df = pd.read_excel(EXCEL_FILE)
    next_id = 1 if df.empty else df['ID'].max() + 1

    new_entry = {
        "ID": next_id,
        "Ονοματεπώνυμο": fullname,
        "Τηλέφωνο": phone,
        "Email": email,
        "Ημερομηνία": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    return jsonify({"success": True, "message": "Εγγραφή επιτυχής."})

if __name__ == '__main__':
    app.run(debug=True)
