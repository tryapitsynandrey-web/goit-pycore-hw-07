import random
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.document import Document

from assistant_bot import commands
from assistant_bot.utils.console import console
from assistant_bot.utils.ux_messages import WELCOME_MESSAGES, GOODBYE_MESSAGES, WRONG_LANGUAGE_MESSAGES


class SmartCompleter(Completer):
    def __init__(self, address_book):
        self.address_book = address_book
        self.commands = list(commands.COMMAND_REGISTRY.keys()) + ['exit', 'close']

    def get_completions(self, document: Document, complete_event):
        text = document.text_before_cursor
        
        # If the input is empty or just standard command entry
        if ' ' not in text:
            for cmd in self.commands:
                if cmd.startswith(text):
                    yield Completion(cmd, start_position=-len(text))
            return
            
        # Context-aware completion
        full_command = text.split()
        cmd_name = full_command[0].lower()
        
        # Tag Autocompletion
        if cmd_name in ('filter_by_tag', 'remove_tag'):
            # Collect unique tags from the address book
            # book.tags structure: {contact_name: [tag1, tag2]}
            unique_tags = set()
            for tag_list in self.address_book.tags.values():
                unique_tags.update(tag_list)
            
            # The word being typed (last word)
            current_word = full_command[-1] if text.endswith(' ') is False else ''
            
            # If we are typing the tag argument (2nd word usually)
            # filter_by_tag <tag>
            if len(full_command) >= 1:
                for tag in unique_tags:
                    if tag.startswith(current_word):
                        yield Completion(tag, start_position=-len(current_word))


class App:
    def __init__(self, address_book=None):
        self.address_book = address_book
        self.running = True
        self.consecutive_errors = 0

    def run(self):
        # use SmartCompleter
        completer = SmartCompleter(self.address_book)
        
        style = Style.from_dict({
            'prompt': 'ansicyan bold',
        })
        
        session = PromptSession(completer=completer, style=style)

        console.print(f"[bold green]{WELCOME_MESSAGES[0]}[/bold green]")
        
        while self.running:
            try:
                user_input = session.prompt('bot> ')
                user_input = user_input.strip()
                
                # Check 1: Empty Input
                if not user_input:
                    self.consecutive_errors += 1
                    self._check_auto_help()
                    continue

                # Check 2: Language Detection (Non-ASCII implies non-English usually)
                if not user_input.isascii():
                     console.print(f"[bold yellow]{random.choice(WRONG_LANGUAGE_MESSAGES)}[/bold yellow]")
                     self.consecutive_errors += 1
                     self._check_auto_help()
                     continue

                # Dispatch command
                cmd_name = user_input.split()[0].lower()
                is_valid_command = cmd_name in commands.COMMAND_REGISTRY or cmd_name in ('exit', 'close')

                if is_valid_command:
                    self.consecutive_errors = 0
                    if not commands.dispatch(self.address_book, user_input):
                        self.running = False
                else:
                    self.consecutive_errors += 1
                    # Let dispatch handle printing "Unknown command" error
                    commands.dispatch(self.address_book, user_input)
                    self._check_auto_help()
                    
            except (KeyboardInterrupt, EOFError):
                self.running = False
            except Exception as e:
                console.print(f"[bold red]Unexpected error: {e}[/bold red]")

    def _check_auto_help(self):
        if self.consecutive_errors >= 3:
            console.print("\n[bold magenta]🤔 You seem lost. Here is the help menu:[/bold magenta]")
            commands.handle_help(self.address_book, [])
            self.consecutive_errors = 0

