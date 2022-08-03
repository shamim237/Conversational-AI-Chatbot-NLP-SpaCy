from botbuilder.dialogs.prompts import Prompt, PromptOptions,PromptRecognizerResult
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes
from recognizers_text import Culture
from recognizers_date_time import DateTimeRecognizer 
import datetime
import parsedatetime
import datetime
import dateparser
from typing import Dict


class DatePrompt (Prompt):
    def __init__(self, 
        dialog_id,
        validator : object = None,
        defaultLocale = None):
     super().__init__(dialog_id, validator=validator)
     
     if defaultLocale is None:
        defaultLocale = Culture.English

     self._defaultLocale = defaultLocale

    async def on_prompt(
        self, 
        turn_context: TurnContext, 
        state: Dict[str, object], 
        options: PromptOptions, 
        is_retry: bool, 
    ):
        if not turn_context:
            raise TypeError("turn_context Can’t  be none")
        if not options:
            raise TypeError("options Can’t  be none")

        if is_retry and options.retry_prompt is not None:
            await turn_context.send_activity(options.retry_prompt)
        else:
            if options.prompt is not None:
                await turn_context.send_activity(options.prompt)    

    async def on_recognize(self,
        turn_context: TurnContext, 
        state: Dict[str, object], 
        options: PromptOptions, 
    ) -> PromptRecognizerResult:  

        if not turn_context:
            raise TypeError("turn_context cannt be none")

        if turn_context.activity.type == ActivityTypes.message:
            usertext = turn_context.activity.text


        if "/" or "-" not in usertext:
            p = parsedatetime.Calendar()
            time_struct, parse_status = p.parse(usertext)
            dates = datetime.datetime(*time_struct[:6]).strftime("%Y-%m-%d")

            turn_context.activity.locale = self._defaultLocale

            recognizer = DateTimeRecognizer(Culture.English)
            model = recognizer.get_datetime_model()
            mode_result = model.parse(dates)

            prompt_result = PromptRecognizerResult()

            if len(mode_result) > 0 and len(mode_result[0].resolution) > 0:
                for resolution in mode_result[0].resolution["values"]:
                    if "value" in resolution:
                        #prompt_result.succeeded = True
                        prompt_result.value = resolution["value"]
                        print("Date: ", prompt_result.value)
                        if prompt_result.value < datetime.datetime.today().strftime("%Y-%m-%d"):
                            prompt_result.succeeded = False
                            return prompt_result
                        else:
                            prompt_result.succeeded = True
                            return prompt_result


        if "/" or "-" in usertext:

            dates = dateparser.parse(usertext)
            dates = datetime.datetime.strftime(dates, '%Y-%m-%d')
            turn_context.activity.locale = self._defaultLocale

            recognizer = DateTimeRecognizer(Culture.English)
            model = recognizer.get_datetime_model()
            mode_result = model.parse(dates)

            prompt_result = PromptRecognizerResult()

            if len(mode_result) > 0 and len(mode_result[0].resolution) > 0:
                for resolution in mode_result[0].resolution["values"]:
                    if "value" in resolution:
                        #prompt_result.succeeded = True
                        prompt_result.value = resolution["value"]
                        print("Date: ", prompt_result.value)
                        if prompt_result.value < datetime.datetime.today().strftime("%Y-%m-%d"):
                            prompt_result.succeeded = False
                            return prompt_result
                        else:
                            prompt_result.succeeded = True
                            return prompt_result
