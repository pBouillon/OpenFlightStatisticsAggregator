SOURCE_FOLDER=db_normalizer
TESTS_FOLDER=tests

install:
	apt install -y python3-pip
	pip install cx_Oracle --upgrade
	pip3 install -r requirements.txt

test: clean
	python3 -m unittest discover --start-directory $(TESTS_FOLDER)

clean:
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '*.pyo' -exec rm -fv {} +
	find . -name '__pycache__' -exec rm -frv {} +
