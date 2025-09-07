#Builder Stage - add the requirements
FROM python:3.11 as Builder 

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#Runtime Stage - Run the python app 
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /install /usr/local

COPY . .

EXPOSE 5001

ENV PORT=5001

CMD ["python", "main.py"]