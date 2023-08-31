import paho.mqtt.client as mqtt
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    client.subscribe("databiota/co2")

def on_message(client, userdata, msg):
    print("Topik: " + msg.topic + " - Pesan: " + msg.payload.decode())
    
    data = json.loads(msg.payload.decode())
    co2Input = data.get("co2Input")
    co2Output = data.get("co2Output")
    print("co2Input:", co2Input)
    print("co2Output:", co2Output)

    # Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
    gspread_client = gspread.authorize(credentials)

    spreadsheet = gspread_client.open_by_url('https://docs.google.com/spreadsheets/d/1YQ0jEzjVzSNQMff9rH0Vu-7PcldXzE5V_3l8kavfvdc/edit?usp=sharing')
    worksheet = spreadsheet.get_worksheet(0)

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    data_to_insert = [formatted_time, co2Input, co2Output]

    # Masukkan data ke baris baru di bagian atas worksheet
    worksheet.insert_row(data_to_insert, 2)

# MQTT Client Setup
client = mqtt.Client("client-2")
client.on_connect = on_connect
client.on_message = on_message
client.connect("test.mosquitto.org", 1883, 60)

# MQTT Loop
client.loop_forever()
