version = "0.1.2"
fullname = "artifact_py-$(version)"
zip_dir = "dist/$(fullname)/"


check: fix test
	# SHIP IT!

ship: check
	rm -rf pycheck/ dist/
	virtualenv --python=python3 pycheck
	pycheck/bin/pip install .
	py3/bin/python setup.py sdist
	# run: py3/bin/twine upload dist/*
	# also run `make zipit` and upload that

zipit:
	rm -rf $(zip_dir) "dist/$(fullname).zip"
	mkdir -p $(zip_dir)
	cp -r artifact_py/ $(zip_dir)
	mv $(zip_dir)/artifact_py/bin/artifact_py_local $(zip_dir)/artifact_py/bin/artifact_py
	for pkg in decorator.py six.py anchor_txt/ networkx/ yaml/ ; do \
      cp -r py3/lib/python*/site-packages/$$pkg $(zip_dir); \
    done
	cd dist && zip -r "$(fullname).zip" "$(fullname)"



init:
	# python2
	virtualenv --python=python2 py2
	py2/bin/pip install -r requirements.txt
	py2/bin/pip install pytest
	# python3
	virtualenv --python=python3 py3
	py3/bin/pip install -r requirements.txt
	py3/bin/pip install pytest yapf pylint twine

fix:
	py3/bin/yapf --in-place -r artifact_py tests
	py3/bin/python -m artifact_py export -i --format md

lint:
	py3/bin/pylint artifact_py

test2:
	# Testing python2
	PYTHONHASHSEED=42 py2/bin/py.test -vvv

test3:
	# Testing python3
	py3/bin/py.test -vvv

test: test3 test2

clean:
	rm -rf py2 py3 dist artifact_py.egg-info
