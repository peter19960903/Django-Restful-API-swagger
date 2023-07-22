FROM python:3.10
WORKDIR /DRF_BACKEND
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py" , "runserver", "0.0.0.0:8000"]