{
  "metadata": {
    "language_info": {
      "name": ""
    },
    "kernelspec": {
      "name": "python",
      "display_name": "Python (Pyodide)",
      "language": "python"
    }
  },
  "nbformat_minor": 4,
  "nbformat": 4,
  "cells": [
    {
      "cell_type": "code",
      "source": "import csv\nfrom datetime import datetime\n\ndef split_name(name):\n    location, source, sensor = name.strip().split('/')\n    return location, source, sensor\n\ndef convert_to_phe_record(sensors, sensor_id, value, timestamp):\n    sensor_id, source, location, sensor = sensors[sensor_id]\n    return \"input_event_instant({},({},{},{}),{}){}\".format(sensor_id, sensor, source, location, value, timestamp)\n\ndef convert_to_epoch(timestamp_str):\n    datetime_obj = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')\n    epoch_timestamp = int(datetime_obj.timestamp())  \n    return epoch_timestamp\n\nsensors = {}\n\nwith open('sensor.csv') as inp:\n    csv_reader = csv.DictReader(inp, delimiter=',')  \n    for line in csv_reader:\n        sensor_id, node_id, sensor, name = line['sensor_id'], line['node_id'], line['type'], line['name']\n        location, source, sensor = split_name(name)\n        sensors[sensor_id] = (sensor_id, source, location, sensor)\n\n\n\nwith open('sensor_sample_float.csv') as float_data, \\\n     open('sensor_sample_int.csv') as int_data, \\\n     open('converted_data.input', 'w') as outfile:\n    float_reader = csv.DictReader(float_data, delimiter=',')\n    for record in float_reader:\n        value_id = record['value_id']\n        sensor_id = record['sensor_id']\n        timestamp = record['timestamp']\n        value = record['value']\n\n       \n\n        epoch_timestamp = convert_to_epoch(timestamp)\n\n        phenesthe_record = convert_to_phe_record(sensors, sensor_id, value, epoch_timestamp)\n\n\n \n\n        outfile.write(phenesthe_record + '\\n')",
      "metadata": {},
      "execution_count": null,
      "outputs": []
    }
  ]
}