from __future__ import annotations

from typing import Tuple, TYPE_CHECKING, Any

if TYPE_CHECKING:
  from settings import SETTINGS  # type: ignore
else:
  class _DummySettings:
    pass

  SETTINGS = _DummySettings()

# =========================
# ТЕКСТОВІ ПОВІДОМЛЕННЯ (UX)
# =========================

AUTO_HELP_EVERY_EMPTY_INPUTS: int = getattr(SETTINGS, "auto_help_every_empty_inputs", 6)

WELCOME_MESSAGES: Tuple[str, ...] = (
  "👋🙂 Welcome to the assistant bot!\nThis tool helps you manage your contacts.\nType 'help' to see commands. =)",
  "🤖✨ Welcome!\nContact management is ready.\nEnter 'help' to see all commands ->",
  "👋😊 Hello and welcome!\nAdd, update, search and manage contacts.\nUse 'help' to get started. =)",
  "📇🙂 Welcome!\nYour contact assistant is online.\nType 'help' for guidance ->",
  "👋🤝 Hi there!\nLet’s keep your contacts tidy.\nType 'help' to begin. =)",
  "🤖🙂 Welcome!\nQuick contact management starts here.\nUse 'help' anytime ->",
  "✨👋 Welcome!\nI can help you add/find/update contacts.\nType 'help' to see options. =)",
  "🙂📞 Welcome!\nYour address book assistant is ready.\nType 'help' to learn commands ->",
  "👋🧭 Welcome!\nNot sure where to start?\nType 'help' and pick a command. =)",
  "🤖📌 Welcome!\nSimple CLI. Serious usefulness.\nType 'help' for the menu ->",
)

GOODBYE_MESSAGES: Tuple[str, ...] = (
  "👋🙂 Good bye! Thanks for using the assistant bot. =)",
  "😊👋 Good bye! See you next time! =)",
  "🌤️🙂 Good bye! Have a great day! =)",
  "🔒✅ Session ended. Your contacts are safe. =)",
  "💾🙂 Saved! Good bye and take care! =)",
  "🤝👋 Thanks for choosing the assistant bot! =)",
  "✨🙂 Bye! Stay productive and calm. =)",
  "🚀👋 Good bye! Come back anytime. =)",
  "😄👋 See you later! =)",
  "📇🙂 Address book closed. Bye! =)",
)

HELP_MESSAGE: str = (
  "┌──────────────────────────────────────────────────────────────┐\n"
  "│                   🤖  ASSISTANT BOT — HELP  🤖               │\n"
  "├──────────────────────────────────────────────────────────────┤\n"
  "│ 📌 MAIN COMMANDS (Contacts & Notes)                          │\n"
  "├──────────────────────────────┬───────────────────────────────┤\n"
  "│ help                         │ Show this help screen ℹ️🙂     │\n"
  "│ exit | close                 │ Save and exit 👋🙂             │\n"
  "│ add <name> [phone]           │ Add new contact ➕             │\n"
  "│ change <name> <old> <new>    │ Change phone number ✏️        │\n"
  "│ add_phone <name> <phone>     │ Add extra phone 📱            │\n"
  "│ phone <name>                 │ Show phones 📞                │\n"
  "│ delete <name>                │ Delete contact 🗑️              │\n"
  "│ add_email <name> <email>     │ Set email 📧                  │\n"
  "│ add_birthday <name> <date>   │ Set birthday (DD-MM-YYYY) 🎂  │\n"
  "│ birthdays [days]             │ Show upcoming birthdays 📅    │\n"
  "│ days_to_bday <name>          │ Days until birthday ⏳        │\n"
  "│ search <query>               │ Search contacts 🔍            │\n"
  "│ list                         │ List all contacts 📋          │\n"
  "│ add_note <name> <text>       │ Add text note 📝              │\n"
  "│ edit_note <name> <id> <text> │ Edit note by index ✍️         │\n"
  "│ delete_note <name> <id>      │ Delete note ❌                │\n"
  "│ search_notes <query>         │ Search in notes 🔎            │\n"
  "│ list_notes [name]            │ Show notes 🗒️                 │\n"
  "├──────────────────────────────┴───────────────────────────────┤\n"
  "│ 🏷️ TAGS                                                      │\n"
  "├──────────────────────────────┬───────────────────────────────┤\n"
  "│ add_tag <name> <tag>         │ Add tag to contact 🏷️         │\n"
  "│ remove_tag <name> <tag>      │ Remove tag ➖                 │\n"
  "│ list_tags                    │ List all tags 📑              │\n"
  "│ filter_by_tag <tag>          │ Filter contacts by tag 🧩     │\n"
  "├──────────────────────────────┴───────────────────────────────┤\n"
  "│ 💾 DATA & SYSTEM                                             │\n"
  "├──────────────────────────────┬───────────────────────────────┤\n"
  "│ import <path>                │ Import from JSON/CSV 📥       │\n"
  "│ export <path>                │ Export to JSON/CSV 📤         │\n"
  "└──────────────────────────────────────────────────────────────┘"
)

