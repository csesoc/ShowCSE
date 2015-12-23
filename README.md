# ShowCSE
## Developing

```
(you) $ vagrant up
(you) $ vagrant ssh
(vagrant@debian) $ cd /deploy/com.csesoc.showcse
(vagrant@debian) $ source .env
# Now you're in the venv
(vagrant@debian) $ python run.py server --host 0.0.0.0
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

##### Connecting UNSW LDAP
```
ssh you@cse.unsw.edu.au -L 1389:ad.unsw.edu.au:1389
```


## Deploying
Deploy using docker.


### Initial Creation
**Configure Environment Variables**

Create an env.sh file, which we will use when creating our docker containers to ensure the expected environment is passed to each container. Save this file as `env.sh`, unless you wish to modify subsequent commands that use it.

```
MYSQL_DATABASE=showcse
MYSQL_USER=showcse

# MySQL Password is required.
MYSQL_PASSWORD=

# Secret key used for signing cookies and CSRF tokens
SECRET_KEY=

# Ship exceptions to a sentry logging instance if provided (optional)
SENTRY_DSN=

# Determine what configuration setting should be used for the app
CONFIG_CLASS=Production
```

*Setup the MySQL Container*
```
docker create --name showcse.mysql -e MYSQL_RANDOM_ROOT_PASSWORD=true --env-file=env.sh mysql
```

*Run the MySQL Container*
```
docker start showcse.mysql
```

**Setup the App Container**

```
# You can replace the port binding with whatever you feel is good.
docker create --name showcse --env-file=env.sh --link showcse.mysql:mysql -p 0.0.0.0:8000:8000 nickw444/showcse
```

Before first run, we must provision the database
```
docker run -it --rm -env-file=env.sh --link showcse.mysql:mysql nickw444/showcse python3 run.py db upgrade
```

Start ShowCSE
```
docker start showcse
```

### Run at Startup with systemd
Copy or Clone this repo to acquire the service files. See folder `./systemd/` which contains systemd services.
```
# Enable the Services
systemctl enable systemd/showcse.mysql.service
systemctl enable systemd/showcse.service

# Start the service. 
systemctl start showcse
```

## Building the Docker Image
```
docker build --rm -t nickw444/showcse .
```

## Push Docker Image To Cloud

docker push nickw444/showcse



