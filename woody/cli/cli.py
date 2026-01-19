import sys
from .commands import CommandRegistry
from .splash_screen import SPLASH_SCREEN
from woody.pywoody.objects.guard import Guard
from woody.pywoody.core.console import format_msg, get_prompt

class CLI:
    guard = Guard()
    
    def __init__(self):
        self.registry = CommandRegistry()
        
    def start(self):
        
        print(SPLASH_SCREEN)

        print(format_msg("woody", "CLI - Type 'help' for commands, 'exit' to quit", "woody"))
        
        while self.registry.running:
            try:
                prompt = get_prompt(self.guard._current_project, self.guard._context)
                
                sys.stdout.write(prompt)
                sys.stdout.flush()
                
                user_input = input("").strip()
                
                if not user_input:
                    continue 
                
                result = self.registry.execute(user_input)
                if result:
                    print(result)
                
            except EOFError:
                break
            except KeyboardInterrupt:
                print(f"\n{format_msg('woody', 'Shutting down...', 'woody')}")
                self.registry.running = False
                break