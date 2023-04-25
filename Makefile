serve:
	hugo server -D --disableFastRender

build:
	mkdocs build

deploy:
	mkdocs gh-deploy

new:
	@read -p "What's the lower-case kebab-case name of the new post? " POST_NAME; \
	echo $$POST_NAME; \
	hugo new "posts/$$POST_NAME.md"
