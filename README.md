# doco

build and mount your container with your current pwd mounted.
useful for developing in different environments.

heavily inspired by the now archived `spotify/docker-interface`.


## usage

`doco` requires python 3.6+, docker and pyyaml.

create a `doco.yaml`. see provided one for an example.

run `doco` anywhere with a Dockerfile to build, mount the current working dir and give you a shell.

run `doco --dockerfile /path/to/custom/dockerfile` if you have your dockerfile elsewhere.

## mounted workspace

you should now be in a shell session within your countainer. any changes you make in the countainer will show up on the host, as it's mounted, not copied.



