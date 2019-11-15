
wheel: clean
	python setup.py bdist_wheel
clean:
	rm -rf dist build
deploy: wheel
	scp picklr.ini nginx-snippet.conf dist/picklr-0.0.1-py3-none-any.whl robertkarl.space:~/picklr/
run_devel:
	FLASK_ENV=development FLASK_APP=picklr.picklr flask run
run_wsgi:
	uwsgi --ini picklr.ini
docker_image:
	docker build -t robertkarl/picklr:latest .
run_docker:
	docker run --publish-all --expose 5000 picklr:latest
.PHONY: wheel clean docker_image
