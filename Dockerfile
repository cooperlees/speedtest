FROM ubuntu:bionic

RUN echo 'UTC' > /etc/localtime && apt update && apt install -y gnupg1 apt-transport-https dirmngr lsb-core
ENV INSTALL_KEY=379CE192D401AB61
RUN export DEB_DISTRO=$(lsb_release -sc) ; apt-key adv --keyserver keyserver.ubuntu.com --recv-keys $INSTALL_KEY
RUN export DEB_DISTRO=$(lsb_release -sc) ; echo "deb https://ookla.bintray.com/debian ${DEB_DISTRO} main" > /etc/apt/sources.list.d/speedtest.list && apt update && apt install -y speedtest
RUN mkdir /speedtest_wrapper

CMD ["speedtest"]
