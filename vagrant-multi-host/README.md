## Vagrant Plugins

1. [vagrant-git](https://github.com/Learnosity/vagrant-git) for managing git repositories
2. [vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest) for automatically installing VirtualBox Guest Additions
3. [vagrant-hostmanager](https://github.com/devopsgroup-io/vagrant-hostmanager) for automatically managing the `/etc/hosts` file on guest machines - very useful in the multi-machine environment.

## [Vagrant Multi-Machine](https://www.vagrantup.com/docs/multi-machine/)  ##

### Creating ###

To create a multi-machie environment you provide multiple calls to `config.vm.define` in your vagrant file:

```ruby
Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "echo Hello"

  config.vm.define "web" do |web|
    web.vm.box = "apache"
  end

  config.vm.define "db" do |db|
    db.vm.box = "mysql"
  end
end
```

Or using loops:

```ruby

config.vm.box = "ubuntu/trusty64"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 4096
    vb.cpus = 4
  end
  
  (1..3).each do |i|
    config.vm.define "leviathan#{i}" do |node|
      node.vm.hostname = "leviathan#{i}"
      node.vm.network :forwarded_port, guest: 22, host: 2200+i, id: "ssh", auto_correct: true
      node.vm.network :private_network, ip: "192.169.0.10#{i}"
      provision_host node, i
    end
  end

```

### Private networks ###

* allows customized addressing
* easy way to wire VMs with the host

![alt](img/priv_nets.png)



### Customized provisioning

* parametrized provisiong scripts
* parametrized port mappings/addressing
* parametrized host naming

```ruby

$http_server = <<SCRIPT
mkdir /home/vagrant/www && cd /home/vagrant/www
echo $1 > index.html
python -m SimpleHTTPServer
SCRIPT

def provision_host(node, host_id)
  node.vm.provision "http_server",
                    type: "shell",
                    inline: $http_server,
                    args: "Hello from #{host_id}!"
end

Vagrant.configure(2) do |config|
    
  (1..3).each do |i|
    config.vm.define "td-host#{i}" do |node|
      node.vm.hostname = "td-host#{i}"
      node.vm.network :forwarded_port, guest: 8080, host: 8080+i, auto_correct: true
      node.vm.network :private_network, ip: "192.169.0.10#{i}"
      provision_host node, i
    end
  end
  
end
```

### Example

Run `vagrant up`. You will get three VMs with HTTP server running on each of them. Their 80 ports are redirected to 8081, 8082 and 8083 respectively:

![alt](img/example.png)
