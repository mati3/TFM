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

# lupyne
RUN pip install lupyne

#RUN tar xzvf jdk-8u261-linux-x64.tar.gz
#RUN mkdir /usr/lib/jvm/
#RUN mv jdk1.8.0_261/ /usr/lib/jvm/jdk1.8.0_261
#RUN update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_261/bin/java" 0
#RUN update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.8.0_261/bin/javac" 0
#RUN update-alternatives --set java /usr/lib/jvm/jdk1.8.0_261/bin/java
#RUN update-alternatives --set javac /usr/lib/jvm/jdk1.8.0_261/bin/javac
#RUN export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_261
#RUN export PATH=$PATH:$JAVA_HOME/bin

#RUN svn co https://svn.apache.org/repos/asf/lucene/pylucene/trunk/jcc jcc
# cambiar en archivo setup.py oracle 8 por jdk1.8.0_261
#RUN sed -i 's/java-8-oracle/jdk1.8.0_261/g' jcc/setup.py
#RUN python jcc/setup.py build
#RUN python jcc/setup.py install

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
#CMD [ "python", "./appCesta.py" ]
CMD gunicorn appFile:app --bind 0.0.0.0:5000
