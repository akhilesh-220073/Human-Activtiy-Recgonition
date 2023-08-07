import csv
from datetime import datetime

def split_name(name):
    location, source, sensor = name.strip().split('/')
    return location, source, sensor

def convert_to_phe_record(sensors, sensor_id, value, timestamp):
    sensor_id, source, location, sensor = sensors[sensor_id]
    return "input_event_instant({}({},{},{},{}),{}".format(sensor_id, sensor, source, location, value, timestamp)

def convert_to_epoch(timestamp_str):
    datetime_obj = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
    epoch_timestamp = int(datetime_obj.timestamp())  
    return epoch_timestamp

sensors = {}

with open('D:\human_activity_raw_sensor_data\sensor.csv') as inp:
    csv_reader = csv.DictReader(inp, delimiter=',')  
    for line in csv_reader:
        sensor_id, node_id, sensor, name = line['sensor_id'], line['node_id'], line['type'], line['name']
        location, source, sensor = split_name(name)
        sensors[sensor_id] = (sensor_id, source, location, sensor)



with open('D:\human_activity_raw_sensor_data\sensor_sample_float.csv') as float_data, \
     open('D:\human_activity_raw_sensor_data\sensor_sample_int.csv') as int_data, \
     open('converted_data.input', 'w') as outfile:
    float_reader = csv.DictReader(float_data, delimiter=',')
    for record in float_reader:
        value_id = record['value_id']
        sensor_id = record['sensor_id']
        timestamp = record['timestamp']
        value = record['value']

    int_reader = csv.DictReader(int_data,delimiter=',')
    for record in int_reader:
        value_id = record['value_id']
        sensor_id = record['sensor_id']
        timestamp = record['timestamp']
        value = record['value']

        epoch_timestamp = convert_to_epoch(timestamp)

        phenesthe_record = convert_to_phe_record(sensors, sensor_id, value, epoch_timestamp)


 

        outfile.write(phenesthe_record + '\n')
