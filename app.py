from flask import Flask, request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = Flask(__name__)

# Replace with your own Google Sheets API credentials
API_KEY = "YOUR_API_KEY"
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"


@app.route("/post-data", methods=["POST"])
def post_data():
    # Get the data from the request
    data = request.json

    # Set up the Google Sheets API client
    credentials = Credentials.from_authorized_user_info(info=request.json, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=credentials)

    # Call the Sheets API to append the data to the spreadsheet
    response = service.spreadsheets().values().append(
        spreadsheetId="YOUR_SPREADSHEET_ID",
        range="Sheet1!A1",
        valueInputOption="RAW",
        body={"values": [data]}
    ).execute()

    return response


@app.route("/get-data", methods=["GET"])
def get_data():
    # Set up the Google Sheets API client
    credentials = Credentials.from_authorized_user_info(info=request.json, scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=credentials)

    # Call the Sheets API to retrieve the data from the spreadsheet
    response = service.spreadsheets().values().get(
        spreadsheetId="YOUR_SPREADSHEET_ID",
        range="Sheet1!A1:Z"
    ).execute()

    # Extract the data from the response and return it
    values = response.get("values", [])
    return values


if __name__ == '__main__':
    app.run()
