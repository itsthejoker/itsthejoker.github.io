docs:
	hugo server -D --disableFastRender

build:
	mkdocs build

deploy:
	mkdocs gh-deploy