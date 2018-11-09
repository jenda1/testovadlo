FROM library/debian:testing

#
# install additional packages
#
RUN perl -i -pe 's/ main/ main non-free contrib/' /etc/apt/sources.list && \
	apt-get update && \
	apt-get install -y locales python3.7 vim libxml2-utils python3-pip xvfb openjdk-8-jdk x11-apps netpbm curl && \
	localedef -i cs_CZ -c -f UTF-8 -A /usr/share/locale/locale.alias cs_CZ.UTF-8

ENV LANG cs_CZ.utf8

RUN pip3 install aiostream ipdb

COPY entrypoint /
COPY wiki_inputs/*.py /usr/lib/python3/dist-packages/wiki_inputs
COPY wi /usr/bin/

#
# Final tuning
#
ENTRYPOINT ["/entrypoint"]
