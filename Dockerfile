FROM openjdk:9

RUN apt-get update; apt-get install -y locales
COPY locale.gen /etc/locale.gen
RUN locale-gen
ENV LC_ALL=cs_CZ.UTF-8

COPY entrypoint.sh /
RUN mkdir -p /data /output

CMD ["/entrypoint.sh"]
