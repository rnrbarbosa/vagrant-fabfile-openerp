# For development, it is not needed when run on the production environment.
Vagrant.require_plugin "vagrant-fabric"

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise32"
  config.vm.network :forwarded_port, guest: 80, host: 88
  config.vm.network :forwarded_port, guest: 8069, host: 8069
  config.vm.network :private_network, ip: "192.168.77.11"
  config.vm.hostname = "openerp"
end

Vagrant.configure("2") do |config|
  # Enable provisioning with fabric script, specifiying jobs you want execute,
  # and the path of fabfile.
  config.vm.provision :fabric do |fabric|
    fabric.fabfile_path = "./fabfile.py"
    fabric.tasks = ["deploy", ]
  end
end


