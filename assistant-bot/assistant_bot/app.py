import random
from typing import Optional, List, Iterable, TYPE_CHECKING

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.document import Document

from assistant_bot import commands, config
from assistant_bot.utils.console import console
from assistant_bot.utils.ux_messages import (
    WELCOME_MESSAGES, 
    WRONG_LANGUAGE_MESSAGES
)

if TYPE_CHECKING:
    from assistant_bot.models import AddressBook

# Constants
PROMPT_STYLE = Style.from_dict({
    'prompt': 'ansicyan bold',
})

TAG_COMMANDS = {'filter_by_tag', 'remove_tag'}


class SmartCompleter(Completer):
    """
    Context-aware completer for the CLI.
    Provides command suggestions and dynamic tag autocompletion.
    """
    def __init__(self, address_book: 'AddressBook'):
        self.address_book = address_book
        self.base_commands = list(commands.COMMAND_REGISTRY.keys()) + ['exit', 'close']

    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        
        # Case 1: Start of line or simple command entry
        if ' ' not in text:
            for cmd in self.base_commands:
                if cmd.startswith(text):
                    yield Completion(cmd, start_position=-len(text))
            return

        # Case 2: Argument completion (Context-aware)
        full_command = text.split()
        if not full_command:
            return

        cmd_name = full_command[0].lower()
        
        # Tag Autocompletion for specific commands
        if cmd_name in TAG_COMMANDS:
            yield from self._get_tag_completions(text, full_command)

    def _get_tag_completions(self, text: str, full_command: List[str]) -> Iterable[Completion]:
        """Helper to generate tag completions."""
        unique_tags = self.address_book.get_unique_tags()
        
        # Determine the word currently being typed
        current_word = full_command[-1] if not text.endswith(' ') else ''

        for tag in unique_tags:
            if tag.startswith(current_word):
                yield Completion(tag, start_position=-len(current_word))


class App:
    """
    Main application controller.
    """
    def __init__(self, address_book: 'AddressBook'):
        self.address_book = address_book
        self.running = True
        self.consecutive_errors = 0
        self.session: Optional[PromptSession] = None

    def run(self) -> None:
        """Starts the main application loop."""
        self._setup_session()
        console.print(f"[bold green]{WELCOME_MESSAGES[0]}[/bold green]")
        
        while self.running:
            try:
                self._process_cycle()
            except (KeyboardInterrupt, EOFError):
                self.running = False
            except Exception as e:
                console.print(f"[bold red]Unexpected error: {e}[/bold red]")

    def _setup_session(self) -> None:
        """Initializes the PromptSession with the completer."""
        completer = SmartCompleter(self.address_book)
        self.session = PromptSession(completer=completer, style=PROMPT_STYLE)

    def _process_cycle(self) -> None:
        """Handles a single cycle of the input loop."""
        if not self.session:
            return

        user_input = self.session.prompt('bot> ').strip()
        
        # Validation checks
        if not user_input:
            self._handle_error()
            return

        if not user_input.isascii():
            console.print(f"[bold yellow]{random.choice(WRONG_LANGUAGE_MESSAGES)}[/bold yellow]")
            self._handle_error()
            return

        # Execution
        self._execute_command(user_input)

    def _execute_command(self, user_input: str) -> None:
        """Dispatches the command or handles unknown commands."""
        cmd_name = user_input.split()[0].lower()
        is_known = cmd_name in commands.COMMAND_REGISTRY or cmd_name in ('exit', 'close')

        if is_known:
            self.consecutive_errors = 0
            # dispatch returns False if command signals exit
            should_continue = commands.dispatch(self.address_book, user_input)
            if not should_continue:
                self.running = False
        else:
            # Let dispatch handle the "Unknown command" message and simple routing
            commands.dispatch(self.address_book, user_input)
            self._handle_error()

    def _handle_error(self) -> None:
        """Increments error count and triggers auto-help if needed."""
        self.consecutive_errors += 1
        if self.consecutive_errors >= config.AUTO_HELP_THRESHOLD:
            console.print("\n[bold magenta]🤔 You seem lost. Here is the help menu:[/bold magenta]")
            commands.handle_help(self.address_book, [])
            self.consecutive_errors = 0

