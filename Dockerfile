#Builder Stage - add the requirements
FROM python:alpine3.21 as Builder

WORKDIR /app

COPY requirements.txt .

#prefix=/install install the requirements.txt to a new path /install which will be ez to grap later in runtime
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt 

#Runtime Stage - Run the python app 
FROM python:alpine3.21 as Runtime

WORKDIR /app

#copy from the stage builder the /install to /usr/local which is the default place for pip to install to  
COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5001

ENV PORT=5001

CMD ["python", "main.py"]


