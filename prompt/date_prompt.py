from botbuilder.dialogs.prompts import Prompt, PromptOptions,PromptRecognizerResult
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes
from datetime import datetime
from recognizers_date_time import DateTimeRecognizer 
import recognizers_suite as Recognizers
from recognizers_suite import Culture
import gspread
from typing import Dict
culture = Culture.English


class DatePrompt (Prompt):
    def __init__(self, dialog_id, validator : object = None, defaultLocale = None):
     super().__init__(dialog_id, validator=validator)
     
     if defaultLocale is None:
        defaultLocale = Culture.English
     self._defaultLocale = defaultLocale

    async def on_prompt(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions, is_retry: bool,):
        if not turn_context:
            raise TypeError("turn_context Can’t  be none")
        if not options:
            raise TypeError("options Can’t  be none")

        if is_retry and options.retry_prompt is not None:
            await turn_context.send_activity(options.retry_prompt)
        else:
            if options.prompt is not None:
                await turn_context.send_activity(options.prompt)    

    async def on_recognize(self, turn_context: TurnContext, state: Dict[str, object], options: PromptOptions,) -> PromptRecognizerResult: 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        if not turn_context:
            raise TypeError("turn_context cannt be none")

        if turn_context.activity.type == ActivityTypes.message:
            usertext = turn_context.activity.text

        today = datetime.now()
        today = datetime.strftime(today, "%Y-%m-%d")   
        today = datetime.strptime(today, "%Y-%m-%d").date()

        raw = Recognizers.recognize_datetime(usertext, culture) 
        dates = []     
        for i in raw:
            raw = i.resolution
            dd = raw['values']
            for j in dd:
                tim = j['value']  
                dates.append(tim) 
        datess = []
        for i in dates:
            datey = datetime.strptime(i, "%Y-%m-%d").date()
            if datey >= today:
                datess.append(i)
            else:
                pass

        datek = ",".join(datess)
            
        turn_context.activity.locale = self._defaultLocale

        recognizer = DateTimeRecognizer(Culture.English)
        model = recognizer.get_datetime_model()
        mode_result = model.parse(datek)


        wks.update_acell("F10", str(datek))
        wks.update_acell("F11", str(mode_result[0].resolution))
        wks.update_acell("F12", str(today))

        prompt_result = PromptRecognizerResult()

        if len(mode_result) > 0 and len(mode_result[0].resolution) > 0:
            for resolution in mode_result[0].resolution["values"]:
                if "value" in resolution:
                    prompt_result.value = resolution["value"]
                    if prompt_result.value < datetime.today().strftime("%Y-%m-%d"):
                        wks.update_acell("F13", str("entered-False"))
                        prompt_result.succeeded = False
                        return prompt_result
                    else:
                        wks.update_acell("F14", str("entered-True"))
                        prompt_result.succeeded = True
                        return prompt_result
