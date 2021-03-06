FROM python:3

#updates
RUN apt-get update -y

#port to use app
EXPOSE 5000

# Add application to app dir
ADD . /app
WORKDIR /app

# Install requirements
RUN pip install -r /app/requirements.txt

#run command
ENTRYPOINT ["python"]
CMD ["app.py"]
