all: default

default: checkdeps updatedeps lint

checkdeps:
	./utils/check_dependencies.sh

updatedeps:
	git submodule init
	git submodule update

lint:
	# TODO: Add Pylint

serve:
	dev_appserver.py .

deploy:
	appcfg.py -v update .
