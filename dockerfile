FROM python:3.9-alpine3.13
LABEL maintainer="Ruben Rocha"

ENV PYTHONUNBUFFERED 1

# copies our local requirements.txt to to a temp folder in our docker image
# it will allow us to have all the same requirements in our image as locally
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#Copies local app files into app folder on our image
COPY ./app /app
WORKDIR /app
#image we will be able to access from our image
EXPOSE 8001
#sets DEV, we use this file for deployment, so dev files will not be needed
ARG DEV=false
# creates new venv to store dependencies
RUN python -m venv /py && \
#upgrades pip for the venv
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
        #installs all requirements into our venv
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    #removes all of our temp files once we're done using them
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    #add user to prevent using root user
    adduser --disabled-password --no-create-home django-user

#this ensure anytime we run a CLI command it'll run from the venv
ENV PATH="/py/bin:$PATH"

#define the user we're using to run app
USER django-user