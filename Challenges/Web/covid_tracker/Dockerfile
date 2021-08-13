FROM node:13
WORKDIR /app
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install
COPY . .
EXPOSE 3000
ENV FLAG "greyhats{w3bApp5_n33d_v@cc1ne?_4521f}"
ENV SECRET "adsfaciruhretnsjdcHASAFAD"
ENV ADMIN_PASSWORD "asdafasdvyasiuv7243n3kj"
CMD npm run serve