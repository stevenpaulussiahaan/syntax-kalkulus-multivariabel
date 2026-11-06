# Image untuk hosting yang mendukung Docker (Render, Railway, Fly.io, VPS, dll.)
FROM php:8.3-apache
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-numpy python3-matplotlib \
 && rm -rf /var/lib/apt/lists/* \
 && a2enmod rewrite
COPY . /var/www/html/
RUN python3 /var/www/html/python/generate_figures.py \
 && chown -R www-data:www-data /var/www/html
EXPOSE 80