EMPTY_INPUT_MESSAGES: Tuple[str, ...] = (
  "⏎🙂 Empty input.\nPlease type a command or use 'help'. =)",
  "🤔🙂 Nothing entered.\nTry a command or type 'help'. ->",
  "📝🙂 No command detected.\nType 'help' to see options. =)",
  "⌨️🙂 Just Enter?\nPlease enter a command (or 'help'). ->",
  "💡🙂 Tip: type 'help' anytime.\nEnter a command to proceed. =)",
  "👀🙂 I’m still here.\nPlease type a command. ->",
  "🧭🙂 Not sure what to do?\nType 'help' and pick a command. =)",
  "📌🙂 Waiting for your input...\nType a command or 'help'. ->",
  "🕒🙂 Still waiting...\nType something meaningful. =)",
  "✨🙂 Start with 'help'.\nIt’s the safest move. ->",
)

INVALID_COMMAND_MESSAGES: Tuple[str, ...] = (
  "❌🙂 Invalid command.\nType 'help' to see supported commands. ->",
  "🚫🙂 Command not recognized.\nUse 'help' for the list. =)",
  "📛🙂 Unsupported command.\nType 'help' to view options. ->",
  "🤔🙂 Unknown command.\nCheck spelling or type 'help'. =)",
  "📘🙂 Need help?\nType 'help' to continue. ->",
  "⚠️🙂 I can’t do that.\nTry 'help' for available commands. =)",
  "🔎🙂 Not found.\nType 'help' to see the menu. ->",
  "🧠🙂 I didn’t understand.\nUse 'help' and try again. =)",
  "🧭🙂 Wrong direction.\nType 'help' for guidance. ->",
  "🙃🙂 Nope.\nType 'help' and we’ll pretend it never happened. =)",
)

NO_CONTACTS_MESSAGES: Tuple[str, ...] = (
  "📭🙂 No contacts saved yet.\nUse 'add' to create one. =)",
  "📂🙂 Your contact list is empty.\nStart with 'add <name> <phone>'. ->",
  "🗒️🙂 No contacts found.\nTry adding your first contact. =)",
  "✨🙂 Nothing here yet.\nUse 'add' to begin. ->",
  "📘🙂 Empty address book.\nType 'add' to create a contact. =)",
  "📞🙂 No contacts.\nAdd one and we’ll talk again. ->",
  "🧭🙂 Start simple:\nadd John +123456789. =)",
  "🚀🙂 Ready when you are.\nAdd your first contact. ->",
  "🙂📇 No entries.\nUse 'add' to populate the list. =)",
  "💡🙂 Tip:\nUse 'help' if you forget syntax. ->",
)

