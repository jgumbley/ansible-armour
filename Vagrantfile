# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'
Vagrant.require_version ">= 1.5.0"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
    config.vm.box = 'trusty64'
    config.vm.box_url = 'https://vagrantcloud.com/ubuntu/boxes/trusty64/versions/1/providers/virtualbox.box'
    config.ssh.forward_agent = true

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "environment.yml"
    end
 
    config.vm.define "blackhat" do | blackhat |
        blackhat.vm.network "private_network", ip: "10.0.0.10", 
            virtualbox__intnet: true
    end
  
    config.vm.define "fortress" do | fortress |
        fortress.vm.network "private_network", ip: "10.0.0.11", 
            virtualbox__intnet: true
    end

end
