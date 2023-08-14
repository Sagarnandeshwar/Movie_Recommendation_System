FROM ubuntu:18.04

RUN useradd -ms /bin/bash -g root -G sudo user1

RUN apt-get update
RUN apt-get install python3.8 -y
RUN apt-get install python3-pip -y

USER user1
WORKDIR /home/user1

COPY . .

# COPY requirements.txt .

RUN echo '#!/bin/bash' > api_run.sh
RUN echo 'pip3 install --upgrade pip' >> api_run.sh
RUN echo 'pip3 install flask' >> api_run.sh
RUN echo 'pip3 install kafka-python' >> api_run.sh
RUN echo 'pip3 install requests' >> api_run.sh
RUN echo 'pip3 install pandas' >> api_run.sh
RUN echo 'pip3 install tqdm' >> api_run.sh
RUN echo 'pip3 install scipy' >> api_run.sh
RUN echo "pip3 install colorlog" >> api_run.sh
RUN echo "pip3 install scikit-learn" >> api_run.sh
RUN echo "pip3 install torch --no-cache-dir" >> api_run.sh
RUN echo "pip3 install pyyaml==5.1.0" >> api_run.sh
RUN echo "pip3 install colorama==0.4.4" >> api_run.sh
RUN echo "pip3 install tensorboard" >> api_run.sh
RUN echo "pip3 install prometheus-flask-exporter" >> api_run.sh
# RUN echo 'pip3 install -r requirements.txt' >> api_run.sh
RUN echo 'python3 api.py' >> api_run.sh

RUN chmod +x api_run.sh

EXPOSE 8082

CMD /home/user1/api_run.sh