CONTACT_ADDED_MESSAGES: Tuple[str, ...] = (
  "✅🙂 Validated! Contact {name} has been added to the matrix.",
  "🎉🙂 Hooray! {name} is now part of your exclusive club.",
  "💾🙂 Saved. {name} is safe with me.",
  "🤝🙂 Nice to meet you, {name}! Contact added.",
  "🦾🙂 As you wish. {name} has been assimilated.",
  "📘🙂 The archives are complete. {name} added.",
  "✨🙂 Magic! {name} appears in your list.",
  "🚀🙂 {name} has boarded the spaceship. Added!",
  "📇🙂 Rolodex updated. Welcome, {name}.",
  "🧱🙂 Another brick in the wall. {name} added.",
)

CONTACT_UPDATED_MESSAGES: Tuple[str, ...] = (
  "✏️🙂 Polished and shiny! {name} has been updated.",
  "🔄🙂 Evolution complete. {name} is new and improved.",
  "🧬🙂 DNA modified. {name} updated successfully.",
  "📝🙂 Rewriting history... {name} changed.",
  "🔧🙂 Tightened the bolts on {name}. Updated.",
  "🎨🙂 A fresh coat of paint for {name}.",
  "🦄🙂 {name} transformed! Update successful.",
  "✅🙂 Acknowledged. {name} is up to date.",
  "💾🙂 Overwritten. {name} is new now.",
  "🧐🙂 Indeed. {name} has been revised.",
)

PHONE_ADDED_MESSAGES: Tuple[str, ...] = (
  "📞🙂 Ring ring! New phone added to {name}.",
  "📱🙂 More connectivity! {name} has a new number.",
  "🔌🙂 {name} is now even more reachable.",
  "📡🙂 Signal boosted. Phone added for {name}.",
  "🔗🙂 Connection established. {name} +1 Phone.",
  "☎️🙂 Operator? Add this number to {name}. Done.",
  "🗣️🙂 Can you hear me now? Phone added to {name}.",
  "📟🙂 Beep me. {name} gets a new digit.",
  "🎰🙂 Jackpot! Number added for {name}.",
  "📶🙂 Full bars. Phone attached to {name}.",
)

PHONE_UPDATED_MESSAGES: Tuple[str, ...] = (
  "🔄🙂 Number ported. {name}'s phone updated.",
  "📞🙂 New digits, who dis? {name} updated.",
  "📲🙂 SIM card swapped. Phone changed for {name}.",
  "📡🙂 Frequencies adjusted. {name}'s number updated.",
  "📝🙂 Cross out the old one. {name}'s phone is new.",
  "🔧🙂 Replaced the wiring. Phone updated for {name}.",
  "♻️🙂 Recycled the old number. {name} has a new one.",
  "✅🙂 Corrected. {name}'s phone is set.",
  "☎️🙂 Switchboard updated for {name}.",
  "🧬🙂 Number mutation complete for {name}.",
  "🧬🙂 Number mutation complete for {name}.",
)

DUPLICATE_PHONE_MESSAGES: Tuple[str, ...] = (
  "📞🙂 Deja vu! This phone number is already in the system.",
  "🚫🙂 Copycat detected. Phone number already exists.",
  "👯🙂 Double trouble. This phone belongs to someone else.",
  "🛑🙂 Halt! I've seen this number before. Duplicate found.",
  "💾🙂 Memory check: Phone number match found. Try another.",
  "🤖🙂 My positronic brain recalls this number. It's taken.",
  "📵🙂 Line busy. This number is assigned to another contact.",
  "⚡🙂 Static interference. Duplicate phone number detected.",
  "🦜🙂 Squawk! Phone taken! Squawk!",
  "🔮🙂 I foresee a conflict. This number exists already.",
)

