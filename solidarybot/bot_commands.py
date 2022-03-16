from nio import AsyncClient, MatrixRoom, RoomMessageText, EnableEncryptionBuilder
import logging
from solidarybot.chat_functions import react_to_event, send_text_to_room
from solidarybot.config import Config
from solidarybot.storage import Storage
logger = logging.getLogger(__name__)
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
        elif self.command.startswith("new"):
            await self._solidary_new()
        elif self.command.startswith("donate"):
            await self._solidary_donate()
        elif self.command.startswith("requests"):
            await self._solidary_requests()
        elif self.command.startswith("calc"):
            await self.donatefinalamount()
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
            text = "Available commands: <br>"
            text += "`new` <br> use: <br> new [wanted sum] [wanted hashtag] [your username]"
            text += "`donate` <br> use: <br> donate [sum you want to donate] [hashtag to donate] [your username]"
        elif topic == "new":
            text = "Text"
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)
    async def _solidary_new(self):
        """
        Handles the new solidary requests
        """
        solidaryhast = self.args[0]
        solidarysum = self.args[1]
        solidarygo = self.args[2]
        if solidaryhast.startswith("#"):
            if solidarygo.startswith("@"):
                self.store.new_solidary(solidaryhast, solidarysum, solidarygo)
                solidarycreateden = f"🇺🇸 <br> New solidary request created with hashtag: '{solidaryhast}'."
                solidarycreatedfi = f"🇫🇮 <br> Uusi solidaarisuuspyyntö on luotu hashtagilla: '{solidaryhast}'."
                solidarycreated = (solidarycreateden + "<br> --- <br>" + solidarycreatedfi)
                await send_text_to_room(self.client, self.room.room_id, solidarycreated)
                await self.client.room_create(
                name=solidaryhast,
                topic=("Täällä ovat kaikki jotka ovat lahjoittaneet " + solidaryhast + "tiin"),
                initial_state=[EnableEncryptionBuilder().as_dict()],
            )
    async def _solidary_requests(self):
        sa = "False"
        results = self.store.cursor.execute("""
            select * from solidary where private = ?;
        """, (sa,))
        results2 = results.fetchall()
        result_text = ("Avaible solidary requests <br>" + str(results2))
        await send_text_to_room(self.client, self.room.room_id, result_text)

        
    async def _solidary_donate(self):
        donateamount = self.args[0]
        donatehash = self.args[1]
        donateuser = self.args[2]
        if donatehash.startswith("@"):
            await send_text_to_room(self.client, self.room.room_id, "PLEASE TRY AGAIN")
        elif donatehash.startswith("#"):
            results = self.store.cursor.execute("""
                select sum from solidary where hashtag = ?;
            """, (donatehash,))
            #results1 = self.store.cursor.execute("""
                #select maxsum from solidary where hashtag = ?;
            #""", (donatehash,))
            cat = results.fetchone()
            catamount = (" " + str(cat) + " " + donateamount + " " + donatehash)
            await send_text_to_room(self.client, "!XSGosuFCQFOqWfLMoC:elokapina.fi", catamount)
            
            #self.store.cursor.execute("""
                #update solidary set sum = ? where hashtag = ?;
            #""", (newsum, donatehash))
            #self.store.conn.commit()
        elif donateamount.startswith("#"):
            await send_text_to_room(self.client, self.room.room_id, "cat")
            results = self.store.cursor.execute("""
                select sum from solidary where hashtag = ?;
            """, (donatehash,))
            cadf = results.fetchone()
            await send_text_to_room(self.client, self.room.room_id, cadf)

    async def donatefinalamount(self):
        finalamount = self.args[0]
        finalhast = self.args[1]
        self.store.cursor.execute("""
            update solidary set sum = ? where hashtag = ?;
        """, (finalamount, finalhast))
        self.store.conn.commit()
        results = self.store.cursor.execute("""
            select sum from solidary where hashtag = ?;
        """, (finalhast,))
        finalamounttest = results.fetchone()
        finalamounttest = (str(finalamounttest))
        await send_text_to_room(self.client, self.room.room_id, finalamounttest)
        

    async def _unknown_command(self):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        )
