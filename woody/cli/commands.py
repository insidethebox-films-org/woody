from woody.pywoody.core.console import WoodyError, format_msg, handle_woody_errors

from .setup import SetupCLI
from .cmds.core import help, exit
from .cmds.context import set_context, switch_projects
from .cmds.queries import list
from .cmds.create import create
from .cmds.update import update

import shlex

class CommandRegistry:
    def __init__(self):
        self.commands = {
            "help": self.help,
            "exit": self.exit,
            "list": self.list,
            "context": self.set_context,
            "switch": self.switch_projects,
            "create": self.create,
            "update": self.update,
            "setup": self.setup 
        }
        self.running = True
        
    #==== Utils ====#
    
    def _parse_args(self, parser, args):
        try:
            return parser.parse_args(args)
        except SystemExit as e:
            # Exit code 0 means help was shown successfully
            if e.code == 0:
                return None
            raise WoodyError("")
    
    @handle_woody_errors
    def execute(self, cmd_line):
        parts = shlex.split(cmd_line)
        if not parts:
            return
        
        command = parts[0].lower()
        args = parts[1:]

        if command in ["--help", "-h"]:
            command = "help"
        
        if command not in self.commands:
            raise WoodyError(f"Unknown command '{command}'. Type 'help' for usage.")
        
        result = self.commands[command](args)
        
        if result is None:
            return
        
        if result:
            if command in ["exit", "help"]:
                return result
            return format_msg("Success", result, "success")

    #==== Base Commands ====#
    
    def help(self, args):
        return help(self, args)
        
    
    def exit(self, args):
        """Exit the CLI"""
        return exit(self, args)
    
    def setup(self, args):
        """Run Woody setup configuration"""
        setup_cli = SetupCLI()
        setup_cli.run()
        return None
    
    #==== list Commands ====#
    
    def list(self, args):
        """List created entities with flags"""
        return list(self, args)
    
    #==== Tool Commands ====#
    
    def set_context(self, args):
        """Change current working context (tree/group/asset)"""
        return set_context(self, args)
    
    def switch_projects(self, args):
        """Switch to a different active project."""
        return switch_projects(self, args)
        
    def create(self, args):
        """Create new entities: projects, assets, etc."""
        return create(self, args)

    def update(self, args):
        """Update metadata: -p '{"key":"value"}' | -a '{"key":"value"}'"""
        return update(self, args)