DUPLICATE_EMAIL_MESSAGES: Tuple[str, ...] = (
  "📧🙂 Email clash! This address is already taken.",
  "📨🙂 Full inbox? No, just a duplicate email address.",
  "📫🙂 Return to sender. Email {email} is already in use.",
  "👯🙂 Double vision. This email belongs to someone else.",
  "🚫🙂 SPAM filter says: Duplicate email detected.",
  "💻🙂 System conflict. Email {email} exists in the matrix.",
  "🦜🙂 Polly says: 'Duplicate! Duplicate!' (Email taken).",
  "🛑🙂 Stop right there. That email is already registered.",
  "🔍🙂 Found it! ...associated with another contact. Try a different email.",
  "⚡🙂 Lightning strikes twice? Not with emails. Duplicate found.",
)

CONTACT_DELETED_MESSAGES: Tuple[str, ...] = (
  "🗑️🙂 Dust to dust. {name} has been deleted.",
  "👻🙂 {name}? Who is {name}? (Deleted).",
  "💨🙂 Gone with the wind. {name} removed.",
  "🧹🙂 Swept away. {name} is no more.",
  "🚫🙂 Access denied. {name} deleted.",
  "📉🙂 Downsizing. {name} let go.",
  "👋🙂 Sayonara, {name}. Deleted.",
  "🧼🙂 Clean slate. {name} removed.",
  "🌋🙂 Thrown into the volcano. {name} deleted.",
  "🛸🙂 {name} was abducted by aliens. (Deleted).",
)

EMAIL_UPDATED_MESSAGES: Tuple[str, ...] = (
  "📧🙂 You've got mail! Email set for {name}.",
  "📨🙂 Inbox ready. Email updated for {name}.",
  "📫🙂 Postman knows where to go. Email added for {name}.",
  "🌐🙂 Digital identity established. Email for {name}.",
  "📤🙂 Send it! Email saved for {name}.",
  "🐦🙂 Carrier pigeon replaced by email for {name}.",
  "💌🙂 Sealed with a kiss (and an @ symbol). Email set for {name}.",
  "💻🙂 @test.com? No, real email added for {name}.",
  "📡🙂 Comms channel open. Email for {name}.",
  "📝🙂 Rolodex updated with email for {name}.",
)

BIRTHDAY_UPDATED_MESSAGES: Tuple[str, ...] = (
  "🎂🙂 Cake alert! Birthday set for {name}.",
  "🎉🙂 Party time! Birthday saved for {name}.",
  "📅🙂 Calendar marked. Don't forget {name}'s bday!",
  "🎈🙂 Balloons ordered. Birthday for {name} is set.",
  "🕯️🙂 Make a wish! Birthday added for {name}.",
  "🎁🙂 Gift shopping starts now. Birthday for {name}.",
  "🕰️🙂 The clock is ticking until {name}'s bday.",
  "🍰🙂 The cake is a lie? No, {name}'s bday is real.",
  "🥳🙂 Confetti ready. Birthday recorded for {name}.",
  "👶🙂 Born on this day... Birthday set for {name}.",
)

NOTE_ADDED_MESSAGES: Tuple[str, ...] = (
  "📝🙂 Noted. Don't forget it, {name}.",
  "📌🙂 Pinned to the board. Note added for {name}.",
  "🧠🙂 Stored in external memory. Note for {name}.",
  "🗒️🙂 Scribbled down. Note saved for {name}.",
  "🖊️🙂 Ink dry. Note added for {name}.",
  "💡🙂 Bright idea! Note attached to {name}.",
  "📑🙂 Filed away. Note for {name}.",
  "🔖🙂 Bookmarked. Note added for {name}.",
  "🤐🙂 Secret (or not) kept. Note for {name}.",
  "💾🙂 Data fragment saved. Note for {name}.",
)

