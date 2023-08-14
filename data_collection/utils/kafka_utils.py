from .rest_api_utils import get_user_info, get_movie_info
from kafka import KafkaConsumer
import os
import csv
import math
import random
from tqdm import tqdm
server = 'fall2022-comp585.cs.mcgill.ca:9092'
topic = 'movielog4'
log_set = set()

# gets kafka consumer
def get_consumer():
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=server,
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )

    return consumer

def parse_request_log(log):
    log_data = log.split(",")
    if len(log_data) < 4:
        return
    server = log_data[2].replace('recommendation request ', '')
    code = log_data[3].replace(' status ', '')

    new_log = {
        "timestamp": log_data[0],
        "userid": log_data[1],
        "server": server,
        "code": code,
        "predictions": [],
        "response_time": log_data[-1].strip()
    }

    movies_split = log_data[4:]
    movies_split.pop()
    movies_split[0] = movies_split[0].replace(' result: ', '')
    movies_split = [m.strip(' ') for m in movies_split]
    new_log["predictions"] = movies_split
    return new_log

# gets log type from log (as string)
def get_log_type(log):
    log_data = log.split(",")
    watching = '/data/' in log_data[2]
    rating = '/rate/' in log_data[2]
    
    if watching:
        return "watch"
    elif rating:
        return "rate"
    else:
        return "request"

# gets string[] of logs from filepath
def get_logs_from_file(filepath):
    # df = pd.read_csv(f'../data/{filepath}')
    kafka_stream = open(filepath, "r").read().split("\n")
    rows = kafka_stream[0:]
    random.shuffle(rows)
    kafka_stream = rows
    return kafka_stream

def get_log_file_from_kafka(filepath, amount, rating_only=False):
    print("Begin kafka log collection")
    consumer = get_consumer()
    curr = 0
    log_set = set()
    with open (filepath,'w+') as data_file:
        csv_writer = csv.writer(data_file)
        
        for log in consumer:
            log_data = log.value.split(",")

            if not validate_log_data(log_data, rating_only):
                continue
            
            csv_writer.writerow(log_data)
            curr += 1

            if curr % (amount/100) == 0:
                print(str(math.floor((curr/amount)*100)) + "%", end='\r')

            if curr >= amount:
                break

        data_file.close()
    
    print("{amount} logs collected in {filepath}".format(amount=amount, filepath=filepath))


def for_each_log(logs, action, *args):
    print("Start action on logs")
    total_count = len(logs)
    curr = 0
    count_err = 0
    error_logs = []

    for log in tqdm(logs):
        if log == "":
            continue
        
        try:
            action(log, args)
        except:
            count_err += 1
            error_logs.append(str(log))
            continue

        curr += 1
        # if curr % (total_count/100) == 0:
        #     print(str(math.floor((curr/total_count)*100)) + "%", end='\r')
    
    for err in error_logs:
        print("ERROR: "+err)

    print("Completed action on {total_count} logs".format(total_count=total_count))
    print(str(count_err) + " errors detected")


def list_items_to_key(info_list):
    key = ""
    for info in info_list:
        key += info + ";"

    return key

def validate_log_data(log_data, rating_only=False):
    if len(log_data) < 3:
        return False

    if rating_only and "/rate/" not in log_data[2]:
        return False

    key = list_items_to_key(log_data)
    if key in log_set:
        return False
            
    log_set.add(key)
    return True

def get_movie_on_rate(rate_file, movie_store):
    movie_ids = set(rate_file.iloc[:,2])
    for id in tqdm(movie_ids):
        movie_store.update_movie_info(id)
    return movie_store
