FROM python:3.12-slim
# image to use

WORKDIR /app
#word directory in the container from where the next commands will be executed


COPY . .
#first . means copies all the local files, second . means into the docker workdir
#(except what is in the dockignore file)

RUN pip install --no-cache-dir -r requirements.txt
#install the dependencies in the countainer

CMD ["python", "main.py"]
#tells which default command will be executed when the container will start.
#here main.py with the interpreter python