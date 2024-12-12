FROM nginx:latest

# Ставим envsubst
RUN apt-get update && apt-get install -y gettext-base && apt-get clean

# Ставим certbot 
RUN apt-get update && \
    apt-get install -y certbot python3-certbot-nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Потом объявим как том
RUN mkdir -p /certs


CMD ["sh", "-c", "certbot certonly --nginx -d $DOMEN -d www.$DOMEN --non-interactive --agree-tos --email minkin.d.d@gmail.com --cert-name $DOMEN --key-type ecdsa --config-dir /certs"]
