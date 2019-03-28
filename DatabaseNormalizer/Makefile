SOURCE_FOLDER=db_normalizer
TESTS_FOLDER=tests

install:
	apt install python3-pip
	pip3 install -r requirements.txt

run:
	python3 $(SOURCE_FOLDER)/database_normalizer.py

tests: clean
	python3 -m unittest $(TESTS_FOLDER)/csv_utils/normalizer.py
	python3 -m unittest $(TESTS_FOLDER)/csv_utils/reader.py

clean:
	find . -name '*.pyc' -exec rm -fv {} +
	find . -name '*.pyo' -exec rm -fv {} +
	find . -name '__pycache__' -exec rm -frv {} +
