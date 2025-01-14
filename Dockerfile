# FROM rocm/pytorch:latest
#
# RUN chown -R jenkins:jenkins /var/lib/jenkins
#
# ENV PATH="/var/lib/jenkins/.local/bin:$PATH"
# ENV PS1="\[\e[01;35m\]rocm/pytorch\[\e[01;34m\] \w \$\[\e[00m\] "

FROM rocm/dev-ubuntu-22.04:latest

ARG USER=docker-usr

RUN useradd -ms /bin/bash ${USER}

RUN usermod -aG sudo ${USER}
RUN echo "${USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

ENV PATH="${PATH}:/home/${USER}/.local/bin"
ENV MIOPEN_LOG_LEVEL=3

WORKDIR /home/${USER}/

RUN chown -R ${USER}:${USER} .

USER ${USER}

# COPY --chown=${USER} . ./

RUN echo 'export PS1="\[\e[01;35m\]tts-rocm\[\e[01;34m\] \w \$\[\e[00m\] "' >> /home/${USER}/.bashrc
