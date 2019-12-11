[![pipeline status](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/pipeline.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

[![coverage report](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/coverage.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

# {{cookiecutter.project_slug}}

* dev domain : {{cookiecutter.dev_domain_name}}
* prod domain : {{cookiecutter.domain_name}}

## Branch convention

Please follow the conventions as defined here : https://x.vingtcinq.me/travailler-equipe-git/

## Init project

Requirements:
* a remote git repo (usually gitlab)

Run the following to init the project in GIT :

```
git init
git remote add origin https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}.git
git add --all
git push --set-upstream origin master
```

## Running tests :

```
coverage run manage.py test
```

## Deploying :

Deploy to dev or prod server using `one-cli` as explained here : https://x.vingtcinq.me/parametrer-et-utiliser-one-cli/

## Assets :

* Install assets with `yarn` : `cd assets && yarn install`
* Launch gulp : `gulp`

