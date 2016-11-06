clean:
	rm -rf venv;

install:
	virtualenv venv; \
	venv/bin/pip install -r requirements.txt;

createdb:
	python -m spectacle.data_layer.database_setup