#!/bin/sh

echo "testing with $(python2 -V 2>&1)"
python2 $(which nosetests) --rednose -v --with-coverage --cover-erase tests/

if [ $? == 0 ]; then
	echo

	echo "testing with $(python3 -V 2>&1)"
	python3 $(which nosetests-3) --rednose -v --with-coverage --cover-erase tests/
fi
