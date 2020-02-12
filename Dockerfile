FROM python


COPY . /app

WORKDIR /app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8050
#ENV NAME OpentoAll

CMD [ "python", "./app.py" ]
