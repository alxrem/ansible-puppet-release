FROM %%IMAGE%%

RUN apt-get update
RUN apt-get -y --no-install-recommends install openssh-server python python-apt
RUN echo root:root | chpasswd

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-o", "UsePrivilegeSeparation=no", "-o", "PermitRootLogin=yes"]
