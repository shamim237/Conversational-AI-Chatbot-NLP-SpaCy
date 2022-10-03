# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState
from botbuilder.schema import ChannelAccount
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
import time

class DialogBot(ActivityHandler):
    """
    This Bot implementation can run any type of Dialog. The use of type parameterization is to allows multiple
    different bots to be run at different endpoints within the same project. This can be achieved by defining distinct
    Controller types each with dependency on distinct Bot types. The ConversationState is used by the Dialog system. The
    UserState isn't, however, it might have been used in a Dialog implementation, and the requirement is that all
    BotState objects are saved at the end of a turn.
    """

    def __init__(self, expire_after_seconds: int, conversation_state: ConversationState, user_state: UserState, dialog: Dialog,):
        
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given")
        if user_state is None:
            raise TypeError("[DialogBot]: Missing parameter. user_state is required but None was given")
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.expire_after_seconds = expire_after_seconds
        self.conversation_state = conversation_state
        self.dialog_state_property = conversation_state.create_property("DialogState")
        self.last_accessed_time_property = conversation_state.create_property("LastAccessedTime")
        self.user_state = user_state
        self.dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        # Retrieve the property value, and compare it to the current time.
        now_seconds = int(time.time())
        last_access = int(
            await self.last_accessed_time_property.get(turn_context, now_seconds)
        )
        if now_seconds != last_access and (
            now_seconds - last_access >= self.expire_after_seconds
        ):
            # Notify the user that the conversation is being restarted.
            await turn_context.send_activity(
                "Welcome back!  Let's start over from the beginning."
            )

            # Clear state.
            await self.conversation_state.clear_state(turn_context)
            await self.conversation_state.save_changes(turn_context, True)

        await super().on_turn(turn_context)

        await self.last_accessed_time_property.set(turn_context, now_seconds)
        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_members_added_activity(self, members_added: ChannelAccount, turn_context: TurnContext):
        
        """
        Greet when users are added to the conversation.
        Note that all channels do not send the conversation update activity.
        If you find that this bot works in the emulator, but does not in
        another channel the reason is most likely that the channel does not
        send this activity.
        """

        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                    await turn_context.send_activity("Hello, Welcome to Jarvis Care!")
                    await turn_context.send_activity("I am Jarvis. How can I help you?")



    async def on_message_activity(self, turn_context: TurnContext):

        await DialogHelper.run_dialog(self.dialog, turn_context, self.dialog_state_property,)
