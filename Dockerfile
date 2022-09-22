FROM python:slim

RUN echo 'UTC' > /etc/localtime && apt update && apt install -y curl
RUN curl -s  https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash
RUN apt-get install speedtest
RUN mkdir /speedtest_wrapper
COPY README.md setup.py speedtest_wrapper.py /speedtest_wrapper/
RUN pip3 --no-cache-dir install /speedtest_wrapper
RUN apt remove -y curl
RUN apt autoremove -y

CMD ["speedtest-wrapper", "--debug"]
