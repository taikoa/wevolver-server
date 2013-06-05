#!/bin/bash
cd $WORKSPACE
venv=$(which virtualenv2 2> /dev/null || which virtualenv 2> /dev/null)
if [[ -z $venv ]]
then
    echo "No virtualenv found"
    exit 0
fi

$venv env
source ./env/bin/activate
pip install -r requirements.txt
pip install -r requirements-testing.txt

echo "env created ok"
echo ""
echo ""
echo "Run '. ./env/bin/activate' to activate your virtual environment"

source $WORKSPACE/env/bin/activate
cp $WORKSPACE/conf/custom_settings.py $WORKSPACE/wevolve/settings_test.py
cd $WORKSPACE

python manage.py jenkins
