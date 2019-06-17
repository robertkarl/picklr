
wheel: clean
	python setup.py bdist_wheel
clean:
	rm -rf dist build
deploy: wheel
	scp dist/picklr-0.0.1-py3-none-any.whl robertkarl.space:~/picklr/
run_devel:
	FLASK_ENV=development FLASK_APP=picklr.picklr flask run
run_wsgi:
	uwsgi --ini picklr.ini
.PHONY: wheel clean
