docs:
	hugo server -D

build:
	mkdocs build

deploy:
	mkdocs gh-deploy