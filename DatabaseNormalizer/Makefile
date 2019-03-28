SOURCE_FOLDER=db_normalizer
TESTS_FOLDER=tests

install:
        apt install python-pip
        pip3 install -r requirements.txt

run:
        python3 $(SOURCE_FOLDER)/database_normalizer.py

test:
        python3 -m unittest $(TESTS_FOLDER)/csv_utils/normalizer.py
