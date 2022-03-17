from re import I
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
        #elif self.command.startswith("room"):
            #await self.ridset()
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
                solidarycreateden = f"🇺🇸 <br> New solidary request created with hashtag: '{solidaryhast}'."
                solidarycreatedfi = f"🇫🇮 <br> Uusi solidaarisuuspyyntö on luotu hashtagilla: '{solidaryhast}'."
                solidarycreated = (solidarycreateden + "<br> --- <br>" + solidarycreatedfi)
                await send_text_to_room(self.client, self.room.room_id, solidarycreated)
                response = await self.client.room_create(
                name=solidaryhast,
                topic=("Täällä ovat kaikki jotka ovat lahjoittaneet " + solidaryhast + "tiin"),
                initial_state=[EnableEncryptionBuilder().as_dict()],
                )
                room_id = response.room_id
                logger.info(f"Breakout room created at {room_id}")
                solidaryroomid = room_id
                self.store.new_solidary(solidaryhast, solidarysum, solidarygo, solidaryroomid)
    async def _solidary_requests(self):
        sa = "False"
        hashtags = self.store.cursor.execute("""
            select hashtag from solidary where private = ?;
        """, (sa,))
        hashtag = hashtags.fetchall()
        hashtag = str(hashtag)
        hashtag1 = hashtag.replace("(", "")
        hashtag2 = hashtag1.replace(")", "<br>")
        hashtag3 = hashtag2.replace("'", "")
        hashtag4 = hashtag3.replace(",", "")
        hashtag5 = hashtag4.replace("[", "")
        hashtag6 = hashtag5.replace("]", "")
        result_text = ("Avaible solidary requests <br>" + str(hashtag6))
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
            ridre = self.store.cursor.execute("""
                select roomid from solidary where hashtag = ?;
            """, (donatehash,))
            cat = results.fetchone()
            rid = ridre.fetchone()
            logger.info(f"RID={rid}")
            ridi = str(rid)
            final_rid = ridi.replace("(", "")
            final1_rid = final_rid.replace(")", "")
            final2_rid = final1_rid.replace("'", "")
            final3_rid = final2_rid.replace(",", "")
            logger.info(f"final rid = {final3_rid}")
            await self.client.room_invite(final3_rid, donateuser)
            await self.donatefinalamount1(donatehash, donateamount)
        elif donateamount.startswith("#"):
            await send_text_to_room(self.client, self.room.room_id, "cat")
            results = self.store.cursor.execute("""
                select sum from solidary where hashtag = ?;
            """, (donatehash,))
            cadf = results.fetchone()
            await send_text_to_room(self.client, self.room.room_id, cadf)
    async def donatefinalamount1(self, donatehash: str, donateamount: int):
        results = self.store.cursor.execute("""
                select sum from solidary where hashtag = ?;
        """, (donatehash,))
        ridi = results.fetchone()
        da = str(ridi)
        final_amount_1 = da.replace("(", "")
        final_amount1 = final_amount_1.replace(")", "")
        final_amount2 = final_amount1.replace("'", "")
        final_amount3 = final_amount2.replace("'", "")
        final_amount4 = final_amount3.replace(",", "")
        final_amount = (int(final_amount4) + int(donateamount))
        logger.info(f"{final_amount}")
        self.store.cursor.execute("""
            update solidary set sum = ? where hashtag = ?;
        """, (final_amount, donatehash))
        self.store.conn.commit()
        await send_text_to_room(self.client, self.room.room_id, str(final_amount))

    

    async def _unknown_command(self):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        )
