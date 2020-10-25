# https://gist.github.com/cobyism/4730490#gistcomment-2375522

.PHONY: all deploy clean build

all: build dist

dist:
	git worktree add build gh-pages

# Replace this rule with whatever builds your project
build:
	python build.py

deploy: all
	cd build && \
	git add --all && \
	git commit -m "Deploy to gh-pages" && \
	git push origin gh-pages

# Removing the actual dist directory confuses git and will require a git worktree prune to fix
clean:
	rm -rf build/*
