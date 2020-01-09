from datetime import datetime

import json
import urllib.request
from influxdb import InfluxDBClient

location = "capelle aan den ijssel"
weerlive_apikey = ""
influxdb_host = ""
influxdb_dbname = ""
influxdb_username = ""
influxdb_password = ""
idx = ""

with urllib.request.urlopen(
        "http://weerlive.nl/api/json-data-10min.php?key=" + weerlive_apikey + "&locatie=" +
        urllib.parse.quote(location)) as url:
    data = json.loads(url.read().decode())
    client = InfluxDBClient(host=influxdb_host, port=8086, username=influxdb_username,
                            password=influxdb_password)
    client.switch_database(influxdb_dbname)
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body = [
        {
            "measurement": "Temperature",
            "tags": {
                "idx": idx,
                "name": "Outside temperature",
            },
            "time": current_time,
            "fields": {
                "value": float(data["liveweer"][0]["temp"])
            }
        },
        {
            "measurement": "Humidity",
            "tags": {
                "idx": idx,
                "name": "Outside humidity",
            },
            "time": current_time,
            "fields": {
                "value": float(data["liveweer"][0]["lv"])
            }
        }
    ]
    client.write_points(json_body)
