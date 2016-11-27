clean:
	rm -rf venv;

install:
	virtualenv venv --no-site-packages; \
	venv/bin/pip install -r requirements.txt;

createdb:
	python -m spectacle.data_layer.database_setup
