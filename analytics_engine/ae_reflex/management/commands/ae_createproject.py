from django.core.management.base import BaseCommand, NoArgsCommand
from django.core import exceptions
from ae_reflex.models import Project, Key


class Command(BaseCommand):
    help = 'Create a new Project'
    args = "name"

    def handle(self, *args, **options):
        project_name = args[0]
        project = Project.create_project(project_name)
        self.stdout.write('Project successfully created')
        print("Project External ID = ", str(project.external_id))

        exit_flag = False
        while not exit_flag:
            input_msg = 'Do you want to create source key(s) for this project? [y/n]: '
            command_input = input(input_msg)
            if command_input == 'y' or command_input == 'Y':
                input_msg = 'Enter Key name: '
                command_input = input(input_msg)
                key = Key.create_key(command_input, project)
                print("Key ID = ", str(key.unique_id))
            elif command_input == 'n' or command_input == 'N':
                print(command_input)
                exit_flag = True
            else:
                print("Unrecognized input")
