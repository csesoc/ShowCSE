# This project is DevScale!

apt-get update
apt-get install -y python2.7 python3.4 python3-dev python-dev python-setuptools python3-setuptools
apt-get install -y mongodb redis-server

# Tell the bootstrap where the project is mounted
PROJECT_ROOT="/deploy/com.csesoc.showcse/"
PYTHON_BINARY="python3.4"

# Install VirtualEnv
easy_install pip
easy_install3 pip
pip install virtualenv

# Make a VirtualEnv for the project.
cd $PROJECT_ROOT;

if [ -e ".venv" ]; then
    rm -rf ".venv"; #Delete venv if it exists;
fi

virtualenv -p $PYTHON_BINARY ".venv"
source ".venv/bin/activate"
    # Inside Venv Context
    # Install project requirements
    pip install -r requirements.txt
deactivate
