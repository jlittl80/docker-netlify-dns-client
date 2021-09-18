FROM python:3

RUN mkdir /app

# expose volume
VOLUME /data

run touch /data/env

WORKDIR /app
COPY netlify-dns.py /app/netlify-dns.py
CMD ["netlify-dns.py"]
ENTRYPOINT ["python3"]
