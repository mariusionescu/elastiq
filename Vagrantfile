# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provider "virtualbox" do |v|
    v.memory = 512
  end
  config.vm.box = "trusty64"
  config.vm.network "private_network", ip: "192.168.100.12"
  config.vm.synced_folder ".", "/opt/elastiq"
  config.vm.hostname = "elastiq-dev"
end

