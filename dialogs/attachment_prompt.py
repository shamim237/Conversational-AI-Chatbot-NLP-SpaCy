from typing import Callable, Dict
from botbuilder.schema import ActivityTypes
from botbuilder.core import TurnContext
from botbuilder.dialogs.prompts import Prompt, PromptValidatorContext
from botbuilder.dialogs.prompts import PromptOptions
from botbuilder.dialogs.prompts  import PromptRecognizerResult


class AttachmentPrompt(Prompt):
    """
    Prompts a user to upload attachments like images.

    By default the prompt will return to the calling dialog an `[Attachment]`
    """

    def __init__(
        self, dialog_id: str, validator: Callable[[PromptValidatorContext], bool] = None
    ):
        super().__init__(dialog_id, validator)

    async def on_prompt(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
        is_retry: bool,
    ):

        if not turn_context:
            raise TypeError("AttachmentPrompt.on_prompt(): TurnContext cannot be None.")
            

        if not isinstance(options, PromptOptions):
            raise TypeError(
                "AttachmentPrompt.on_prompt(): PromptOptions are required for Attachment Prompt dialogs.")

        if is_retry and options.retry_prompt:
            await turn_context.send_activity(options.retry_prompt)
        elif options.prompt:
            await turn_context.send_activity(options.prompt)

    async def on_recognize(
        self,
        turn_context: TurnContext,
        state: Dict[str, object],
        options: PromptOptions,
    ) -> PromptRecognizerResult:


        if not turn_context:
            raise TypeError("AttachmentPrompt.on_recognize(): context cannot be None.")

        result = PromptRecognizerResult()

        if turn_context.activity.type == ActivityTypes.message:
            message = turn_context.activity
            if "attachmentUrl" and "attachmentId" in message.additional_properties.keys():  
                result.succeeded = True
                result.value = message.additional_properties

        return result
