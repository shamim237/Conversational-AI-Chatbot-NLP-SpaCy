from botbuilder.dialogs.prompts import Prompt, PromptOptions,PromptRecognizerResult
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes
from recognizers_text import Culture
from recognizers_date_time import DateTimeRecognizer 
import recognizers_suite as Recognizers
from recognizers_suite import Culture
from typing import  Dict
culture = Culture.English

class TimePrompt (Prompt):
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

    async def on_recognize(self, turn_context: TurnContext,  state: Dict[str, object], options: PromptOptions,) -> PromptRecognizerResult:  

        if not turn_context:
            raise TypeError("turn_context cannt be none")

        if turn_context.activity.type == ActivityTypes.message:
            usertext = turn_context.activity.text


        extract = Recognizers.recognize_datetime(usertext, culture) 
        times = []     
        for i in extract:
            keys = i.resolution
            values = keys['values']
            for j in values:
                timea = j['value']  
                times.append(timea)  

        times = ",".join(times)
        turn_context.activity.locale = self._defaultLocale
        recognizer = DateTimeRecognizer(Culture.English)
        model = recognizer.get_datetime_model()
        mode_result = model.parse(times)

        prompt_result = PromptRecognizerResult()

        if len(mode_result) > 0 and len(mode_result[0].resolution) > 0:
            for resolution in mode_result[0].resolution["values"]:
                if "value" in resolution:
                    prompt_result.value = resolution["value"]
                    prompt_result.succeeded = True
                    return prompt_result


