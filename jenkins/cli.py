import functools
import json
import os
import click
import dotenv
from .api import JenkinsApi


dotenv.load_dotenv(dotenv_path=os.path.join(os.getenv('HOME', '.'), '.jenkins-env'))


HOSTNAME = os.getenv('JENKINS_HOST')
VERIFY_SSL = not bool(os.getenv('JENKINS_NOVERIFY'))
USERNAME = os.getenv('JENKINS_USERNAME')
TOKEN = os.getenv('JENKINS_TOKEN')


def api_command(group):
    def decorator(func):
        @group.command()
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            api = JenkinsApi(HOSTNAME, auth=(USERNAME, TOKEN), verify=VERIFY_SSL)
            response = func(api, *args, **kwargs)
            result = response if isinstance(response, str) else json.dumps(response, indent=2)
            print(result)
        return wrapper
    return decorator


@click.group()
def main():
    pass


@api_command(main)
def jobs(api):
    return api.jobs()


@api_command(main)
@click.option('-j', '--job', required=True)
def job(api, job):
    return api.job(job)


@api_command(main)
@click.option('-j', '--job', required=True)
@click.option('-r', '--run', required=True)
@click.option('-g', '--git', 'job_action', flag_value='git')
@click.option('-s', '--stdout', 'job_action', flag_value='stdout')
@click.option('--default', 'job_action', flag_value='run', default=True)
def run(api, job, run, job_action):
    action = getattr(api, job_action)
    return action(job, run)


@api_command(main)
def computer(api):
    return api.computer()


@api_command(main)
def people(api):
    return api.people()


@api_command(main)
def builds(api):
    return api.view_all()
