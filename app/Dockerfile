FROM python:3.13-alpine
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY upload_old_data.py upload_old_data.py
CMD ["python", "-u", "upload_old_data.py"]