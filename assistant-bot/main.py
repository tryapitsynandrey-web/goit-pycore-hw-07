from assistant_bot import storage
from assistant_bot.app import App
from assistant_bot.utils.ux_messages import WELCOME_MESSAGES, GOODBYE_MESSAGES


def main():
    # Load or create AddressBook
    address_book = storage.load_address_book()

    app = App(address_book)
    try:
        app.run()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        storage.save_address_book(address_book)
        print(GOODBYE_MESSAGES[0])


if __name__ == '__main__':
    main()
