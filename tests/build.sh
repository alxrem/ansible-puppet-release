#!/bin/sh

PRODUCT=ansible-puppet-release

for IMAGE in debian:wheezy debian:jessie ubuntu:trusty ubuntu:xenial; do
	DOCKERFILE=`mktemp -p .`
	sed -e "s/%%IMAGE%%/${IMAGE}/g" tests/docker/os.dockerfile > $DOCKERFILE
	TAG=`echo $IMAGE | tr : _`
	docker build -t ${PRODUCT}-os:${TAG} -f $DOCKERFILE .
	rm -f $DOCKERFILE
done

for VERSION in 2.1.6 2.2.3 2.3.1; do
	docker build -t ${PRODUCT}-ansible:${VERSION} --build-arg version=${VERSION} -f tests/docker/ansible.dockerfile .
done
