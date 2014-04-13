define green
	@tput setaf 2
	@tput bold
	@echo $1
	@tput sgr0
endef

in_venv=venv/bin/activate

ansible-playbook=ansible-playbook -i \
	.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory \
   	--private-key=~/.vagrant.d/insecure_private_key -u vagrant

.PHONY: default¬
default: box
	$(call green,"[All steps successful]")

.PHONY: ssh
ssh: venv
	. $(in_venv); vagrant ssh
	$(call green,"[Back in local machine]")

.PHONY: box
box: venv
	. $(in_venv); vagrant up
	$(call green,"[Using Vagrant to bring up local dev VM success]")

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -r requirements.txt
	touch venv/bin/activate
	$(call green,"[Making venv successful]")

.PHONY: provision
provision: venv
	source ./venv/bin/activate; vagrant provision
	$(call green,"[Making venv successful]")

.PHONY: tests
tests: venv box
	. $(in_venv); $(ansible-playbook) tests_environment.yml
	cat xunit_out.xml
	$(call green,"[Tests run]")

.PHONY: mrsparkle
mrsparkle: clean
	rm -Rf venv
	$(call green,"[Cleaned up everything]")

clean:
	vagrant halt
	vagrant destroy -f
	$(call green,"[Cleaned up]")
