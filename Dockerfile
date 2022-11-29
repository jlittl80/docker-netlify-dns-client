FROM python:3

RUN mkdir /logs ;\
    touch /logs/netlifydns.log
VOLUME /logs

RUN mkdir /app

WORKDIR /app
COPY netlify-dns.py /app/netlify-dns.py
CMD ["python3", "netlify-dns.py"]
