puppet-release
==============

Role installs release package from Puppetlabs repository.

No parameters, no dependencies.

Intended to use as dependency of other roles related to puppet.

Supported platforms are

- Debian wheezy
- Debian jessie
- Ubuntu trusty (14.04 LTS)
- Ubuntu xenial (16.04 LTS)

Example playbook
----------------

```yaml
---
- hosts: puppet.example.org
  roles:
  - alxrem.puppet-release
```

License
-------

Apache-2.0
