from .handlers.processor import Processor
from .objects.preferences import Preferences
from .core.console import woody_logger, quiet
from woody.cli.cli import CLI
from woody.cli.setup import SetupCLI


class Woody:
    def __init__(self):
        self.processor = Processor()
        self.preferences = Preferences()
        self.cli = CLI()
        
    def run(self):
        if self.preferences.check():
            
            prefs = self.preferences.load()
            
            current_project = prefs.get("current_project")
            if current_project is not None:
                self._switch_projects(current_project)
            else:
                woody_logger.warning("No project selected. Use 'create_project' or 'switch'.")
            
        else:
            woody_logger.info("Initializing first-time setup...")
            setup_cli = SetupCLI()
            if setup_cli.run():
                self.run()
                self.cli.start()
                
    @quiet
    def _switch_projects(self, project_name):
        return self.preferences.switch_projects(project_name)