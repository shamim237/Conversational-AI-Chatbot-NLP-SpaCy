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


####################################################  set a pill reminder for bendix tablet daily at 9 pm for 6 months  #################################################################

class caseFiveDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseFiveDialog, self).__init__(dialog_id or caseFiveDialog.__name__)

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
                    self.scnd_step,
                    self.third_step,
                    self.fourth_step,
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

        main = step_context.context.activity.text
        pred = reminder_class(main)
        
        global med_names
        global med_types
        global periods
        global durations
        global times

        classes     = []
        med_names   = []
        times       = []
        med_types   = []
        periods     = []
        durations   = []

################################################################# set a pill reminder for bendix tablet daily at 9 pm ################################################################################
        
        for x in pred.keys():
            if x == "MED_NAME":
                med_name = pred[x]
                med_names.append(med_name)
                classes.append(x)
            if x == "TIME":
                time = pred[x]
                times.append(time)
                classes.append(x)
            if x == "MED_TYPE":
                med_type = pred[x]
                med_types.append(med_type)
                classes.append(x)
            if x == "PERIOD":
                period = pred[x]
                periods.append(period)
                classes.append(x)
            if x == "DURATION":
                duration = pred[x]
                durations.append(duration)
                classes.append(x)   


        global dosages
        dosages     = "siaiai3"

        tablet  = ["tablet", "tablets", "tabs", "tab."] 
        drop    = ["drops", "drop"]
        syrup   = ["syrup", "syrups"]
        syringe = ["syringe", "syringes", "injections", "injection"]
        caps    = ["capsules", "capsule", "caps", "cap."]
        types   = med_types[0]
        types   = str(types).lower()


        if types in tablet:
            dosages = "tablet dose"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)
        if types in drop:
            dosages = "drops dose" 
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)
        if types in caps:
            dosages = "capsule dose"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?")),)   
        if types in syringe:
            dosages = "syringe dose"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?")),)
        if types in syrup:
            dosages = "syrup dose"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?")),)                     



    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if dosages == "tablet dose":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            med_types   = "0"
            pill_name   = med_names[0]
            pill_time   = times[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = "#DB4F64"
            shape_type  = "0"
            place       = ""
            dosage_ml   = ""
            dates       = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_types, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()

        global dropfor1
        global dosage1

        dropfor1 = "8a8a8a"
        dosage1  = "8s88d8"      

        if dosages == "drops dose":
            dropfor1 = "drop kothay"
            dosage   = step_context.result
            dosage   = str(dosage)
            dosage   = dosage.lower()
            dosage1  = dosage.replace("drops", "").replace("drop ", "")

            reply = MessageFactory.text("Where to use the drop?")
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Eye",
                        type=ActionTypes.im_back,
                        value= "Eye"),
                    CardAction(
                        title= "Nose",
                        type=ActionTypes.im_back,
                        value= "Nose"),
                    CardAction(
                        title= "Ear",
                        type=ActionTypes.im_back,
                        value= "Ear"),
                ])
            return await step_context.context.send_activity(reply)


        if dosages == "capsule dose":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            med_type    = "2"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = times[0] 
            shape_type  = "-1"
            place       = ""
            dosage_ml   = ""
            dates       = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()


        if dosages == "syringe dose":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("ml", "").replace("mg", "")
            med_type    = "3"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = times[0]
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            dates       = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()


        if dosages == "syrup dose":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("mL", "").replace("ml", "")
            med_type    = "4"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = times[0]
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            dates       = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if dropfor1 == "drop kothay":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            pill_time   = times[0]
            color_code  = ""
            shape_type  = "-1"
            dosage_ml   = ""
            dates       = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage1, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()        
