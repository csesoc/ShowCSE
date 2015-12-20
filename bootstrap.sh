# Fix SSH Locale
localedef -i en_US -f UTF-8 en_AU.UTF-8
export DEBIAN_FRONTEND=noninteractive # Don't run interactive stuff
MYSQL_ROOT_PW="RlzUsa7HnGBqHrmZbwNDqbkXYeCPKx"
# This project is DevScale!

apt-get update
apt-get install -y python2.7 python3.4 python3-dev python-dev python-setuptools python3-setuptools libffi-dev
apt-get install -y mongodb redis-server
apt-get install -y git curl
apt-get install -y mysql-server

# Tell the bootstrap where the project is mounted
PROJECT_ROOT="/deploy/com.csesoc.showcse/"
PYTHON_BINARY="python3.4"

# Install VirtualEnv
easy_install pip
easy_install3 pip
pip install virtualenv

# Secure & setup the MySQL Installation
mysql -e "CREATE USER 'webskale'@'localhost'; CREATE DATABASE webskale; GRANT ALL PRIVILEGES ON webskale . * TO 'webskale'@'localhost'";
mysql -e "UPDATE mysql.user SET Password = PASSWORD('$MYSQL_ROOT_PW') WHERE User = 'root'"
mysql -e "FLUSH PRIVILEGES"



# Install Node/NPM
curl --silent --location https://deb.nodesource.com/setup_0.12 | bash -
apt-get install --yes nodejs
npm install -g grunt-cli # Get grunt too
npm install -g bower

# Make a VirtualEnv for the project.
cd $PROJECT_ROOT;

if [ -e ".venv" ]; then
    rm -rf ".venv"; #Delete venv if it exists;
fi

if [ -e "node_modules" ]; then
    rm -rf "node_modules";
fi

virtualenv -p $PYTHON_BINARY ".venv"
source ".venv/bin/activate"
    # Inside Venv Context
    # Install project requirements
    pip install -r requirements.txt
    # Install node requirements
    npm install
    grunt bower_global

deactivate