NOTE_UPDATED_MESSAGES: Tuple[str, ...] = (
  "✍️🙂 Edited. Note for {name} improved.",
  "🔄🙂 Revision history updated. Note for {name} changed.",
  "📝🙂 Rewrite complete. Note for {name} updated.",
  "🎨🙂 Touching up the details. Note for {name} updated.",
  "🔧🙂 Tweaked. Note for {name} passed QC.",
  "📄🙂 Version 2.0. Note for {name} updated.",
  "♻️🙂 Refreshed. Note for {name} is new.",
  "✅🙂 Correction applied. Note for {name} updated.",
  "🧬🙂 Evolved. Note for {name} changed.",
  "🖊️🙂 Red pen used. Note for {name} updated.",
)

NOTE_DELETED_MESSAGES: Tuple[str, ...] = (
  "🗑️🙂 Shredded. Note for {name} deleted.",
  "🔥🙂 Burned after reading. Note for {name} gone.",
  "🧼🙂 Washed away. Note for {name} removed.",
  "🧹🙂 Cleaned up. Note for {name} deleted.",
  "✂️🙂 Snip snip. Note for {name} cut.",
  "💨🙂 Vaporized. Note for {name} deleted.",
  "🌬️🙂 Gone with the breeze. Note for {name} removed.",
  "🚫🙂 Redacted. Note for {name} deleted.",
  "📉🙂 Less baggage. Note for {name} deleted.",
  "🚮🙂 Binned. Note for {name} deleted.",
)

TAG_ADDED_MESSAGES: Tuple[str, ...] = (
  "🏷️🙂 Tagged! {name} is now '{tag}'.",
  "📌🙂 Label applied. {name} +{tag}.",
  "🔖🙂 Categorized. 'tag' added to {name}.",
  "🎨🙂 Color coded. {name} is '{tag}'.",
  "🧩🙂 Piece fits. Tag '{tag}' added to {name}.",
  "🔗🙂 Linked. {name} is part of '{tag}'.",
  "📦🙂 Boxed. {name} tagged as '{tag}'.",
  "🆕🙂 Branding. {name} gets '{tag}'.",
  "📍🙂 Map marker. {name} tagged '{tag}'.",
  "📎🙂 Clipped. {name} tagged '{tag}'.",
)

TAG_REMOVED_MESSAGES: Tuple[str, ...] = (
  "🏷️🙂 Untagged. {name} lost the label.",
  "✂️🙂 Cut loose. Tag removed from {name}.",
  "🧼🙂 Scrubbed. Tag gone from {name}.",
  "🆓🙂 Free agent. Tag removed from {name}.",
  "🧹🙂 Swept away. Tag removed from {name}.",
  "📉🙂 De-categorized. {name} has fewer tags.",
  "🚫🙂 Label peeled off. Tag removed from {name}.",
  "🗑️🙂 Tag trashed. {name} updated.",
  "💨🙂 Poof. Tag gone from {name}.",
  "🧊🙂 Cool. Tag removed from {name}.",
)

IMPORT_SUCCESS_MESSAGES: Tuple[str, ...] = (
  "📥🙂 Download complete. Data imported from {path}.",
  "📦🙂 Package received. Import successful from {path}.",
  "🚛🙂 Delivery made. Contacts imported from {path}.",
  "🏗️🙂 Foundation built. Data loaded from {path}.",
  "🧬🙂 Genetic material added. Import from {path} done.",
  "💾🙂 Read operation successful. {path} imported.",
  "🧛🙂 I have invited them in. Import from {path} complete.",
  "🚀🙂 Cargo loaded. {path} imported.",
  "📚🙂 Library expanded. Import from {path} done.",
  "🎼🙂 New sheet music. {path} imported.",
)

EXPORT_SUCCESS_MESSAGES: Tuple[str, ...] = (
  "📤🙂 Upload complete. Data exported to {path}.",
  "📦🙂 Package sent. Export successful to {path}.",
  "🚀🙂 Satellite launched. Data saved to {path}.",
  "💾🙂 Backup created. Exported to {path}.",
  "💎🙂 Treasure buried. Data exported to {path}.",
  "🧊🙂 Frozen for later. Exported to {path}.",
  "📜🙂 Scroll written. Exported to {path}.",
  "🚢🙂 Ship has sailed. Data exported to {path}.",
  "📡🙂 Transmission sent. Export to {path} done.",
  "📸🙂 Snapshot taken. Exported to {path}.",
)

