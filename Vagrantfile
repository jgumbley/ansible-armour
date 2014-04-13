# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'
Vagrant.require_version ">= 1.5.0"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = 'precise64'
    config.vm.box_url = 'http://files.vagrantup.com/precise64.box'
    config.ssh.forward_agent = true

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "environment.yml"
    end
 
    config.vm.define "blackhat" do |frontend|
        config.vm.network "private_network", ip: "10.0.0.10"
    end
  
    config.vm.define "fortress" do |management|
        config.vm.network "private_network", ip: "10.0.0.11"
    end

end
