# doco

build and mount your container with your current pwd mounted.
useful for developing in different environments.

heavily inspired by the now archived [`spotify/docker-interface`](https://github.com/spotify/docker_interface).


## usage

`doco` requires python 3.6+, docker and pyyaml.

create a `doco.yaml`. see provided one for an example.

run `doco` anywhere with a Dockerfile to build, mount the current working dir and give you a shell.

run `doco --dockerfile /path/to/custom/dockerfile` if you have your dockerfile elsewhere.

## mounted workspace

you should now be in a shell session within your countainer. any changes you make in the countainer's working directory will show up on the host, as it's mounted, not copied.
changes made on the host through and IDE will be immediately available to run in the container.



## example


```bash

$ doco
Building Docker image: example-env for linux/amd64 platform...
Build command: docker build --platform linux/amd64 -t example-env -f Dockerfile .
[+] Building 1.2s (7/7) FINISHED                                                                                                                              docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                                          0.0s
 => => transferring dockerfile: 497B                                                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/python:3.9-slim                                                                                                            1.0s
 => [internal] load .dockerignore                                                                                                                                             0.0s
 => => transferring context: 2B                                                                                                                                               0.0s
 => [1/3] FROM docker.io/library/python:3.9-slim@sha256:d1fd807555208707ec95b284afd10048d0737e84b5f2d6fdcbed2922b9284b56                                                      0.0s
 => => resolve docker.io/library/python:3.9-slim@sha256:d1fd807555208707ec95b284afd10048d0737e84b5f2d6fdcbed2922b9284b56                                                      0.0s
 => CACHED [2/3] RUN apt-get update && apt-get install -y     git     curl     build-essential     --no-install-recommends     && rm -rf /var/lib/apt/lists/*                 0.0s
 => CACHED [3/3] WORKDIR /app                                                                                                                                                 0.0s
 => exporting to image                                                                                                                                                        0.0s
 => => exporting layers                                                                                                                                                       0.0s
 => => exporting manifest sha256:c32b191398d34c0f425ccb69ba2f42b9bd9407ec08f9c8985730b8b66421b28c                                                                             0.0s
 => => exporting config sha256:ee4a6a6960ec36e042eb1337570ec0fc666f601797fe9fac39377acdacb81eea                                                                               0.0s
 => => exporting attestation manifest sha256:6570e79f93fea00b3abd6f28f81164e5a7bf6ab5dd0205d1c5e88338312c1825                                                                 0.0s
 => => exporting manifest list sha256:4c82f3b1ccc8e086d74eda322156865d12612f1ec840ca0315197f8faaf9c6b5                                                                        0.0s
 => => naming to docker.io/library/example-env:latest                                                                                                                         0.0s
Build successful!
Starting container with /Users/nk/playground/doco mounted at /app on linux/amd64 platform...


root@73d7cdbf6acc:/app# cat /etc/os-release > foobar
root@73d7cdbf6acc:/app# ^C


$ cat foobar
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
VERSION="12 (bookworm)"
VERSION_CODENAME=bookworm
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```
