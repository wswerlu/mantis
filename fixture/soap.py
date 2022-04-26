from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:
    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = self.get_client()
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_client(self):
        base_url = self.app.config['web']['baseUrl']
        client = Client(base_url + "/api/soap/mantisconnect.php?wsdl")
        return client

    def get_project_list(self):
        client = self.get_client()
        projects = []
        config = self.app.config['webadmin']
        projects_mc = client.service.mc_projects_get_user_accessible(
            username=config["username"], password=config["password"])
        for project in projects_mc:
            projects.append(Project(id=project.id, name=project.name))
        return projects
