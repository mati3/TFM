# base image
FROM node

# set working directory
WORKDIR /myapp/frontend

# install chrome for protractor tests
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -yq google-chrome-stable

# add `/app/node_modules/.bin` to $PATH
ENV PATH /myapp/frontend/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /myapp/frontend/package.json
RUN npm install
RUN npm install -g @angular/cli
# paginación
RUN npm install ngx-pagination --save
# documentación
RUN npm install --save-dev @compodoc/compodoc 
# documentación typeScript
RUN npm install --global typedoc

# add app
#COPY . .

# start app
CMD ng serve --ssl true --host 0.0.0.0
#CMD ng serve --host 0.0.0.0
