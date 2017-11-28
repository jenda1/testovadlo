FROM openjdk:9

RUN apt-get update; apt-get install -y locales
COPY locale.gen /etc/locale.gen
RUN locale-gen
ENV LC_ALL=cs_CZ.UTF-8

COPY tasks/* /tasks/
RUN mkdir -p /data /run.d

COPY entrypoint.sh /
CMD ["/entrypoint.sh"]

# test it
# RUN ln -s /tasks/dump /run.d/01-dump; echo '{val:"test"}' > /data/arg0.json
