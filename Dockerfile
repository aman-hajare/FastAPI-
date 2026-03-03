FROM python:3.11.0

WORKDIR /src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src/app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]