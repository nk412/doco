# doco

Isolated development environments with Docker.

### What?

Run docker container with your current working directory mounted. Just a python wrapper around a YAML config and some docker commands. Inspired by the now archived [docker_interface](https://github.com/spotify/docker_interface).


### Why?
Emulate different setups, dependencies and environment configuration within Docker containers and not your local system. The mounted filesystem means you can make changes on your favorite IDE and have the immediately available to run in your container.

### How?

NOTE: `doco` requires python 3.6+, docker and pyyaml.

1. Create a `doco.yaml`. see provided one for an example.
2. Run `doco` anywhere with a Dockerfile to build, mount the current working dir and give you a shell. Or run `doco --dockerfile /path/to/custom/dockerfile` if you have your dockerfile elsewhere.

You should now be in a shell session within your container. Any changes you make in the container's working directory will show up on the host, as it's mounted, not copied. Changes made on the host through an IDE will be immediately available to run.

### Environments

Use a `.env` containing key-value pairs that are available at runtime.

## Example

### TASK: Use the AWS CLI to list buckets on Ubuntu 22


### 1. Set up a simple Dockerfile to have AWS CLI setup on Ubuntu 22.04.

```Dockerfile
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
```

### 2. Create a `doco.yaml`

```yaml
image_name: aws-example

mount_path: /example/aws
platform: linux/amd64
shell: bash

docker_options:
  - "--env-file=.env"
  # - "-p=8080:8080"  # Uncomment to add port mapping
  # - "--network=host"  # Uncomment to use host network

```

### 3. Create a `.env` file with AWS credentials

```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

### 4. Run doco

```bash
$ doco
╰──╴$ doco
Building Docker image: aws-example for linux/amd64 platform...
Build command: docker build --platform linux/amd64 -t aws-example -f Dockerfile .
[+] Building 1.2s (10/10) FINISHED                                                                                   
 => [internal] load build definition from Dockerfile                                                                 
 => => transferring dockerfile: 392B                                                                                 
 => [internal] load metadata for docker.io/library/ubuntu:22.04                                                      
 => [internal] load .dockerignore                                                                                    
 => => transferring context: 2B                                                                                      
 => [1/6] FROM docker.io/library/ubuntu:22.04@sha256:ed1544e454989078f5dec1bfdabd8c5cc9c48e0705d07b678ab6ae3fb61952d2
 => => resolve docker.io/library/ubuntu:22.04@sha256:ed1544e454989078f5dec1bfdabd8c5cc9c48e0705d07b678ab6ae3fb61952d2
 => CACHED [2/6] RUN apt-get update && apt-get install -y curl libssl-dev unzip                                      
 => CACHED [3/6] RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"               
 => CACHED [4/6] RUN unzip awscliv2.zip                                                                              
 => CACHED [5/6] RUN ./aws/install                                                                                   
 => CACHED [6/6] WORKDIR /app                                                                                        
 => exporting to image                                                                                               
 => => exporting layers                                                                                              
 => => exporting manifest sha256:c6066ac701addf8f5d400d52ae8f494c56aef4b6288124615258728360b11f6d                    
 => => exporting config sha256:baafdf802d9d98d45741a769e7f5950650358e604a66d4a64a051e084a220ab1                      
 => => exporting attestation manifest sha256:25ca69fad806042c026c31c6f040d57f06ef393627ffd3623937da11e398de96        
 => => exporting manifest list sha256:d6c6632abe08d4952f1dcc9424dc33e36efcb83c416897bf922a415af27cfac3               
 => => naming to docker.io/library/aws-example:latest                                                                
Build successful!
Starting container with /Users/nk/playground/doco mounted at /example/aws on linux/amd64 platform...
```

```
root@c5c4e2155aa9:/example/aws# aws s3 ls
... bucket listing ...

```


## Other scenarios


### ● Using your local SSH key during build

Make your SSH key available during build to pull private repos, for instance

Update doco.yaml to include your SSH keyfile

```
ssh_key_path: ~/.ssh/id_ed25519
```

Update Dockerfile to use the secret mount for the provided SSH key
```
RUN --mount=type=secret,id=ssh_key,target=/tmp/ssh_key \
    cp /tmp/ssh_key /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa && \
    eval "$(ssh-agent -s)" && \
    ssh-add /root/.ssh/id_rsa && \
    pip install git+ssh://git@github.com/super-private-user/super-private-repo.git
```

### ● Using your local SSH key during runtime

Use secret mount like above to create a /home/root/.ssh/ dir

TODO: example


### ● GCP service account

Have a service account keyfile on your working directory, and an entry in .env that sets `GOOGLE_APPLICATION_CREDENTIALS`.

TODO: example


### ● Talking to services on host

Enable `--network=host` in doco.yaml, and access any services like MySQL through host `docker.host.internal`.

TODO: example

### ● Exposing ports on the container

Enable port forwarding in doco.yaml.

TODO: example

