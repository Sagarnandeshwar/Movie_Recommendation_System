import argparse

"""
Here are the param for the training

"""


def get_args():
    parser = argparse.ArgumentParser("COMP585 recommendation system")
    # model info
    parser.add_argument("--model-name", type=str, default="MultiVAE")
    parser.add_argument("--config-list", type=str, default="./model/MultiVAE.yaml")
    parser.add_argument("--version", type=str, default="1.0")
    

    # train info
    parser.add_argument("--load-pretrain", type=str, default="False")
    parser.add_argument("--train-test", type=str, default="False")
    parser.add_argument("--show-progress", type=str, default="False")

    args = parser.parse_args()

    return args