[![pipeline status](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/pipeline.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

[![coverage report](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/badges/dev/coverage.svg)](https://gitlab.com/e-reflex/{{cookiecutter.project_slug}}/commits/dev)

# {{cookiecutter.project_slug}}

* dev domain : {{cookiecutter.dev_domain_name}}
* prod domain : {{cookiecutter.domain_name}}

## Branch convention

Here are conventions for branching :

* `master` is the branch used in production
* `dev` is the branch used for development (before the site is live)
* `feature-[something]` is the branch use to develop the feature [name]
* there is no `staging` branch, use the dev branch instead

## Running tests :

```
coverage run manage.py test
```

Test are automatically run with gitlab using .env.gitlab.conf and a postgresql database (set on gitlab).


## Deploying :

You can deploy using one of the following :

* Create a tag on master branch (use `git push --tags` to push tags)
* Use gitlab web interface
* Use fabric `fab deploy` (you must have the `.pem` file enabled) 

## Assets :

* Install assets with `yarn` : `cd assets && yarn install`
* Launch gulp : `gulp`

