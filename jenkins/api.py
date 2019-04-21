from .util import ApiHost, JsonRequests


class JenkinsApi(object):
    def __init__(self, hostname, **kwargs):
        self._host = ApiHost(hostname)
        self._http = JsonRequests(**kwargs)

    def jobs(self):
        return self._http.get(self._host('/api/json'))

    def job(self, job):
        return self._http.get(self._host(f'/job/{job}/api/json'))

    def run(self, job, run):
        return self._http.get(self._host(f'/job/{job}/{run}/api/json'))

    def git(self, job, run):
        return self._http.get(self._host(f'/job/{job}/{run}/git/api/json'))

    def stdout(self, job, run):
        return self._http.get(self._host(f'/job/{job}/{run}/consoleText'), raw=True)

    def people(self):
        return self._http.get(self._host('/asynchPeople/api/json'))

    def computer(self):
        return self._http.get(self._host('/computer/api/json'))

    def view_all(self):
        return self._http.get(self._host('/view/all/api/json'))
