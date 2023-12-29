# Backend Containerfile

FROM registry.redhat.io/rhel8/python-311

LABEL description="Clinic Backend image"

# created env variables with default values (can be overrided from podman run)
ENV BACKEND_SERVER_PORT=5000
ENV BACKEND_URL=0.0.0.0

EXPOSE $BACKEND_SERVER_PORT

RUN pip install flask==2.3.3 flask-mysql flask-cors pika

COPY Pipelines/Backend/clinic-reservation-system/ /opt/source-code	

# ENTRYPOINT FLASK_APP=/opt/source-code/app.py flask run

WORKDIR /opt/source-code

# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Error in substituting ENVs
# CMD ["flask", "run", "--host=$BACKEND_URL", "--port=$BACKEND_SERVER_PORT"]

# invoke a shell  to expand the ENV before running flask
CMD sh -c 'flask run --host=$BACKEND_URL --port=$BACKEND_SERVER_PORT'




