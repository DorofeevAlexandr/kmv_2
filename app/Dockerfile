FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY config.py config.py
COPY upload_old_data.py upload_old_data.py
CMD ["python", "-u", "upload_old_data.py"]