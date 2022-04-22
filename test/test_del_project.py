from model.project import Project
from random import randrange


def test_del_some_project(app, config):
    app.project.create_project_if_it_not_exist(Project(name="test"))
    old_projects = app.soap.get_project_list(
        username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    index = randrange(len(old_projects))
    app.project.delete_project_by_index(index)
    new_projects = app.soap.get_project_list(
        username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    assert len(old_projects) - 1 == len(new_projects)
    del old_projects[index]
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
