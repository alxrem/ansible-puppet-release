#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sts=4 sw=4 et

import unittest
from subprocess import check_output
import re


class AnsibleTestCaseMixin:
    RESULT_RE = re.compile(
        r'(\w+)\s*:\s*'
        r'ok=(\d+)\s+changed=(\d+)\s+unreachable=(\d+)\s+failed=(\d+)',
        )

    def setUp(self):
        self.target_id = \
            check_output('docker run -d ansible-puppet-release-os:{}'
                         .format(self.__class__.IMAGE).split()).strip()

    def tearDown(self):
        check_output('docker rm -f {}'.format(self.target_id).split())

    def ansible_playbook(self, playbook):
        self._ansible_results = dict()
        stdout = \
            check_output('docker run --rm --link {}:target '
                         'ansible-puppet-release-ansible:{} {}.yml'
                         .format(self.target_id, self.__class__.VERSION,
                                 playbook).split())
        for results in AnsibleTestCaseMixin.RESULT_RE.findall(stdout):
            self._ansible_results[results[0]] = dict(zip(
                'ok changed unreachable failed'.split(),
                [int(counter) for counter in results[1:]]))

    def assertAnsibleResults(self, **kwargs):
        for host, results in self._ansible_results.items():
            for status, counter in results.items():
                if status not in kwargs:
                    continue
                expected = kwargs[status]
                self.assertEqual(
                    counter, expected,
                    'Expected {0} tasks were {1} on host {2}, '
                    'got {3}'.format(expected, status, host, counter))

    def test_install_package_on_clean_system(self):
        self.ansible_playbook('install')
        self.assertAnsibleResults(ok=3, changed=2, failed=0)
        self.ansible_playbook('check')
        self.assertAnsibleResults(ok=2, failed=0)

    def test_idempotency(self):
        self.ansible_playbook('install')
        self.ansible_playbook('install')
        self.assertAnsibleResults(ok=2, changed=0, failed=0)

    def test_reinstall_package(self):
        self.ansible_playbook('install')
        self.ansible_playbook('remove')
        self.ansible_playbook('install')
        self.assertAnsibleResults(ok=3, changed=2, failed=0)


for image in ('debian_jessie', 'debian_wheezy',
              'ubuntu_trusty', 'ubuntu_xenial'):
    for version in ('2.3.1', '2.2.3', '2.1.6'):
        class_name = "Test{}{}".format(image, version.replace('.', ''))
        globals()[class_name] = \
            type(class_name, (AnsibleTestCaseMixin, unittest.TestCase),
                 dict(IMAGE=image, VERSION=version))


if __name__ == '__main__':
    unittest.main()
