FROM python:3.10

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .

RUN pip install -r requirements.txt
RUN mkdir -p storage && touch storage/data.json

EXPOSE 3000

CMD ["python", "main.py"]