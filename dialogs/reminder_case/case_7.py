import gspread
from prompt.date_prompt import DatePrompt
import recognizers_suite as Recognizers
from recognizers_suite import Culture 
from prompt.time_prompt import TimePrompt
from lib.message_factory import MessageFactory
from lib.card import CardAction
from prompt.email_prompt import EmailPrompt
from nlp_model.pill_predict import reminder_class
from adv_pill_reminder import  save_reminder_spec_days_multi_time
from date_regex import cal_date_adv, cal_date_by_day
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions


####################################################   remind me to take Sapa   #################################################################

class caseSevenDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseSevenDialog, self).__init__(dialog_id or caseSevenDialog.__name__)

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
                    self.sixth_step,
                    self.seventh_step,
                    self.eighth_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global token
        global userId
        global wks
        global main
        global med_names
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        
        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        main = step_context.context.activity.text
        wks.update_acell("R1", str(main))    
        pred = reminder_class(main)
        
        
        classes = []
        med_names = []


        for x in pred.keys():
            if x == "MED_NAME":
                med_name = pred[x]
                med_names.append(med_name)
                classes.append(x)

   
        #remind me to take Sapa
        return await step_context.prompt(
            "time_prompt",
            PromptOptions(prompt=MessageFactory.text("At what time would you like me to remind you to take the medicine? Hint- 6 AM.", extra = main)),)  


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global times

        time = step_context.result
        culture = Culture.English
        raw = Recognizers.recognize_datetime(str(time), culture) 
        times = []     
        for i in raw:
            raw = i.resolution
            dd = raw['values']
            for j in dd:
                tim = j['value']  
                times.append(tim)     

        wks.update_acell("C15", str("".join(times)))

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("How many days do you have to take this medicine? Hint- 7 days/2 weeks/3 months.", extra = main)),) 


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:  

        global duration
        global times
        duration  = step_context.result  
        
        reply = MessageFactory.text("How often you would like to take the medicine? Will it be for daily or only for some specific days?", extra = main)
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title= "Daily",
                    type=ActionTypes.im_back,
                    value= "Daily",
                    extra= main),
                CardAction(
                    title= "Specific Days",
                    type=ActionTypes.im_back,
                    value= "Specific Days",
                    extra= main),])
        return await step_context.context.send_activity(reply) 


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        global times
        global med_type1
        global spec

        med_type1 = "14afafa"
        spec      = "atatata"  

        opt = step_context.result

        if opt == "Daily":
            med_type1 = "type nite hobe1"
            reply = MessageFactory.text("Please help me to recognize the type of medicine-", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Tablet",
                        type=ActionTypes.im_back,
                        value= "Tablet",
                        extra = main),
                    CardAction(
                        title= "Drop",
                        type=ActionTypes.im_back,
                        value= "Drop",
                        extra = main),
                    CardAction(
                        title= "Capsule",
                        type=ActionTypes.im_back,
                        value= "Capsule",
                        extra = main),
                    CardAction(
                        title= "Syringe",
                        type=ActionTypes.im_back,
                        value= "Syringe",
                        extra = main),
                    CardAction(
                        title= "Syrup",
                        type=ActionTypes.im_back,
                        value= "Syrup",
                        extra = main),])
            return await step_context.context.send_activity(reply)


        if opt == "Specific Days":
            spec = "specific days nite chaise"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please enter those days on which you want to take the medicine. Hint- Saturday/Monday/Friday.", extra = main)),)  


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global duration
        global times
        global dosages
        global days
        global med_type2

        dosages     = "atatatat"
        days        = "aa7aa77a"
        med_type2   = "a5a5a5a5"


        if med_type1 == "type nite hobe1":
            types = step_context.result

            if types == "Tablet":
                dosages = "tablet dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if types == "Drop":
                dosages = "drop dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if types == "Capsule":
                dosages = "capsule dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)

            if types == "Syringe":
                dosages = "syringe dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?", extra = main)),)

            if types == "Syrup":
                dosages = "syrup dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?", extra = main)),)


        if spec == "specific days nite chaise":
            days = step_context.result
            med_type2 = "type nite hobe2"
            reply = MessageFactory.text("Please help me to recognize the type of medicine-", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Tablet",
                        type=ActionTypes.im_back,
                        value= "Tablet",
                        extra = main),
                    CardAction(
                        title= "Drop",
                        type=ActionTypes.im_back,
                        value= "Drop",
                        extra = main),
                    CardAction(
                        title= "Capsule",
                        type=ActionTypes.im_back,
                        value= "Capsule",
                        extra = main),
                    CardAction(
                        title= "Syringe",
                        type=ActionTypes.im_back,
                        value= "Syringe",
                        extra = main),
                    CardAction(
                        title= "Syrup",
                        type=ActionTypes.im_back,
                        value= "Syrup",
                        extra = main),])
            return await step_context.context.send_activity(reply)
 


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        global times

        wks.update_acell("C1", str(dosages))
        wks.update_acell("C2", str(duration))
        wks.update_acell("C3", str(med_names[0]))
        wks.update_acell("C4", str("".join(times)))
        wks.update_acell("C5", "entered")

        if dosages == "tablet dose":
            wks.update_acell("C6", "entered")
            dosage      = step_context.result
            wks.update_acell("C7", str(dosage))
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            med_type    = "0"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = "#DB4F64"
            wks.update_acell("C8", "enetered")
            pill_time   = times
            shape_type  = "0"
            place       = ""
            dosage_ml   = ""
            wks.update_acell("C9", "enetered1")
            duration    = str(duration)
            wks.update_acell("C10", str(duration))
            duration    = duration.lower()
            duration    = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
            dates       = cal_date_adv(duration)
            wks.update_acell("C11", "enetered2")
            wks.update_acell("C12", str("".join(dates)))
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
        
        
        global dropfor1
        global dosage1

        dropfor1 = "aratata"
        dosage1  = "awanana"

        if dosages == "drop dose":  
            dropfor1    = "drop kothay"
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage1     = dosage.replace("drops", "").replace("drop ", "")

            reply = MessageFactory.text("Where to use the drop?", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Eye",
                        type=ActionTypes.im_back,
                        value= "Eye",
                        extra = main),
                    CardAction(
                        title= "Nose",
                        type=ActionTypes.im_back,
                        value= "Nose",
                        extra = main),
                    CardAction(
                        title= "Ear",
                        type=ActionTypes.im_back,
                        value= "Ear",
                        extra = main),
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
            pill_time   = times
            shape_type  = "-1"
            place       = ""
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_adv(duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog()  


        if dosages == "syringe dose": 
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("mL", "").replace("ml", "")
            med_type    = "3"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = times
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_adv(duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
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
            pill_time   = times
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_adv(duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog()  

        global dosages2
        dosages2 = "aerara"

        if med_type2 == "type nite hobe2":
            types2 = step_context.result

            if types2 == "Tablet":
                dosages2 = "tablet dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if types2 == "Drop":
                dosages2 = "drop dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if types2 == "Capsule":
                dosages2 = "capsule dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)

            if types2 == "Syringe":
                dosages2 = "syringe dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?", extra = main)),)

            if types2 == "Syrup":
                dosages2 = "syrup dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?", extra = main)),)


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 


        if dropfor1 == "drop kothay":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            pill_time   = times
            color_code  = ""
            shape_type  = "-1"
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_adv(duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage1, color_code, shape_type, place, dosage_ml)    
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 


        if dosages2 == "tablet dose2":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            med_type    = "0"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = "#DB4F64"
            pill_time   = times
            shape_type  = "0"
            place       = ""
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
            dates       = cal_date_by_day(days, duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 

        
        global dropfor2
        global dosage2

        dropfor2 = "aratata"
        dosage2  = "awanana"

        if dosages2 == "drop dose2":  
            dropfor2    = "drop kothay2"
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage2     = dosage.replace("drops", "").replace("drop ", "")

            reply = MessageFactory.text("Where to use the drop?", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Eye",
                        type=ActionTypes.im_back,
                        value= "Eye",
                        extra = main),
                    CardAction(
                        title= "Nose",
                        type=ActionTypes.im_back,
                        value= "Nose",
                        extra = main),
                    CardAction(
                        title= "Ear",
                        type=ActionTypes.im_back,
                        value= "Ear",
                        extra = main),
                ])
            return await step_context.context.send_activity(reply)


        if dosages2 == "capsule dose2":    
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
            pill_time   = times
            shape_type  = "-1"
            place       = ""
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_by_day(days, duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog()  


        if dosages2 == "syringe dose2": 
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("mL", "").replace("ml", "")
            med_type    = "3"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            color_code  = ""
            pill_time   = times
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_by_day(days, duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog()  


        if dosages2 == "syrup dose2":
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
            pill_time   = times
            shape_type  = "-1"
            place       = ""
            dose        = "1"
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_by_day(days, duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog()  


    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        if dropfor2 == "drop kothay2":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            pill_time   = times
            color_code  = ""
            shape_type  = "-1"
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_by_day(days, duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage2, color_code, shape_type, place, dosage_ml)    
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            if len(pill_time) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            if len(pill_time) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                return await step_context.end_dialog()  