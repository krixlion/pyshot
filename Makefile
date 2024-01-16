init:
	python -m venv .venv
	.\.venv\Scripts\activate

save-reqs:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt
