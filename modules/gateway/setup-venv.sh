source usquad-venv/bin/activate
python src/main/python/setup.py install 
export PYTHONPATH=`pwd`/src/main/python:`pwd`/src/test/python:$PYTHONPATH