DELETE_ALL_MESSAGES: Tuple[str, ...] = (
  "🧨🙂 Boom! All contacts have been vaporized.",
  "🌪️🙂 Category 5 hurricane passed through. Address book is empty.",
  "🕳️🙂 Black hole activated. Everything is gone.",
  "🧼🙂 Squeaky clean. All data wiped.",
  "📉🙂 Market crash. You have 0 contacts now.",
  "👻🙂 It's a ghost town in here. Deleted all.",
  "🗑️🙂 Massive cleanup complete. 0 survivors.",
  "⚪🙂 Tabula rasa. Blank slate restored.",
  "💀🙂 The purge is complete. Address book reset.",
  "🛑🙂 Factory reset executed. Good luck.",
)

WRONG_LANGUAGE_MESSAGES: Tuple[str, ...] = (
  "🌍🙂 I only speak Python and English! Try again. =)",
  "🤔🙂 That looks like Elvish. English please? ->",
  "🥐🙂 Monsieur, I do not understand. English commands only! =)",
  "🐉🙂 High Valyrian is not supported yet. Try English. ->",
  "🤖🙂 Beep boop. Translation module broken. Use English. =)",
  "👽🙂 I come in peace, but I don't speak your language. ->",
  "📜🙂 Is that a magic spell? Please stick to English commands. =)",
  "🧱🙂 It's all Greek to me! English, please. ->",
  "🎵🙂 Nice lyrics, but I need a command in English. =)",
  "🛑🙂 System error: User speaking in tongues. Rebooting... JK, use English. ->",
)

UNKNOWN_COMMAND_MESSAGES: Tuple[str, ...] = (
  "🤯🙂 Whoops! '{cmd}' is not a valid command. Check 'help'!",
  "🕵️‍♂️🙂 Searching for '{cmd}'... 404 Not Found. Try again.",
  "🧙‍♂️🙂 You shall not pass! (Invalid command '{cmd}').",
  "🌌🙂 Houston, we have a problem. '{cmd}' is unknown.",
  "🦄🙂 I believe in unicorns, but not in '{cmd}'.",
  "🎱🙂 Outlook not so good for '{cmd}'. Try 'help'.",
  "🍟🙂 Sir, this is a Wendy's. We don't serve '{cmd}' here.",
  "🐢🙂 I'm too slow to understand '{cmd}'. Speak Python to me.",
  "👻🙂 That command is a ghost. It doesn't exist.",
  "🧩🙂 I'm puzzled. '{cmd}' doesn't fit the puzzle. See 'help'.",
)

MISSING_ARGS_MESSAGES: Tuple[str, ...] = (
  "😱🙂 You forgot the most important part! Usage: {syntax}",
  "🔮🙂 I'm not a mind reader (yet). Please use: {syntax}",
  "🥪🙂 This sandwich is missing the filling. Try: {syntax}",
  "🏃🙂 You're running too fast! Don't forget arguments: {syntax}",
  "🎭🙂 The stage is set, but the actors (arguments) are missing: {syntax}",
  "📉🙂 Incomplete data. Please provide: {syntax}",
  "👻🙂 Spooky! Invisible arguments detected. Real ones needed: {syntax}",
  "🦜🙂 Polly wants a cracker... and arguments: {syntax}",
  "🧩🙂 Missing pieces. Complete the puzzle: {syntax}",
  "🚦🙂 Red light! Stop. You missed arguments: {syntax}",
)

