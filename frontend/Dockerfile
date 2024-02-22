FROM node:20-bookworm-slim as build-step

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY frontend/package.json  ./

RUN npm install

COPY ./frontend/ ./

RUN npm run build


# for production
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --only=production

COPY --from=builder /app/dist ./

EXPOSE 3000

ENTRYPOINT ["node","./app.js"]
