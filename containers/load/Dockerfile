FROM python:3.9.2-slim

# location of code
WORKDIR /code
ENV PYTHONPATH=/code/src

# install cron
RUN apt-get update && apt-get install cron -y

# install python requirements
ADD ./containers/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy repo
COPY ./ /code/

# copy to the cron.d directory
COPY /scheduler/pull_crypto /etc/cron.d/pull_crypto

# execution rights on cron job
RUN chmod 0644 /etc/cron.d/pull_crypto

# apply cron job
RUN crontab /etc/cron.d/pull_crypto

# create the log to be able to run tail
RUN touch /var/log/cron.log

# run cron
CMD cron && tail -f /var/log/cron.log