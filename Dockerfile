FROM python:3.10

COPY ${PWD} /PCC-RENT
WORKDIR /PCC-RENT/
RUN pip install -r req.txt
RUN chmod +rx startup.sh
CMD ["./startup.sh"]
