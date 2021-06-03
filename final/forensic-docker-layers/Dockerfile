FROM python
COPY container-files/* /
RUN python /decrypt.py enc.txt password.txt
RUN rm /password.txt