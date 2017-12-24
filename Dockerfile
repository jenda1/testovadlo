FROM openjdk:9

#
# install additional packages
#
RUN apt-get update; apt-get dist-upgrade -y; \
	apt-get install -y \
		locales python3.6 vim libxml2-utils \
		texlive-luatex texlive-latex-base texlive-latex-recommended texlive-latex-extra

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

COPY jr* /data/
RUN ln -s /tasks/unpack /test.d/00-unpack_arg0; \
	ln -s /tasks/unpack /test.d/00-unpack_arg1; \
	ln -s /tasks/unpack /test.d/00-unpack_arg2; \
	ln -s /tasks/unpack /test.d/00-unpack_arg3; \
	ln -s /tasks/unpack /test.d/00-unpack_arg4; \
	ln -s /tasks/unpack /test.d/00-unpack_arg5; \
	ln -s /tasks/unpack /test.d/00-unpack_arg6; \
	ln -s /tasks/unpack /test.d/00-unpack_arg7; \
	ln -s /tasks/unpack /test.d/00-unpack_arg8; \
	ln -s /tasks/unpack /test.d/00-unpack_arg9; \
	ln -s /tasks/unpack /test.d/00-unpack_arg10; \
	ln -s /tasks/unpack /test.d/00-unpack_arg11; \
	ln -s /tasks/unpack /test.d/00-unpack_arg12; \
	ln -s /tasks/unpack /test.d/00-unpack_arg13; \
	ln -s /tasks/unpack /test.d/00-unpack_arg14; \
	ln -s /tasks/unpack /test.d/00-unpack_arg15; \
	ln -s /tasks/unpack /test.d/00-unpack_arg16; \
	ln -s /tasks/unpack /test.d/00-unpack_arg17; \
	ln -s /tasks/unpack /test.d/00-unpack_arg18; \
	ln -s /tasks/unpack /test.d/00-unpack_arg19; \
	ln -s /tasks/unpack /test.d/00-unpack_arg20; \
	ln -s /tasks/unpack /test.d/00-unpack_arg21; \
	ln -s /tasks/unpack /test.d/00-unpack_arg22; \
	ln -s /tasks/unpack /test.d/00-unpack_arg23; \
	ln -s /tasks/unpack /test.d/00-unpack_arg24; \
	ln -s /tasks/unpack /test.d/00-unpack_arg25; \
	ln -s /tasks/latex /test.d/10-latex_jr

# test 1
# RUN ln -s /tasks/dump.sh /run.d/01-dump.sh; echo '{val:"test"}' > /data/arg0.json

# test - compile, checkstyle
#COPY arg0.json /data/
#RUN ln -s /tasks/unpack /test.d/00-unpack_arg0; \
#	ln -s /tasks/compile /test.d/01-compile; \
#	ln -s /tasks/runit /test.d/03-runit
