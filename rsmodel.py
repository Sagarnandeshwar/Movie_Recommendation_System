from model.recbole.quick_start import run_recbole, load_data_and_model
from model.recbole.utils.case_study import full_sort_topk
from model.recbole.config import Config
from model.recbole.utils import get_model, get_trainer, set_color
from model.recbole.data import create_dataset, data_preparation
from logging import getLogger
import logging
import numpy as np
import pandas as pd
import random
import torch
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def train(model="BPR", dataset='movie', config_list=["./model/BPR.yaml"], load_pretrain=False, model_file='./model/saved/BPR1.0.pth', version=0.0, show_progress=True):
    model_file = model_file
    if not load_pretrain:
        result = run_recbole(model=model, dataset=dataset, config_file_list=config_list, show_config_info=False, show_split_info=True, show_progress=show_progress, version=version)
    else:
        logger = getLogger()
        checkpoint = torch.load(model_file)
        config = checkpoint['config']
        config["version"] = version
        config = Config(model=config['model'], dataset=dataset, config_file_list=config_list)
        config['show_progress'] = show_progress
        dataset = create_dataset(config)
        train_data, valid_data, test_data = data_preparation(config, dataset)
        model = get_model(config['model'])(config, train_data.dataset).to(config['device'])
        model.load_state_dict(checkpoint['state_dict'])
        model.load_other_parameter(checkpoint.get('other_parameter'))
       
        trainer = get_trainer(config['MODEL_TYPE'], config['model'])(config, model)
        # model training
        best_valid_score, best_valid_result = trainer.fit(train_data, valid_data, saved=True, show_progress=config['show_progress'])
        # model evaluation
        test_result = trainer.evaluate(test_data, load_best_model=True, show_progress=config['show_progress'])
        
        logger.info(set_color('best valid ', 'yellow') + f': {best_valid_result}')
        logger.info(set_color('test result', 'yellow') + f': {test_result}')
        result = {
        'best_valid_score': best_valid_score,
        'valid_score_bigger': config['valid_metric_bigger'],
        'best_valid_result': best_valid_result,
        'test_result': test_result
    }
    return result


def load_model(model_path='./model/saved/BPR1.0.pth'):
    model = load_data_and_model(model_file=model_path, movie_config=["./model/movie.yaml"], dataset='movie')
    return model

def predict(userid, high_rating, model, model_name='MultiVAE', item=None, user=None, test_data=None, dataset=None, config=None):

    # config = Config(model=model_name, dataset=dataset, config_file_list=config)
    # dataset = create_dataset(config)
    # _, _, test_data = data_preparation(config, dataset)
    # user_id = userid
    user = user
    item = item
    if int(userid) in user:
        # config = Config(model=model_name, dataset=dataset, config_file_list=config)
        # dataset = create_dataset(config)
        # _, _, test_data = data_preparation(config, dataset)
        uid_series = dataset.token2id(dataset.uid_field, [userid])
        _, topk_iid_list = full_sort_topk(uid_series, model, test_data, k=20)
        external_item_list = dataset.id2token(dataset.iid_field, topk_iid_list)
        del uid_series
        del topk_iid_list
        ids = external_item_list[0]
        ids = [int(i) for i in ids]
        movie_ids = item.loc[item['tmdb_id:token'].isin(ids)]["movie_id:token_seq"].to_list()
    else:
        high_rating_movie = high_rating
        movie_ids = []
        split = np.array_split(high_rating_movie, 20)
        for ele in split:
            movie_id = random.choice(ele)
            movie_ids.append(movie_id)
        
    
    return movie_ids

if __name__ == "__main__":
    pass