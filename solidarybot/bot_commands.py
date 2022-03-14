from nio import AsyncClient, MatrixRoom, RoomMessageText

from solidarybot.chat_functions import react_to_event, send_text_to_room
from solidarybot.config import Config
from solidarybot.storage import Storage


class Command:
    def __init__(
        self,
        client: AsyncClient,
        store: Storage,
        config: Config,
        command: str,
        room: MatrixRoom,
        event: RoomMessageText,
    ):
        """A command made by a user.

        Args:
            client: The client to communicate to matrix with.

            store: Bot storage.

            config: Bot configuration parameters.

            command: The command and arguments.

            room: The room the command was sent in.

            event: The event describing the command.
        """
        self.client = client
        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

    async def process(self):
        """Process the command"""
        if self.command.startswith("echo"):
            await self._echo()
        elif self.command.startswith("react"):
            await self._react()
        elif self.command.startswith("help"):
            await self._show_help()
        else:
            await self._unknown_command()

    async def _echo(self):
        """Echo back the command's arguments"""
        response = " ".join(self.args)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _react(self):
        """Make the bot react to the command message"""
        # React with a start emoji
        reaction = "⭐"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

        # React with some generic text
        reaction = "Some text"
        await react_to_event(
            self.client, self.room.room_id, self.event.event_id, reaction
        )

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = (
                "Hello, I am a bot made with matrix-nio! Use `help commands` to view "
                "available commands."
            )
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = "Available commands: ..."
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)
    async def _new_solidary(self):
        solidaryhast = self.args[0]
        solidarysum = self.args[1]
        solidarypri = self.args[2]
        solidaryday = self.args[3]
        solidarycom = self.args[4]
        if solidarypri == "Yes" or solidarypri == "yes":
            solidarypublic = False
            solidaryprivate = True
            if solidaryhast.startswith("#"):
                # Save info to database for reading it later
            else:
                await send_text_to_room(self.client, self.room.room_id, "You have to set hashtag to your solidary request if request is private.")
        elif solidarypri == "No" or solidarypri == "no":
            solidarypublic = True
            solidaryprivate = False
        elif not solidarypri or solidarypri == "help":
            text = "You have to set all functions, type help to get more info."
            await send_text_to_room(self.client, self.room.room_id, text)
            await _show_help
    async def _unknown_command(self):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        )
