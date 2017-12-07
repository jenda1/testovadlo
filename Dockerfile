FROM openjdk:9

#
# install additional packages
#
RUN apt-get update; apt-get dist-upgrade -y; apt-get install -y locales python3.6 vim libxml2-utils

#
# setup locale (FIXME: all locales?)
#
COPY locale.gen /etc/locale.gen
RUN locale-gen; \
	update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1; \
	update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2
ENV LC_ALL=cs_CZ.UTF-8

#
# Tasks
#
COPY tasks/* /tasks/

ADD http://downloads.sourceforge.net/project/checkstyle/checkstyle/8.5/checkstyle-8.5-all.jar /lib/checkstyle-8.5-all.jar
#COPY checkstyle-8.5-all.jar /lib/checkstyle-8.5-all.jar
COPY style.xml /lib/style.xml

#
# Final tuning
#
RUN mkdir -p /data /test.d

COPY entrypoint.sh /
CMD ["/entrypoint.sh"]

# test 1
# RUN ln -s /tasks/dump.sh /run.d/01-dump.sh; echo '{val:"test"}' > /data/arg0.json

# test - compile, checkstyle
#COPY arg0.json /data/
#RUN ln -s /tasks/unpack /test.d/00-unpack_arg0; \
#	ln -s /tasks/compile /test.d/01-compile; \
#	ln -s /tasks/runit /test.d/03-runit
