FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# system level deps
RUN apt-get update && apt-get install -y curl libssl-dev unzip

# install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

WORKDIR /app

CMD ["/bin/bash"]
