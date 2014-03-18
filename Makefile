test:
	coverage run tests.py

verify:
	pyflakes app
	pep8 app

clean:
	find . -name *.pyc -delete

run:
	./run.py

setup:
	virtualenv --distribute venv

install:
	pip install -r requirements.txt

#hello