all: default

default: checkdeps updatedeps lint

checkdeps:
	./utils/check_dependencies.sh

updatedeps:
	git submodule init
	git submodule update
	pip install -r requirements.txt

lint:
	@PYTHONPATH=`./utils/get_gae_pythonpath.sh` \
	pylint -r n -d C0301,C0111,E1101,W0232,R0903 ./*.py

serve:
	dev_appserver.py .

deploy:
	appcfg.py -v update .
