import gspread
from word2number import w2n
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from botbuilder.core import MessageFactory
from prompt.email_prompt import EmailPrompt
from nlp_model.pill_predict import reminder_class
from adv_pill_reminder import save_reminder_spec_days
from date_regex import cal_date_stend
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions


####################################################   remind me to take 10ml Benadryl from tomorrow  #################################################################

class caseThreeDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseThreeDialog, self).__init__(dialog_id or caseThreeDialog.__name__)

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
                    self.fifth_step,

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
        
        global start_dates
        global med_names
        global quants

        classes     = []
        med_names   = []
        quants      = []
        start_dates = []


        for x in pred.keys():

            if x == "MED_NAME":
                med_name = pred[x]
                med_names.append(med_name)
                classes.append(x)

            if x == "QUANT":
                quant = pred[x]
                quants.append(quant)
                classes.append(x)

            if x == "START_DATE":
                start_date = pred[x]
                start_dates.append(start_date)
                classes.append(x)

        return await step_context.prompt(
            "time_prompt",
            PromptOptions(prompt=MessageFactory.text("At what time do you need to take the medicine?")),)            
        


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global time
        time = step_context.result
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("How long do you want to take the medicine? Hints- 7 days/ 2 weeks/ 3 months.")),) 


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        duration = step_context.result

        reply = MessageFactory.text("Please help me to recognize the type of medicine-")
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title= "Tablet",
                    type=ActionTypes.im_back,
                    value= "Tablet"),
                CardAction(
                    title= "Drop",
                    type=ActionTypes.im_back,
                    value= "Drop"),
                CardAction(
                    title= "Capsule",
                    type=ActionTypes.im_back,
                    value= "Capsule"),
                CardAction(
                    title= "Syringe",
                    type=ActionTypes.im_back,
                    value= "Syringe"),
                CardAction(
                    title= "Syrup",
                    type=ActionTypes.im_back,
                    value= "Syrup"),])
        return await step_context.context.send_activity(reply)


    
    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        global duration

        typeo = step_context.result

        if typeo == "Tablet":
            dosage = quants[0]
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            
            try:
                dosage = w2n.word_to_num(dosage)
            except:
                dosage = 1

            med_type = "0"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = "#DB4F64"
            pill_time = time
            shape_type = "0"
            place = ""
            dosage_ml = ""
            duration = str(duration)
            duration = duration.lower()
            duration = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
            dates = cal_date_stend(start_dates[0], duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog() 


        global dropfor1
        global dosage1
        dropfor1 = "auauauau"
        dosage1  = "sissiiss"   

        if typeo == "Drop":
            dropfor1 = "drop kothay"
            dosage = quants[0]
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("drops", "").replace("drop ", "")

            try:
                dosage1 = w2n.word_to_num(dosage)
            except:
                dosage1 = 1

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


        if typeo == "Capsule":
            dosage      = quants[0]
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            try:
                dosage  = w2n.word_to_num(dosage)
            except:
                dosage  = 1
            med_type    = "2"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = time 
            shape_type  = "-1"
            place       = ""
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_stend(start_dates[0], duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog() 

        wks.update_acell("G1", str(duration))

        if typeo == "Syringe":
            wks.update_acell("G2", "entered")
            dosage       = quants[0]
            wks.update_acell("G3", str(dosage))
            dosage       = str(dosage)
            dosage       = dosage.lower()
            dosage       = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml= w2n.word_to_num(dosage)
            except:
                dosage_ml= 1
            wks.update_acell("G4", str(dosage))
            med_type    = "3"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = time
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            wks.update_acell("G5", str(pill_name))
            wks.update_acell("G6", str(duration))
            wks.update_acell("G7", str(start_dates[0]))
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            wks.update_acell("G8", str(duration))
            dates       = cal_date_stend(start_dates[0], duration)
            wks.update_acell("G9", str(dates))
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog()  

        if typeo == "Syrup":
            dosage = quants[0]
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml = w2n.word_to_num(dosage)
            except:
                dosage_ml = 1
            med_type    = "4"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = time
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_stend(start_dates[0], duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog() 


            
    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if dropfor1 == "drop kothay":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            pill_time   = time
            color_code  = ""
            shape_type  = "-1"
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_stend(start_dates[0], duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage1, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage1) + " drops of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog()
