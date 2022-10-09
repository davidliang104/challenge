FROM python:3.10

#Set our working directory as app
WORKDIR /app

#Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the relevant directories
COPY model/ ./model
COPY . .

CMD ["python", "app.py"]