#Builder Stage - add the requirements
FROM python:alpine3.21 as Builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#Runtime Stage - Run the python app 
FROM python:alpine3.21 as Runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5001

ENV PORT=5001

CMD ["python", "main.py"]


