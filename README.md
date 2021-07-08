# Deploy Django project to AWS ESB

## Local Deployment

## Reference

*[Deploy a Production Django App With Elastic Beanstalk (Part 1)](https://betterprogramming.pub/production-django-elastic-beanstalk-part1-6632c0d4956a#16a4)*

*[Deploy a Production Django App With Elastic Beanstalk (Part 2)](https://betterprogramming.pub/production-django-elastic-beanstalk-part2-4501caf7d8fb)*

*[Deploying a Django application to Elastic Beanstalk
](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)*

* Not very useful to deploy an existing project

## 1. Initialize

1. Setup virtual env by [`pipenv`](https://pipenv-fork.readthedocs.io/en/latest/basics.html) and generate `Pipfile`

2. (Optional) Install `awscli` to configure credential

3. [Install `awsebcli`](https://pypi.org/project/awsebcli/)

4. `eb init`: configure the Elastic Beanstalk, quite straight forward 
    
    **Note**
    
    * CodeCommit: Do not use CodeCommit for the project, it will conflict with git
    * SSH: Highly recommend to create a new keypair for the EC2 instance

5. Once the initialization is done, there will be a new directory `.elasticbeanstalk`, with a file `config.yml` in there.

*Note*: If you want to start over the Beanstalk project, just delete the directory and `eb init` again.

## 2. Creating the Beanstalk environment

```
eb create
```

* Env Name: What your environment will be named.
* DNS CNAME prefix: Leave as the default.
* Load Balancer Type: Choose Application.
* Spot Fleet Requests: Out of scope, select no.

After the creation, you can use `eb open` to open the application. Yet it will show 502 error because of *WSGI path*

After create, you can use `eb status` to check the configuration of the Beanstalk application.

    *Note*: `CNAME` indicate the application's url.

## 3. Configuration

1. create a new directory `.ebextensions` and config file inside

```shell=
mkdir .ebextensions
touch .ebextensions/django.config
```

Inside the django.config file, add the following:

```
option_settings:
  aws:elasticbeanstalk:application:environment:
    DJANGO_SETTINGS_MODULE: "config.settings"
    PYTHONPATH: "/var/app/current:$PYTHONPATH"
  aws:elasticbeanstalk:container:python:
    WSGIPath: "config.wsgi:application"
```

## 4. SSH into the Server

1. Get the EC2 instance public IP, it should have the same name as your Beanstalk project

2. Copy the public IP and run:

```shell=
ssh -i ~/.ssh/<keypair> ec2-user@<public-ip>
```

3. Navigate to the log directory with `cd /var/log/`, the following three files contains most information for deployment issues:

```
eb-engine.log
cfn-init.log
cfn-init-cmd.log
```

```
# Deployed project

/var/app/current

# Activate Virtual Environment

source /var/app/venv/<venv-name>/bin/activate

```

4. Allowed the host connection: Add `CNAME` to the `ALLOWED_HOST` in `config/settings.py`. The easiest but unsafe method is to make it allow all the connection by '*'.

## 5. Update config and deploy

Before deploy, commit all changes to the git repo (no need to push!)

```
git add .
git commit -m "messages"
```

Once the changes are committed, it's time to deploy the project.

```
eb deploy
```

## 6. Static Files