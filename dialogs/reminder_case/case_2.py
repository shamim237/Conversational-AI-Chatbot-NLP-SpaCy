import gspread
from word2number import w2n
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from botbuilder.core import MessageFactory
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from nlp_model.pill_predict import reminder_class
from adv_pill_reminder import save_reminder_spec_days
from date_regex import cal_date_adv, cal_date_by_day, cal_day
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions


####################################################   #remind me to take Maxpro 50mg at morning.  #################################################################

class caseTwoDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseTwoDialog, self).__init__(dialog_id or caseTwoDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,
                    # self.scnd_step,
                    # self.third_step,
                    # self.fourth_step,
                    # self.fifth_step,
                    # self.sixth_step,
                    # self.seventh_step,
                    # self.eighth_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        
        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")


        main = step_context.context.activity.text
        wks.update_acell("R2", str(main))    
        pred = reminder_class(main)
        
        global med_names
        global u_times

        classes = []
        med_names = []
        u_times = []


        for x in pred.keys():
            if x == "MED_NAME":
                med_name = pred[x]
                med_names.append(med_name)
                classes.append(x)
            if x == "U_TIME":
                u_time = pred[x]
                u_times.append(u_time)
                classes.append(x)


        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?")),)