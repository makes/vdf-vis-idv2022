FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD bokeh serve --show . --allow-websocket-origin vdf-vis.herokuapp.com --port $PORT
