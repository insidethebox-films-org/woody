import argparse
import sys
from woody.pywoody.objects.preferences import Preferences
from woody.pywoody.core.console import woody_logger, SUCCESS_LEVEL, WOODY, GREEN, ORANGE, RESET


class SetupConfig:
    def __init__(self, user_name=None, projects_directory=None, mongodb_address=None):
        self.user_name = user_name
        self.projects_directory = projects_directory
        self.mongodb_address = mongodb_address or "mongodb://localhost:27017"
    
    def get_user_input(self, prompt, default=None):
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            while True:
                user_input = input(f"{prompt}: ").strip()
                if user_input:
                    return user_input
                woody_logger.warning("This field is required. Please enter a value.")
    
    def collect_interactive_input(self):
        print(f"{WOODY}[woody setup]{RESET}")
        print("Configure your woody environment\n")
        
        self.user_name = self.get_user_input("Enter your user name")
        self.projects_directory = self.get_user_input("Enter projects directory path")
        self.mongodb_address = self.get_user_input("Enter MongoDB address", "mongodb://localhost:27017")
    
    def show_summary(self):
        print(f"\n{ORANGE}[Configuration Summary]{RESET}")
        print(f"[User Name] {self.user_name}")
        print(f"[Projects Directory] {self.projects_directory}")
        print(f"[MongoDB Address] {self.mongodb_address}")
    
    def confirm_settings(self):
        confirm = input("\nSave these settings? (y/N): ").strip().lower()
        return confirm in ['y', 'yes']
    
    def is_complete(self):
        return bool(self.user_name and self.projects_directory)
    
    def save_preferences(self):
        prefs = Preferences()
        prefs.create_prefs(self.user_name, self.projects_directory, self.mongodb_address)


class SetupCLI:
    
    def __init__(self):
        self.config = SetupConfig()
    
    def setup_interactive(self):
        try:
            self.config.collect_interactive_input()
            self.config.show_summary()
            
            if self.config.confirm_settings():
                self.config.save_preferences()
                woody_logger.log(SUCCESS_LEVEL, "Woody setup completed successfully!")
                return True
            else:
                woody_logger.warning("Setup cancelled.")
                return False
                
        except Exception as e:
            woody_logger.error(f"Error during setup: {e}")
            return False
    
    def setup_with_args(self, args):
        self.config = SetupConfig(
            user_name=args.user,
            projects_directory=args.projects_dir,
            mongodb_address=args.mongodb
        )
        
        if not self.config.is_complete():
            woody_logger.error("User name and projects directory are required")
            return False
        
        if not args.force:
            self.config.show_summary()
            if not self.config.confirm_settings():
                woody_logger.warning("Setup cancelled.")
                return False
        
        try:
            self.config.save_preferences()
            woody_logger.info("Woody setup completed successfully!")
            return True
        except Exception as e:
            woody_logger.error(f"Error during setup: {e}")
            return False
    
    def run(self, args=None):
        if args and args.user and args.projects_dir:
            return self.setup_with_args(args)
        else:
            return self.setup_interactive()