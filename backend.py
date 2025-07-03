from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Ανάγνωση credentials από μεταβλητή περιβάλλοντος στο Render
credentials_json = os.environ.get("GOOGLE_CREDS_JSON")
if not credentials_json:
    raise Exception("Λείπει η μεταβλητή GOOGLE_CREDS_JSON")

# Σύνδεση με Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Άνοιγμα Google Sheet
sheet = client.open("Εγγραφές Landing").sheet1

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    fullname = data.get('fullname')
    phone = data.get('phone')
    email = data.get('email')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_records = sheet.get_all_values()
    next_id = len(all_records)

    sheet.append_row([next_id, fullname, phone, email, timestamp])
    return jsonify({"success": True, "message": "Εγγραφή στο Google Sheet επιτυχής."})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
