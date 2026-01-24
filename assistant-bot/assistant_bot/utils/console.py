import random
from rich.console import Console
from rich.theme import Theme

# Custom theme for professional look
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "header": "bold magenta",
    "highlight": "bold white"
})

console = Console(theme=custom_theme)

def print_error(msg: str):
    console.print(f"[error]❌ {msg}[/error]")

def print_success(msg: str):
    console.print(f"[success]✅ {msg}[/success]")

def print_info(msg: str):
    console.print(f"[info]ℹ️  {msg}[/info]")

def print_warning(msg: str):
    console.print(f"[warning]⚠️  {msg}[/warning]")

def print_duplicate_error(owner_name: str, owner_data: dict, value: str, messages: tuple):
    """
    Prints a gamified duplicate error message.
    """
    msg = random.choice(messages)
    # Attempt to format if the message expects it
    try:
        # We provide common context variables
        formatted_msg = msg.format(name=owner_name, email=value, phone=value)
    except (IndexError, KeyError, ValueError):
        # If formatting fails (e.g. placeholder missing or different), use raw message
        formatted_msg = msg
        
    console.print(f"[error]❌ {formatted_msg}[/error] (Owned by: [bold]{owner_name}[/bold])")
