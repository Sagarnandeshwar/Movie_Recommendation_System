# train & deploy: python3 auto_deployment.py [is_test_env] [# of logs for training]

# Parameters:
# [is_test_env]: set to true by default, will deploy the model to dev env(which has a lower weight for user requests)
# set to false to deploy to production env
# [# of logs for training]: set to 50,000 by default

import os
import re
import sys
import subprocess
from os.path import exists
from train import train_from_cd
from email_sender import send_email

# subprocess.run(["git", "restore", "."])
subprocess.run(["git", "pull"])

deploy_to_test = len(sys.argv) < 2 or sys.argv[1].lower() != "false"
env_name = "development environment" if deploy_to_test else "production environment"
if deploy_to_test:
    num_of_logs = "100000" if len(sys.argv) < 3 or not sys.argv[2].isdigit() else sys.argv[2]
    subprocess.run(["python3", "data_collection/collect_processed.py", "data", num_of_logs])
    subprocess.run(["python3", "model/process.py"])
    sys.stdout.write("========Successfully Processed Data, Start Training========")
    current_version = ""
    with open("model/saved/current_version.txt", "r") as f:
        current_version = f.read()
    next_version = str(int(current_version) + 1)
    offline_test_result = train_from_cd(next_version)
    sys.stdout.write(str(offline_test_result))
    recall_result = offline_test_result["test_result"]["recall@20"]

    if recall_result < 0.15:
        print("Your deployment of latest model to development environment is aborted! The minimum performance requirement is not met for the new model. ")
        send_email("[CD Failed] Movie recommandation system deployment", "Your deployment of latest model BPR"+ next_version +".pth to " + env_name + "is aborted! The minimum performance requirement is not met for the new model.Now the perforemance is Recall={}".format(recall_result))
        exit()
    else:
        # subprocess.run(["git", "pull"])
        with open("model/saved/current_version.txt", "w") as f:
                f.write(next_version)
        subprocess.run(["git", "add", "data"])
        subprocess.run(["git", "add", "model/saved/current_version.txt"])
        subprocess.run(["git", "add", "tests/logs/auto_deployment.log"])
        subprocess.run(["git", "commit", "-m", "continous_delivery_commit_latest_model_for_test_env with version " + next_version])
        subprocess.run(["git", "push"])

        send_email("[CD Succ] Movie recommandation system deployment", "Your deployment of latest model BPR"+ next_version +".pth to " + env_name + "is successful!\n"+ str(offline_test_result))


if deploy_to_test:
    subprocess.run(["docker", "build", "-t", "movierecc4:next", "."])
    os.system("TAG=next docker-compose up --build -d --force-recreate app_next")
    # subprocess.run(["TAG=next", "docker-compose", "up", "--build", "-d", "--force-recreate", "app_next"])
else:
    subprocess.run(["docker", "build", "-t", "movierecc4:stable", "."])
    os.system("TAG=stable docker-compose up --build -d --force-recreate app_stable")
    # subprocess.run(["TAG=stable", "docker-compose", "up", "--build", "-d", "--force-recreate", "app_stable"])