CONTACT_NOT_FOUND_MESSAGES: Tuple[str, ...] = (
  "🤷‍♂️🙂 Contact '{name}' is playing hide and seek. Cannot find them.",
  "🕵️‍♂️🙂 Sherlock Holmes couldn't find '{name}' in your list.",
  "📉🙂 404 Error: Contact '{name}' not found.",
  "👻🙂 '{name}' must be a ghost. Not in your book.",
  "🌌🙂 Searched the galaxy, but '{name}' is missing.",
  "📇🙂 I checked the rolodex twice. No '{name}' there.",
  "🧊🙂 '{name}'? Never heard of them.",
  "🌵🙂 It's a desert here. '{name}' is not found.",
  "🧙‍♂️🙂 Not even magic can find '{name}' in this list.",
  "🚫🙂 Access denied. '{name}' does not exist.",
)

INVALID_PHONE_MESSAGES: Tuple[str, ...] = (
  "📞🙂 That... doesn't look like a phone number: {phone}",
  "📵🙂 'Hello?' No, {phone} is not a valid number.",
  "🔢🙂 Math error using {phone}. Must be 10 digits or start with +38.",
  "👽🙂 Is {phone} an alien frequency? Try a real number.",
  "🔨🙂 You broke the dial. {phone} is invalid.",
  "🎰🙂 Almost a jackpot? No, {phone} is wrong format.",
  "🧱🙂 Hit a wall. {phone} is not reachable.",
  "🤕🙂 Ouch. {phone} hurts my processor. Fix it!",
  "🙅‍♂️🙂 Computer says NO. {phone} is invalid.",
  "📜🙂 Ancient glyphs? No, just an invalid phone: {phone}.",
)

INVALID_EMAIL_MESSAGES: Tuple[str, ...] = (
  "📧🙂 broken_email_detected: {email}. Try user@domain.com.",
  "📤🙂 Returned to sender. {email} is invalid.",
  "📫🙂 No mailbox found for {email}.",
  "🚫🙂 @ missing? Domain wrong? {email} is unreadable.",
  "📝🙂 Check your spelling. {email} is not an email.",
  "🕵️‍♂️🙂 Looks suspicious. {email} is not a valid address.",
  "🗑️🙂 Junk folder material. {email} is invalid.",
  "🦆🙂 Quack! That's not an email: {email}.",
  "⛔🙂 Stop. {email} cannot pass validation.",
  "🕸️🙂 Caught in the web. {email} is invalid.",
)

INVALID_BIRTHDAY_MESSAGES: Tuple[str, ...] = (
  "📅🙂 Are you a time traveler? Format must be DD-MM-YYYY.",
  "🎂🙂 No cake for you yet. Invalid date format.",
  "🚫🙂 Calendar confused. Please use DD-MM-YYYY.",
  "🕰️🙂 Time paradox detected. Check the date format.",
  "📜🙂 The scrolls require DD-MM-YYYY format.",
  "🤕🙂 My date parser hurts. Use DD-MM-YYYY.",
  "🔢🙂 Numbers, Mason! What do they mean? (Use DD-MM-YYYY).",
  "🦖🙂 From the dinosaur era? Invalid date.",
  "📆🙂 Date rejected. Try DD-MM-YYYY.",
  "🛑🙂 Hold up. That's not a birthday. Use DD-MM-YYYY.",
)

INVALID_INDEX_MESSAGES: Tuple[str, ...] = (
  "🔢🙂 That number is out of bounds!",
  "📉🙂 Index error. Pick a number from the list.",
  "🎯🙂 Missed it! Invalid index.",
  "🎲🙂 Rolled a critical fail. Index invalid.",
  "🚫🙂 There is no note at that number.",
  "🤷‍♂️🙂 Which one? That index doesn't exist.",
  "📐🙂 Measure twice, cut once. Index is wrong.",
  "🧱🙂 You hit the edge of the known universe (list).",
  "🕸️🙂 Nothing there but cobwebs. Invalid index.",
  "❌🙂 X marks the spot... but not that spot. Invalid index.",
)
