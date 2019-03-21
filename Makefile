PY_FILES = $(shell find ./ -name "*.py")
TEST_FILES = $(shell find ./tests -name "*.py")

pep8:
	autopep8 --in-place $(PY_FILES)

test: pep8
	pytest $(TEST_FILES)
	pycodestyle $(PY_FILES)

install: pep8
	pip3 install --user --force-reinstall .

uninstall:
	pip3 uninstall -y graphtool
