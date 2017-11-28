FROM openjdk:9

RUN apt-get update; apt-get install -y locales python3.6

COPY locale.gen /etc/locale.gen
RUN locale-gen; \
	update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1; \
	update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

ENV LC_ALL=cs_CZ.UTF-8

COPY tasks/* /tasks/
RUN mkdir -p /data /run.d

COPY entrypoint.sh /
CMD ["/entrypoint.sh"]

# test it
# RUN ln -s /tasks/dump /run.d/01-dump; echo '{val:"test"}' > /data/arg0.json
