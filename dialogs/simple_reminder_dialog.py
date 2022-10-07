from lib.message_factory import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from prompt.email_prompt import EmailPrompt
from date_regex import cal_date_adv, cal_date_by_day
from adv_pill_reminder import save_reminder_spec_days_multi_time
import recognizers_suite as Recognizers
from recognizers_suite import Culture 
import gspread
from lib.card import CardAction
from botbuilder.schema import ActionTypes, SuggestedActions


class SimplePillReminderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "pill-reminder"):
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
        global main
        global wks
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        main = step_context.context.activity.text

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("What is the name of the medicine?", extra = main)),) 


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global med_name
        med_name = step_context.result

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

            return await step_context.prompt(
                "time_prompt",
                PromptOptions(prompt=MessageFactory.text("At what time would you like me to remind you to take the medicine? Ex: 6 AM.", extra = main)),)  


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:  

        global times
        global med_name

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

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

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How long do you have to take this medicine? Ex: 7 days or 2 weeks or 3 months.", extra = main)),) 


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        global med_name
        global times

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

            duration  = step_context.result  
            
            reply = MessageFactory.text("How often you would like to take the medicine? Will it be daily or only for some specific days?", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Daily",
                        type=ActionTypes.im_back,
                        value= "Daily",
                        extra = main),
                    CardAction(
                        title= "Specific Days",
                        type=ActionTypes.im_back,
                        value= "Specific Days",
                        extra = main),])
            return await step_context.context.send_activity(reply) 

    
    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global duration
        global med_name
        global times
        global med_type1
        global spec

        med_type1 = "14afafa"
        spec      = "atatata"  

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

            opt = step_context.result

            if opt == "Daily":
                med_type1 = "type nite hobe1"
                reply = MessageFactory.text("Please help me to recognize the type of medicine.", extra = main)
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
                    PromptOptions(prompt=MessageFactory.text("Please enter those days on which you want to take the medicine. Ex: Saturday or Monday or Friday.", extra = main)),)            


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        global med_name
        global times
        global dosages
        global days
        global med_type2

        dosages     = "atatatat"
        days        = "aa7aa77a"
        med_type2   = "a5a5a5a5"

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:


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
                reply = MessageFactory.text("Please help me to recognize the type of medicine.", extra = main)
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


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global duration
        global med_name
        global times
        global days
        global dropfor1
        global dosage1
        global dosages2

        dosages2 = "aerara"
        dropfor1 = "aratata"
        dosage1  = "awanana"
        
        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")


        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
    
                    return await step_context.end_dialog()
            

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
                            extra= main),
                        CardAction(
                            title= "Nose",
                            type=ActionTypes.im_back,
                            value= "Nose",
                            extra= main),
                        CardAction(
                            title= "Ear",
                            type=ActionTypes.im_back,
                            value= "Ear",
                            extra= main),
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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")


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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                if len(times) == 2:
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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing") 



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



    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 
        
        global duration
        global med_name
        global times
        global days
        global dropfor2
        global dosage2

        dropfor2 = "aratata"
        dosage2  = "awanana"

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage1) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")

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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")

        


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
                            extra= main),
                        CardAction(
                            title= "Nose",
                            type=ActionTypes.im_back,
                            value= "Nose",
                            extra= main),
                        CardAction(
                            title= "Ear",
                            type=ActionTypes.im_back,
                            value= "Ear",
                            extra= main),
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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")


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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))
                    return await step_context.replace_dialog("passing")
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")


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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))

                    return await step_context.replace_dialog("passing")


    async def ninth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        global med_name
        global times
        global days

        switch = predict_class(step_context.context.activity.text)

        if switch == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me check the earliest appointment slots for you.", extra = main))
            return await step_context.begin_dialog("early-book")

        if switch == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("pill-reminder")

        if switch == "health_profile":
            return await step_context.begin_dialog("health-profile")

        if switch == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text(f"Let me set a pill reminder for you.", extra = main))
            return await step_context.begin_dialog("adv-reminder")

        if switch == "adv_health_record":
            return await step_context.begin_dialog("adv-record")

        if switch == "adv_appointment":
            return await step_context.begin_dialog("spacy-book")

        if switch == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if switch == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")

        else:

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
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                if len(times) == 1:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " at " + str(times[0])+ " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                if len(times) == 2:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " at " + str(times[0]) + " and " + str(times[1]) + " for " + str(duration) + ".", extra = main))

                    return await step_context.end_dialog()
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take " + str(dosage2) + " dose of " + str(pill_name) + " for " + str(duration) + ".", extra = main))
                    return await step_context.replace_dialog("passing")        
        