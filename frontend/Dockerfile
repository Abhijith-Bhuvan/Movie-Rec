FROM node:16-alpine
 
# Copy the .env file into the container
COPY .env /frontend/.env

# Set the NODE_ENV environment variable
ENV NODE_ENV=production

ADD . /frontend
WORKDIR /frontend
RUN npm install --silent
 
CMD ["npm", "start"]