FROM public.ecr.aws/lambda/python:3.10

# Set the working directory within the container
WORKDIR /usr/src/app

RUN yum update -y
RUN yum install -y nmap-ncat
RUN yum clean all

# Copy the necessary files
COPY . .
    
COPY migration.sh ./migration.sh
COPY version.py ./src/version.py

# Copy the wait-for-it script
RUN chmod +x ./migration.sh

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set PYTHONPATH
RUN export PYTHONPATH=${PYTHONPATH}:${PWD}

EXPOSE 8080

# Command to run Alembic migrations
ENTRYPOINT ["./migration.sh"]

