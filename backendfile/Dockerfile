FROM python:3.8

# Expose the port the app runs in
EXPOSE 5000

# Install JDK for Lucene
RUN apt-get update && apt-get install -y default-jdk ant
WORKDIR /usr/lib/jvm/default-java/jre/lib
RUN ln -s ../../lib amd64

# Install Lucene
WORKDIR /usr/src/pylucene
# if it returns an error, check the available version
RUN curl http://apache.uvigo.es/lucene/pylucene/pylucene-8.3.0-src.tar.gz | tar -xz --strip-components=1
RUN cd jcc && NO_SHARED=1 JCC_JDK=/usr/lib/jvm/default-java python setup.py install
RUN make all install JCC='python -m jcc' ANT=ant PYTHON=python NUM_FILES=8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1


# Create a directory where our app will be placed
RUN mkdir -p /usr/src/app

# Change directory so that our commands run inside this new directory
WORKDIR /usr/src/app

# Copy dependency definitions
COPY requirements.txt /usr/src/app/requirements.txt

# Install dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Get all the code needed to run the app
COPY . /usr/src/app

# Serve the app
CMD gunicorn -w 10 appFile:app --bind 0.0.0.0:5000
#CMD gunicorn appFile:app --bind 0.0.0.0:5000
