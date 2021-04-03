FROM node:14
WORKDIR /usr/src/app
# Copy package*.json files before npm install
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 80
CMD ["npm", "start"]