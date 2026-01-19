from woody.pywoody.core.console import format_msg, BOLD, RESET

def help(self, args):
    """Show this help menu"""
    categories = {
        "Base Commands": ["help", "exit"],
        "Project Management": ["list", "switch", "create", "update"],
        "Navigation & Context": ["context"]
    }

    output = [
        f"\n{BOLD}WOODY CLI - PROJECT MANAGEMENT TOOL{RESET}",
        f"Usage: <command> [flags/args]\n"
    ]

    for cat_name, cmd_list in categories.items():
        output.append(f"{BOLD}{cat_name.upper()}{RESET}")
        for cmd_name in cmd_list:
            if cmd_name in self.commands:
                cmd_func = self.commands[cmd_name]
                doc = (cmd_func.__doc__ or "No description").split('\n')[0]
                output.append(f"  {cmd_name:12} - {doc}")
        output.append("")

    output.append(f"Type {BOLD}'create --help'{RESET} or similar for detailed flag info.")
    return "\n".join(output)

def exit(self, args):
        """Exit the CLI"""
        self.running = False
        return format_msg("woody", "Shutting Down...", "woody")