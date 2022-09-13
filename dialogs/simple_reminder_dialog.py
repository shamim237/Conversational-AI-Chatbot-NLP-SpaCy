from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from date_regex import cal_date_adv, cal_date_by_day
from adv_pill_reminder import save_reminder_spec_days_multi_time
import recognizers_suite as Recognizers
from recognizers_suite import Culture 
import gspread
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions


class SimplePillReminderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(SimplePillReminderDialog, self).__init__(dialog_id or SimplePillReminderDialog.__name__)

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
                    self.ninth_step,
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

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("What is the name of the medicine?")),) 


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global med_name
        med_name = step_context.result

        return await step_context.prompt(
            "time_prompt",
            PromptOptions(prompt=MessageFactory.text("At what time would you like me to remind you to take the medicine? Hint- 6 AM.")),)  


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:  

        global times

        time = step_context.result
        culture = Culture.English
        extract = Recognizers.recognize_datetime(time, culture) 
        times = []     
        for i in extract:
            keys = i.resolution
            values = keys['values']
            for j in values:
                timea = j['value']  
                times.append(timea)      

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("For how long you want to take the medicine? Hint- 7 days/2 weeks/3 months.")),) 


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        duration  = step_context.result  
        
        reply = MessageFactory.text("How often you would like to take the medicine? Will it be daily or only for some specific days?")
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title= "Daily",
                    type=ActionTypes.im_back,
                    value= "Daily"),
                CardAction(
                    title= "Specific Days",
                    type=ActionTypes.im_back,
                    value= "Specific Days"),])
        return await step_context.context.send_activity(reply) 

    
    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global med_type1
        global spec

        med_type1 = "14afafa"
        spec      = "atatata"  

        opt = step_context.result

        if opt == "Daily":
            med_type1 = "type nite hobe1"
            reply = MessageFactory.text("Please help me to recognize the type of medicine.")
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

        if opt == "Specific Days":
            spec = "specific days nite chaise"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please enter those days on which you want to take the medicine. Hint- Saturday/Monday/Friday.")),)            


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

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
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if types == "Drop":
                dosages = "drop dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)

            if types == "Capsule":
                dosages = "capsule dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?")),)

            if types == "Syringe":
                dosages = "syringe dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?")),)

            if types == "Syrup":
                dosages = "syrup dose"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?")),)


        if spec == "specific days nite chaise":
            days = step_context.result
            med_type2 = "type nite hobe2"
            reply = MessageFactory.text("Please help me to recognize the type of medicine.")
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


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        wks.update_acell("C1", str(dosages))
        wks.update_acell("C2", str(duration))
        wks.update_acell("C3", str(med_name))
        wks.update_acell("C4", str("".join(times)))
        wks.update_acell("C5", "entered")

        if dosages == "tablet dose":
            wks.update_acell("C6", "entered")
            dosage      = step_context.result
            wks.update_acell("C6", str(dosage))
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            med_type    = "0"
            pill_name   = med_name
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
            dates       = cal_date_adv(duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
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
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog()  


        if dosages == "syringe dose": 
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("mL", "").replace("ml", "")
            med_type    = "3"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog()  


        if dosages == "syrup dose":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("mL", "").replace("ml", "")
            med_type    = "4"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog()  

        global dosages2
        dosages2 = "aerara"

        if med_type2 == "type nite hobe2":
            types2 = step_context.result

            if types2 == "Tablet":
                dosages2 = "tablet dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if types2 == "Drop":
                dosages2 = "drop dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)

            if types2 == "Capsule":
                dosages2 = "capsule dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?")),)

            if types2 == "Syringe":
                dosages2 = "syringe dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?")),)

            if types2 == "Syrup":
                dosages2 = "syrup dose2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended by the doctor?")),)



    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        if dropfor1 == "drop kothay":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 


        if dosages2 == "tablet dose2":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            med_type    = "0"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
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


        if dosages2 == "capsule dose2":    
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage      = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            med_type    = "2"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog()  


        if dosages2 == "syringe dose2": 
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("mL", "").replace("ml", "")
            med_type    = "3"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog()  


        if dosages2 == "syrup dose2":
            dosage      = step_context.result
            dosage      = str(dosage)
            dosage      = dosage.lower()
            dosage_ml   = dosage.replace("mL", "").replace("ml", "")
            med_type    = "4"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog()  


    async def ninth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if dropfor2 == "drop kothay2":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_name
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
                MessageFactory.text(f"Your pill reminder has been set."))
            if len(times) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            if len(times) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + "."))
                return await step_context.end_dialog() 
            else:
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " for " + str(duration) + "."))
                return await step_context.end_dialog()         
        