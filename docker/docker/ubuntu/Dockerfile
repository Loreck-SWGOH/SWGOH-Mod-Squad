FROM ubuntu:latest
ARG USER
ARG GROUP
ARG PASSWD

RUN addgroup --gid 1000 ${GROUP}
RUN adduser --home /home/${USER} --shell /bin/bash --uid 1000 --gid 1000 --disabled-password ${USER}
RUN echo "${USER}:${PASSWD}" | chpasswd

RUN apt-get update
RUN apt-get -y install sudo
# RUN adduser ${USER} sudo
# RUN echo "${USER} ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee "/etc/sudoers.d/dont-prompt-$USER-for-sudo-password"

COPY dotfiles/* /home/${USER}/
RUN chown -R ${USER}:${GROUP} /home/${USER}

COPY install.sh /opt/install.sh
RUN /bin/bash -c /opt/install.sh
COPY install-as-user.sh /opt/install-as-user.sh
RUN sudo -u ${USER} /bin/bash -c /opt/install-as-user.sh

USER ${USER}

WORKDIR /home/${USER}
