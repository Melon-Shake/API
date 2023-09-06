# 
FROM python:3.9

# 
WORKDIR /API

#
RUN mkdir src
RUN mkdir config
RUN mkdir model
RUN mkdir lib

#
COPY requirements.txt .
COPY config/* config/
COPY model/* model/
COPY src/* src/
COPY lib/* lib/
#
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/API"
ENV PYTHONPATH "${PYTHONPATH}:/API/src"


# 
CMD uvicorn src.TotalApi:app --host "0.0.0.0" --port 8000 --reload --log-level info

