FROM library/debian:testing

#
# install additional packages
#
RUN perl -i -pe 's/ main/ main non-free contrib/' /etc/apt/sources.list && apt-get update && \
	apt-get install -y locales python3.6 vim libxml2-utils python3-pip xvfb openjfx openjdk-8-jdk x11-apps netpbm && \
	localedef -i cs_CZ -c -f UTF-8 -A /usr/share/locale/locale.alias cs_CZ.UTF-8
ENV LANG cs_CZ.utf8

#
# Tasks
#
ADD http://downloads.sourceforge.net/project/checkstyle/checkstyle/8.5/checkstyle-8.5-all.jar /lib/checkstyle-8.5-all.jar
#COPY checkstyle-8.5-all.jar /lib/checkstyle-8.5-all.jar
COPY style.xml /lib/style.xml
COPY tasks/* /tasks/

#
# Final tuning
#
RUN mkdir -p /data /test.d

COPY entrypoint.sh /
CMD ["/entrypoint.sh"]

# test 1
COPY cp HelloWorld.java /data/unpack/
RUN ln -s /tasks/compile /test.d/01-compile; \
	ln -s /tasks/runit_gui /test.d/03-runit

# test - compile, checkstyle
#COPY arg0.json /data/
#RUN ln -s /tasks/unpack /test.d/00-unpack_arg0; \
#	ln -s /tasks/compile /test.d/01-compile; \
#	ln -s /tasks/runit /test.d/03-runit
