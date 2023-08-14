import csv
from datetime import datetime

def split_name(name):
    location, source, sensor = name.strip().split('/')
    return location, source, sensor

def convert_to_phe_record(sensors, sensor_id, value, timestamp):
    sensor_id, source, location, sensor = sensors[sensor_id]
    return "input_event_instant({}({},{},{}),{}).".format(sensor, source, location, value, timestamp)

def convert_to_epoch(timestamp_str):
    datetime_obj = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
    epoch_timestamp = int(datetime_obj.timestamp() * 1000)  # Convert to milliseconds
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
     open('./sensordata.csv', 'w') as outfile:

    float_reader = csv.DictReader(float_data, delimiter=',')
    int_reader = csv.DictReader(int_data, delimiter=',')
    int_t = 0
    float_t = 0

    int_record = next(int_reader, None)
    float_record = next(float_reader, None)
    
    while float_reader is not None and int_reader is not None:
        
        if int_record is not None:
            int_t = convert_to_epoch(int_record['timestamp'])
        if float_record is not None:
            float_t = convert_to_epoch(float_record['timestamp'])
        
        if int_t < float_t:
            record =  int_record
            int_record = next(int_reader, None)
        else:
            record  = float_record
            float_record = next(float_reader, None)
        
        value_id = record['value_id']
        sensor_id = record['sensor_id']
        timestamp = convert_to_epoch(record['timestamp'])
        value = record['value']
        phenesthe_record = convert_to_phe_record(sensors, sensor_id, value, timestamp)
        outfile.write(phenesthe_record + '\n')

