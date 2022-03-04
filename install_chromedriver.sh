CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
wget -q "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
unzip -d /usr/bin chromedriver_linux64.zip && \
rm chromedriver_linux64.zip