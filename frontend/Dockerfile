FROM node:17-alpine
RUN apk add --no-cache libc6-compat
WORKDIR /src

COPY package.json package-lock.json ./
RUN npm install

COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]