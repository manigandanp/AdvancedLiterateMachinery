FROM registry.cn-hangzhou.aliyuncs.com/modelscope-repo/modelscope:ubuntu20.04-cuda11.3.0-py38-torch1.11.0-tf1.15.5-1.6.1

RUN apt-get update

RUN apt-get install libmagickwand-dev -y

COPY . /code/

WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r /code/Applications/DocXChain/requirements.txt

RUN pip install Wand

RUN sed -i '/disable ghostscript format types/,+6d' /etc/ImageMagick-6/policy.xml

RUN wget -c -t 100 -P /home/ https://github.com/AlibabaResearch/AdvancedLiterateMachinery/releases/download/v1.2.0-docX-release/DocXLayout_231012.pth

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "7000"]