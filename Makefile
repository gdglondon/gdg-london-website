all: default

default: checkdeps updatedeps lint

checkdeps:
	./utils/check_dependencies.sh

updatedeps:
	# --upgrade is buggy with --target, see https://github.com/pypa/pip/pull/2537
	rm -rf lib/
	pip install --target=lib/ -r requirements.txt

lint:
	@PYTHONPATH=`./utils/get_gae_pythonpath.sh` \
	pylint -r n -d C0301,C0111,E1101,W0232,R0903 ./*.py

serve:
	dev_appserver.py .

deploy:
	appcfg.py --version `git rev-parse --short HEAD` -v update .
	appcfg.py set_default_version --version `git rev-parse --short HEAD` .
