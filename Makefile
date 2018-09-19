env: requirements.txt
	virtualenv --python python3.7 env
	env/bin/pip install -r requirements.txt

dev-env: env
	env/bin/pip install -r dev-requirements.txt -r test-requirements.txt
