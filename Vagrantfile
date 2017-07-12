# vim: ft=ruby ts=2 sts=2 sw=2 et ai

Vagrant.configure(2) do |config|
  config.vm.synced_folder '.', '/vagrant', disabled: true

  { debian_jessie: 'debian/jessie64',
    debian_wheezy: 'debian/wheezy64',
    ubuntu_trusty: 'ubuntu/trusty64',
    ubuntu_xenial: 'ubuntu/xenial64',
  }.each do |vmname, box|
    config.vm.define vmname do |vm|
      vm.vm.box = box
      if vmname == :ubuntu_xenial
        vm.vm.provision 'shell', inline: <<-SHELL
          apt-get update
          apt-get install -y python
        SHELL
      end
    end
  end
end
