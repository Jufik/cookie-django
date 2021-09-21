[![pipeline status](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/pipeline.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

[![coverage report](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/coverage.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

# {{cookiecutter.project_slug}}

-   dev domain : {{cookiecutter.dev_domain_name}}
-   prod domain : {{cookiecutter.domain_name}}

## Branch convention

GitFlow
https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

## Init project

Requirements:

-   a remote git repo (usually gitlab)

Run the following to init the project in GIT :

```
git init
git remote add origin https://gitlab.com/mefa/{{cookiecutter.project_slug}}.git
git add --all
git push --set-upstream origin master
```

## Running tests :

```
coverage run manage.py test
```

## Assets :

-   Install assets with `yarn` : `cd assets && yarn install`
-   Launch gulp : `gulp`
