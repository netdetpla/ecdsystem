FROM ubuntu:latest 

ADD ["sources.list", "/etc/apt/"]

RUN apt update \
    && cd / \
    && apt -y install python3 python3-pip \
    && pip3 install requests -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && apt clean

WORKDIR /

ADD ["ECD", "/"]

CMD python3 main.py

