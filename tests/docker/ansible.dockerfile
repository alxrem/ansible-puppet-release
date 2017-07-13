FROM python:2
ARG version
RUN apt-get -qq update && apt-get -y --no-install-recommends install sshpass
COPY handlers /etc/ansible/roles/alxrem.puppet-release/handlers
COPY tasks/ /etc/ansible/roles/alxrem.puppet-release/tasks/
COPY vars/ /etc/ansible/roles/alxrem.puppet-release/vars/
COPY meta/ /etc/ansible/roles/alxrem.puppet-release/meta/
COPY tests/ansible/ /etc/ansible/
COPY tests/playbooks/ /
ENTRYPOINT ["/usr/local/bin/ansible-playbook"]
RUN pip install ansible==$version
