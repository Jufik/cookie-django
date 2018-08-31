[![pipeline status](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/pipeline.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

[![coverage report](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/coverage.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

# {{cookiecutter.project_slug}}

* dev domain : {{cookiecutter.dev_domain_name}}
* prod domain : {{cookiecutter.domain_name}}

## Running tests :

The `.env.test.json` must be created.

```
CONF=test coverage run manage.py test
```

## Deploying :

You can deploy using one of the following :

* Create a tag on master branch (use `git push --tags` to push tags)
* Use gitlab web interface
* Use fabric `fab deploy` (you must have the `.pem` file enabled) 

## Assets :

* Install assets with `yarn` : `cd assets && yarn install`
* Launch gulp : `gulp`

