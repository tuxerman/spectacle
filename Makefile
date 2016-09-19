clean:
	rm -rf venv;

install:
	virtualenv venv; \
	venv/bin/pip install -r requirements.txt;