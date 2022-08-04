from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from adv_pill_reminder import save_reminder_spec_days
from nlp_model.pill_predict import reminder_class
import gspread
from word2number import w2n
from date_regex import cal_date_adv
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions


class AdvPillReminderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(AdvPillReminderDialog, self).__init__(dialog_id or AdvPillReminderDialog.__name__)

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
                    self.thrd_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global type_med
        global time_med
        global date_med
        global not_med
        global med_names
        global times
        global periods
        global durations
        global med_types
        global start_dates
        global end_dates
        global u_times
        global quants
        global multi_doses

        type_med = "jjsdfujnfs"
        time_med = "jadfaffgbd"
        date_med = "jhsmsi9rki"
        not_med = "dmmdmdofimg"
        
        global userId
        global token
        global pharmacyId
        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
        sh = ac.open("logs_checker")
        wks = sh.worksheet("Sheet1")
        main = wks.acell("A2").value
        wks.update_acell("E1", main)

        pred = reminder_class(main)

        try:
            wks.update_acell("F1", main)
            wks.update_acell("E2", str(pred))
        except:
            pass

        classes = []
        med_names = []
        times = []
        periods = []
        durations = []
        med_types = []
        start_dates = []
        end_dates = []
        u_times = []
        quants = []
        multi_doses = []


        for x in pred.keys():
            if x == "MED_NAME":
                med_name = pred[x]
                med_names.append(med_name)
                classes.append(x)
            if x == "TIME":
                time = pred[x]
                times.append(time)
                classes.append(x)
            if x == "PERIOD":
                period = pred[x]
                periods.append(period)
                classes.append(x)
            if x == "DURATION":
                duration = pred[x]
                durations.append(duration)
                classes.append(x)
            if x == "U_TIME":
                u_time = pred[x]
                u_times.append(u_time)
                classes.append(x)
            if x == "QUANT":
                quant = pred[x]
                quants.append(quant)
                classes.append(x)
            if x == "MED_TYPE":
                med_type = pred[x]
                med_types.append(med_type)
                classes.append(x)
            if x == "START_DATE":
                start_date = pred[x]
                start_dates.append(start_date)
                classes.append(x)
            if x == "END_DATE":
                end_date = pred[x]
                end_dates.append(end_date)
                classes.append(x)
            if x == "MULTI_DOSE":
                multi_dose = pred[x]
                multi_doses.append(multi_dose)
                classes.append(x)
        
        #remind me to take napa.
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes\
            and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            type_med = "just name is here-med_type needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time of the day would you like to take the medicine?")),)
        
        #remind me to take Sapa at 4pm.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes\
            and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            type_med = "just name nand time is here-med_type needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How often you would like to take the medicine? Will it be for daily or only for some specific days?")),)
        
        #remind me to take Maxpro 50mg at morning.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes\
            and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            type_med = "just name nand time and u_time is here-med_type needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?")),)

        #remind me to take Fexo daily at 4pm.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes\
            and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            date_med = "just name,time and period is here-med_date needs to be added"
            reply = MessageFactory.text("Please help me recognize the type of medicine-")
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

        
        #remind me to take napa everyday at night.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes\
            and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            time_med = "just name,u_time and period is here-med_time needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?")),)

        #remind me to take napa daily at 4pm for three weeks.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes\
            and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            not_med = "just name,time,period and duration is here-med_not needs to be added"
            reply = MessageFactory.text("Please help me recognize the type of medicine-")
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

        
        #remind me to take napa daily at morning for two weeks.
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes\
            and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            time_med = "just name,u_time,period and duration is here-med_time needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?")),)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global dosage
        dosage = "sivnisvi"

        if type_med == "just name is here-med_type needs to be added" or type_med == "just name nand time is here-med_type needs to be added" or\
            type_med == "just name nand time and u_time is here-med_type needs to be added":

            reply = MessageFactory.text("Please help me recognize the type of medicine-")
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

        if date_med == "just name,time and period is here-med_date needs to be added": 

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How many days you need to take the medicines? Hint- 2 weeks/three months.")),)

        if time_med == "just name,u_time and period is here-med_time needs to be added" or time_med == "just name,u_time,period and duration is here-med_time needs to be added":
                
            reply = MessageFactory.text("Please help me recognize the type of medicine-")
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

        #remind me to take napa daily at 4pm for three weeks.
        if not_med == "just name,time,period and duration is here-med_not needs to be added": 
            med_type = step_context.result

            if med_type == "Tablet":
                dosage = "koto dosage"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if med_type in "Drop":
                med_type = "1"

            if med_type in "Capsule":
                med_type = "2"

            if med_type in "Syringe":
                med_type = "3"

            if med_type in "Syrup":
                med_type = "4"


    async def thrd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if dosage == "koto dosage":
            dosage = step_context.result
            try:
                dosage = w2n.word_to_num(dosage)
            except:
                dosage = 1
            med_type = "0"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = times[0] 


            dates = cal_date_adv(durations[0])

            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage)   
            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ "."))
            return await step_context.end_dialog()

            





        


                 
        
       

           

        

        

