FROM ubuntu:20.04

LABEL maintainer ChuenLam<chuenlam97@qq.com>
LABEL version=0.1

SHELL ["/bin/bash", "-c"]
ENV CHROME_DRIVER_PATH=/usr/bin/chromedriver
ENV WORKDIR=/workspace/SEU-health-reporting-helper
ENV TZ=Asia/Shanghai
WORKDIR ${WORKDIR}

RUN \
    # set timezone
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    # install tools
    apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    python3 \
    python3-pip
RUN \
    # install Chrome and ChromeDriver
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
	echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip -d /usr/bin chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    # clean
    rm -rf /var/cache/apt && \
    rm -rf /var/lib/apt/lists/* 

# copy files
COPY ["requirements.txt", "${WORKDIR}"]

RUN \
    # runtime related
    pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

CMD ["/bin/bash"]