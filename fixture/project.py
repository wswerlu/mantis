from model.project import Project
import re


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def open_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_page.php"):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def return_to_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Proceed").click()

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_name("name", project.name)
        self.change_field_name("description", project.description)

    def change_field_name(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        # init project creation
        wd.find_element_by_css_selector("[value='Create New Project']").click()
        self.fill_project_form(project)
        # submit group creation
        wd.find_element_by_css_selector("input.button").click()
        self.return_to_projects_page()
        self.project_cache = None

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []
            for element in wd.find_elements_by_xpath("//a[contains(@href, 'manage_proj_edit_page')]"):
                text = element.text
                id = element.get_attribute("href").split("project_id=")[1]
                self.project_cache.append(Project(name=text, id=id))
        return list(self.project_cache)

    def delete_project_by_name(self, project_name):
        wd = self.app.wd
        self.open_projects_page()
        # open project
        wd.find_element_by_xpath(f"//a[text()='{project_name}']").click()
        # delete project
        wd.find_element_by_css_selector("[value='Delete Project']").click()
        # submit deleting project
        wd.find_element_by_css_selector("[value='Delete Project']").click()
        self.project_cache = None

    def count(self):
        wd = self.app.wd
        self.open_projects_page()
        return len(wd.find_elements_by_xpath("//a[contains(@href, 'manage_proj_edit_page')]"))

    def create_project_if_it_not_exist(self, project):
        wd = self.app.wd
        if self.count() == 0:
            self.create(project)

    def delete_project_by_index(self, index):
        wd = self.app.wd
        self.open_projects_page()
        # open project
        wd.find_elements_by_xpath("//a[contains(@href, 'manage_proj_edit_page')]")[index].click()
        # delete project
        wd.find_element_by_css_selector("[value='Delete Project']").click()
        # submit deleting project
        wd.find_element_by_css_selector("[value='Delete Project']").click()
        self.project_cache = None
