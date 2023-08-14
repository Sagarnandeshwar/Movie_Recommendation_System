import rsmodel
from rsmodel import train
from argument import get_args
import sys

if __name__ == "__main__":
    args = get_args()
    if eval(args.train_test):
        args.version = "_test"+args.version
        train(model=args.model_name, dataset='movie', config_list=["./model/MultiVAE_test.yaml"], load_pretrain=eval(args.load_pretrain), model_file='./model/saved/BPR1.0.pth', version=args.version)
    else:
        train(model=args.model_name, dataset='movie', config_list=[args.config_list], load_pretrain=eval(args.load_pretrain), model_file='./model/saved/BPR1.0.pth', version=args.version, show_progress=eval(args.show_progress))

def train_from_cd(version_number):
    args = get_args()
    return train(model=args.model_name, dataset='movie', config_list=[args.config_list], load_pretrain=eval(args.load_pretrain), model_file='./model/saved/BPR1.0.pth', version=version_number, show_progress=eval(args.show_progress))