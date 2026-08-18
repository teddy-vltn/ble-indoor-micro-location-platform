FROM docker.elastic.co/logstash/logstash:8.12.2

# Switch to root to perform privileged operations
USER root

# Install the specific version of the logstash-output-mongodb plugin
# This version is the latests that works with mongodb 5.0
# It avoids the following error: ArgumentError: wrong number of arguments (given 2, expected 1)
# https://github.com/logstash-plugins/logstash-output-mongodb/issues/60
RUN logstash-plugin install --version 3.1.5 logstash-output-mongodb

# Install tzdata for timezone settings
# https://github.com/jruby/jruby/issues/3955 install netbase otherwise "Failed to load native protocols db"
RUN apt-get update && \
    apt-get install -y tzdata netbase && \
    apt-get clean

# Set the timezone to Europe/Paris
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Switch back to the logstash user
USER logstash

# Copy the Logstash configuration file
COPY logstash.conf /usr/share/logstash/pipeline/logstash.conf

# Optional: copy additional configurations if needed
# COPY logstash.yml /usr/share/logstash/config/logstash.yml

CMD ["logstash", "-f", "/usr/share/logstash/pipeline/logstash.conf"]
