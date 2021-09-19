FROM python:3

VOLUME /logs

RUN mkdir /app ;\
    touch /logs/netlifydns.log

WORKDIR /app
COPY netlify-dns.py /app/netlify-dns.py
CMD ["python3", "netlify-dns.py"]
