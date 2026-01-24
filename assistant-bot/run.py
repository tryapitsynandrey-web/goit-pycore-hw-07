import sys
import os

# Ensure the package is in the python path if running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from assistant_bot import storage
from assistant_bot.app import App
from assistant_bot.utils.ux_messages import GOODBYE_MESSAGES

def main():
    """
    Main entry point for the Assistant Bot.
    Initializes the AddressBook, starts the App loop, and handles graceful shutdown.
    """
    # 1. Load Data (JSON)
    address_book = storage.load_address_book()

    # 2. Initialize App
    app = App(address_book)

    # 3. Run Main Loop
    try:
        app.run()
    except (KeyboardInterrupt, SystemExit):
        # Handle manual interruption (Ctrl+C)
        pass
    except Exception as e:
        print(f"Unexpected crash: {e}")
    finally:
        # 4. Save Data on Exit
        storage.save_address_book(address_book)
        print(GOODBYE_MESSAGES[0])

if __name__ == '__main__':
    main()
