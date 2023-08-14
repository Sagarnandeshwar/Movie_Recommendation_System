# Usage:
# python3 run_evaluation.py [path]

# Parameters:
# [path] required: path to directory location of user_store.json

from datetime import datetime, timedelta
import utils.kafka_utils as kafka_utils
from kafka import TopicPartition
import utils.user_utils as user_utils
import sys
import os.path
import evaluation

topic = 'movielog4'

def collect_logs_timeframe(date_in, date_out):
    consumer = kafka_utils.get_consumer()
    consumer.poll()  # we need to read message or call dumb poll before seeking the right position

    tp = TopicPartition(topic, 0)
    
    rec_in  = consumer.offsets_for_times({tp:date_in.timestamp() * 1000})
    rec_out = consumer.offsets_for_times({tp:date_out.timestamp() * 1000})

    consumer.seek(tp, rec_in[tp].offset) # lets go to the first message in New Year!

    logs = []

    c = 0
    for msg in consumer:
        logs.append(msg.value)

        if msg.offset >= rec_out[tp].offset:
            break

        c += 1
    # print("{c} messages between {_in} and {_out}".format(c=c, _in=str(date_in), _out=str(date_out)))
    return logs

def collect_parsed_log_action(log, args):
    user_store = args[0]
    
    type = kafka_utils.get_log_type(log)
    content = None

    # if it's type is watch
    if type == "watch":
        content = watch_store.update_watch_store(log)
        user_store.add_watch_data(content)
    # if it's type is rate
    if type == "rate":
        content = rate_store.update_rate_store(log)
        user_store.add_rating(content)
    # if it's type is request
    if type == "request":
        content = kafka_utils.parse_request_log(log)
        user_store.take_predictions(content)
    
if __name__ == '__main__':
    arg_data_path = sys.argv[1]

    # argument verification
    if not (os.path.exists(arg_data_path) and os.path.isdir(arg_data_path)):
        print("path doesnt exist")
        sys.exit(1)
    
    # data path
    data_path = os.path.join(arg_data_path, 'user_store.json')

    # calculate timeframe
    date_in  = datetime.now() - timedelta(hours=12) - timedelta(seconds=1)
    date_out = datetime.now() - timedelta(seconds=1)
    # get logs within timeframe
    logs = collect_logs_timeframe(date_in, date_out)
    # user_store object
    user_store = user_utils.UserPredictionStore()

    # parse log data and add to user_store
    kafka_utils.for_each_log(logs, collect_parsed_log_action, user_store)

    # create user_store.json
    user_store.get_user_store_json(data_path)
    
    # run evaluation
    evaluation.telemetry_data(user_store, arg_data_path)
    evaluation.evaluate_model(user_store, arg_data_path)
