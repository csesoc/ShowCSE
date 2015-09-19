# ShowCSE


## Developing

```
(you) $ vagrant up
(you) $ vagrant ssh
(vagrant@debian) $ cd /deploy/com.csesoc.showcse
(vagrant@debian) $ source .env
# Now you're in the venv
(vagrant@debian) $ python run.py --host 0.0.0.0
```

##### Upgrading the virtual environment with new requirements
```
(vagrant@debian) $ source .env
(vagrant@debian) $ upgrade
```

##### Re-Provision the VM
```
(you) $ vagrant destroy 
(you) $ vagrant up
```