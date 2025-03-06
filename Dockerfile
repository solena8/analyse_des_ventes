FROM python:3.12-slim
# image to use

WORKDIR /app
#word directory in the container from where the next commands will be executed

COPY requirements.txt .
#copy the dependencies file

RUN pip install --no-cache-dir -r requirements.txt
#install the dependencies in the countainer

CMD ["python", "/app/analyse_des_ventes/main.py"]
#tells which default command will be executed when the container will start.
#here main.py with the interpreter python