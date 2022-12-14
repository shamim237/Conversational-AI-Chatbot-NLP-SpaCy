import gspread
import re
from lib.message_factory import MessageFactory
from lib.card import CardAction
import recognizers_suite as Recognizers
from recognizers_suite import Culture 
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from nlp_model.pill_predict import reminder_class
from adv_pill_reminder import save_reminder_spec_days
from date_regex import cal_date_adv, cal_date_by_day, cal_day
from botbuilder.schema import ActionTypes, SuggestedActions
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
            PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?", extra = main)),)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global times
        
        time = step_context.result
        time = str(time)
        
        culture = Culture.English
        times = [] 
        if "AM" in time or "PM" in time or "A.M" in time or "P.M" in time or "am" in time or "pm" in time or "a.m" in time or "p.m" in time:
            wks.update_acell("A29", "entered1")
            time = re.sub(r"(\d{1,10})\.(\d+)", r"\1:\2", time)
            wks.update_acell("A32", str(time))
            raw = Recognizers.recognize_datetime(str(time), culture)
            for i in raw:
                raw = i.resolution
                dd = raw['values']
                for j in dd:
                    tim = j['value']  
                    times.append(tim)     
        else: 
            wks.update_acell("A31", "entered2")
            time = re.sub(r"(\d{1,10})\.(\d+)", r"\1:\2", time)
            tt = str(time) + " in the " + str(u_times[0])
            wks.update_acell("A32", str(tt))
            raw = Recognizers.recognize_datetime(tt, culture)
            for i in raw:
                raw = i.resolution
                dd = raw['values']
                for j in dd:
                    tim = j['value']  
                    times.append(tim)      

        wks.update_acell("A30", str(times))

        reply = MessageFactory.text("How often you would like to take the medicine? Will it be for daily or only for some specific days?", extra = main)
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


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global daily 
        global specific
        global periodss

        daily    = "sainsvins"
        specific = "vsbvsbvos"
        periodss = "sivsivsiv"


        periodss = step_context.result

        if periodss == "Daily":
            daily = "daily nite chaise"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How long do you have to take this medicine? Ex: 7 days or 2 weeks or 3 months.", extra = main)),) 

        if periodss == "Specific Days":
            specific = "specific days nite chaise"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please enter those days on which you want to take the medicine. Ex: Saturday or Monday or Friday.", extra = main)),)        


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        global med_type
        global duras
        global dayss

        duration = "iwe8hj0s"
        med_type = "weuibwfw"
        duras    = "7fsabuus"
        dayss    = "ksnvsvns"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        

        if daily == "daily nite chaise":

            duration = step_context.result
            wks.update_acell("P1", str(duration))
            med_type = "type nite hobe"

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


        if specific == "specific days nite chaise":
            duras = "duration nite hbe"
            dayss = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Do you want to recurr (repeat) the reminder on the selected days?", extra = main)),) 


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        global duration
        global dayss
        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("P2", str(duration))

        global dosage_tab
        global dosage_cap
        global dosage_drop
        global dosage_inj
        global dosage_syrup

        dosage_tab   = "amsmamsm"
        dosage_cap   = "awmxdjnd"
        dosage_drop  = "sknkzvns"
        dosage_inj   = "eeevvass"
        dosage_syrup = "kjsnkjsn"


        if med_type == "type nite hobe":
            med_types = step_context.result
            if med_types == "Tablet":
                dosage_tab = "koto dosage11"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if med_types == "Drop":
                dosage_drop = "koto drop12"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if med_types == "Capsule":
                dosage_cap = "koto dosage13"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)

            if med_types == "Syringe":
                dosage_inj = "koto dosage14"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)

            if med_types == "Syrup":
                dosage_syrup = "koto dosage15"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)


        global med_types2
        global recurr_or_not

        recurr_or_not = "knsivnin"
        med_types2     = "osnnenon"

        if duras == "duration nite hbe":

            msg = predict_class(step_context.result)

            if msg == "positive":
                recurr_or_not = "asking"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How long do you have to take this medicine? Ex: 7 days or 2 weeks or 3 months.", extra = main)),)
            else:
                med_types2 = "type nite hobe2"
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
        global dayss
        global med_types3
        global duration2

        med_types3 = "asaiksk"
        duration2  = 'iaiaiai'

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("P3", str(duration))

        if dosage_tab == "koto dosage11":

            wks.update_acell("Q2", "entered")
            
            dosage = step_context.result
            wks.update_acell("Q3", str(dosage))
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            wks.update_acell("Q4", str(dosage))
            med_type = "0"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = "#DB4F64"
            pill_time = times[0]
            shape_type = "0"
            place = ""
            dosage_ml = ""
            wks.update_acell("Q5", str(pill_name))
            wks.update_acell("Q6", str(duration))
            duration = str(duration)
            duration = duration.lower()
            wks.update_acell("Q7", str(duration))
            duration = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
            wks.update_acell("Q8", "entered1")
            dates = cal_date_adv(duration)
            wks.update_acell("Q9", "entered2")
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            wks.update_acell("Q10", "entered3")
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + ".", extra = main))

            return await step_context.replace_dialog("passing")

        global dropfor1
        global dosage1

        dropfor1 = "dksbnkjs"
        dosage1  = "kjsnkjsn"

        if dosage_drop == "koto drop12":
            dropfor1 = "drop kothay"
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage1 = dosage.replace("drops", "").replace("drop ", "")
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

        if dosage_cap == "koto dosage13":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            med_type = "2"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0] 
            shape_type = "-1"
            place = ""
            dosage_ml = ""
            duration = str(duration)
            duration = duration.lower()
            duration = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_adv(duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + ".", extra = main))

            return await step_context.replace_dialog("passing") 

        if dosage_inj == "koto dosage14":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            med_type = "3"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]
            shape_type = "-1"
            place = ""
            dose = "1"
            duration = str(duration)
            duration = duration.lower()
            duration = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_adv(duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + ".", extra = main))

            return await step_context.replace_dialog("passing") 

        if dosage_syrup == "koto dosage15":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            med_type = "4"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]
            shape_type = "-1"
            place = ""
            dose = "1"
            duration = str(duration)
            duration = duration.lower()
            duration = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_adv(duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + ".", extra = main))

            return await step_context.replace_dialog("passing") 


        global dosage_tab_2
        global dosage_cap_2
        global dosage_drop_2
        global dosage_inj_2
        global dosage_syrup_2

        dosage_tab_2   = "amsmamsm"
        dosage_cap_2   = "awmxdjnd"
        dosage_drop_2  = "sknkzvns"
        dosage_inj_2   = "eeevvass"
        dosage_syrup_2 = "kjsnkjsn"


        if med_types2 == "type nite hobe2":
            med_type5I = step_context.result
            if med_type5I == "Tablet":
                dosage_tab_2 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if med_type5I == "Drop":
                dosage_drop_2 = "koto drop2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if med_type5I == "Capsule":
                dosage_cap_2 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)

            if med_type5I == "Syringe":
                dosage_inj_2 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)

            if med_type5I == "Syrup":
                dosage_syrup_2 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)


        if recurr_or_not == "asking":
            duration2 = step_context.result
            med_types3 = "type nite hobe3"

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



    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global duration
        global dayss
        global duration2

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        # wks.update_acell("P7", str(duration2))
        
        if dropfor1 == "drop kothay":
            place55 = step_context.result
            med_type = "1"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = times[0]
            color_code = ""
            shape_type = "-1"
            dosage_ml = ""
            duration = str(duration)
            duration = duration.lower()
            duration = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_adv(duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage1, color_code, shape_type, place55, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage1) + " drops of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + ".", extra = main))

            return await step_context.replace_dialog("passing")

        wks.update_acell("G10", str(dosage_drop_2))
        wks.update_acell("G11", str(dayss))

        if dosage_tab_2 == "koto dosage2":
            dosage = step_context.result
            wks.update_acell("G12", str(dosage))
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            wks.update_acell("G13", str(dosage))
            med_type = "0"
            pill_name = med_names[0]
            wks.update_acell("G13", str(pill_name))
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = "#DB4F64"
            pill_time = times[0]
            wks.update_acell("G13", str(pill_time))
            shape_type = "0"
            place = ""
            dosage_ml = ""
            dates = cal_day(dayss)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ ".", extra = main))

            return await step_context.replace_dialog("passing") 

        global dropfor2
        global dosage2

        dropfor2 = "dksbnkjs"
        dosage2  = "kjsnkjsn"

        wks.update_acell("F11", str(dosage_drop_2))

        if dosage_drop_2 == "koto drop2":
            dropfor2 = "drop kothay2"
            wks.update_acell("F12", "entered")
            dosage   = step_context.result
            wks.update_acell("F13", str(dosage))
            dosage   = str(dosage)
            dosage   = dosage.lower()
            dosage2   = dosage.replace("drops", "").replace("drop ", "")
            wks.update_acell("F14", str(dosage2))
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

        if dosage_cap_2 == "koto dosage2":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            med_type = "2"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0] 
            shape_type = "-1"
            place = ""
            dosage_ml = ""

            dates = cal_day(dayss)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+  ".", extra = main))

            return await step_context.replace_dialog("passing") 

        if dosage_inj_2 == "koto dosage2":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            med_type = "3"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_day(dayss)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time) + ".", extra = main))

            return await step_context.replace_dialog("passing")  

        if dosage_syrup_2 == "koto dosage2":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            med_type = "4"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_day(dayss)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time) + ".", extra = main))

            return await step_context.replace_dialog("passing")


        global dosage_tab_3
        global dosage_cap_3
        global dosage_drop_3
        global dosage_inj_3
        global dosage_syrup_3

        dosage_tab_3   = "amsmamsm"
        dosage_cap_3   = "awmxdjnd"
        dosage_drop_3  = "sknkzvns"
        dosage_inj_3   = "eeevvass"
        dosage_syrup_3 = "kjsnkjsn"


        if med_types3 == "type nite hobe3":
            med_type5I = step_context.result
            if med_type5I == "Tablet":
                dosage_tab_3 = "koto dosag3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if med_type5I == "Drop":
                dosage_drop_3 = "koto drop3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if med_type5I == "Capsule":
                dosage_cap_3 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)

            if med_type5I == "Syringe":
                dosage_inj_3 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)

            if med_type5I == "Syrup":
                dosage_syrup_3 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)


    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        # global duration2
        # global dayss

        # ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        # sh = ac.open("chatbot_logger")
        # wks = sh.worksheet("Sheet1")
        # # wks.update_acell("P8", str(duration2))
        # wks.update_acell("F23", str(dropfor2))
        # wks.update_acell("F24", str(dayss))

        if dropfor2 == "drop kothay2":
            wks.update_acell("F24", "eneterd#")
            place = step_context.result
            wks.update_acell("F25", str(place))
            med_type = "1"
            pill_name = med_names[0]
            wks.update_acell("F26", str(pill_name))
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = times[0]
            wks.update_acell("F27", str(pill_time))
            color_code = ""
            shape_type = "-1"
            dosage_ml = ""
            dates = cal_day(dayss)
            wks.update_acell("F28", str(dates))
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage2, color_code, shape_type, place, dosage_ml)
            wks.update_acell("F29", str(dates))
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage2) + " drops of " + str(pill_name) + " at " + str(pill_time) + ".", extra = main))

            return await step_context.replace_dialog("passing")

        global duration2

        wks.update_acell("F30", str(duration2))
        wks.update_acell("F31", str(dosage_tab_3))
        wks.update_acell("F32", str(dayss))

        if dosage_tab_3 == "koto dosag3":
            dosage = step_context.result
            wks.update_acell("F33", str(dosage))
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            wks.update_acell("F34", str(dosage))
            med_type = "0"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = "#DB4F64"
            pill_time = times[0]
            wks.update_acell("F35", str(pill_name))
            wks.update_acell("F36", str(pill_time))
            shape_type = "0"
            place = ""
            dosage_ml = ""
            wks.update_acell("F37", str(duration2))
            duration2 = str(duration2)
            duration2 = duration2.lower()
            duration2 = duration2.replace("for", "").replace("about", "").replace("almost", "")
            wks.update_acell("F38", str(duration2))
            dates = cal_date_by_day(dayss, duration2)
            wks.update_acell("F39", str(duration2))
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration2) + ".", extra = main))

            return await step_context.replace_dialog("passing")   


        global dropfor3
        global dosage3

        dropfor3 = "dksbnkjs"
        dosage3  = "kjsnkjsn"

        if dosage_drop_3 == "koto drop3": 
            dropfor3 = "drop kothay3"
            dosage   = step_context.result
            dosage   = str(dosage)
            dosage   = dosage.lower()
            dosage3   = dosage.replace("drops", "").replace("drop ", "")

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


        if dosage_cap_3 == "koto dosage3":      
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            med_type = "2"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0] 
            shape_type = "-1"
            place = ""
            dosage_ml = ""
            duration2 = str(duration2)
            duration2 = duration2.lower()
            duration2 = duration2.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_by_day(dayss, duration2)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration2) + ".", extra = main))

            return await step_context.replace_dialog("passing")  


        if dosage_inj_3 == "koto dosage3":      
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            med_type = "3"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]
            shape_type = "-1"
            place = ""
            dose = "1"
            duration2 = str(duration2)
            duration2 = duration2.lower()
            duration2 = duration2.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_by_day(dayss, duration2)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration2) + ".", extra = main))
  
            return await step_context.replace_dialog("passing")


        if dosage_syrup_3 == "koto dosage3":  
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            med_type = "4"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]
            shape_type = "-1"
            place = ""
            dose = "1"
            duration2 = str(duration2)
            duration2 = duration2.lower()
            duration2 = duration2.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_by_day(dayss, duration2)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time) + " for " + str(duration2) + ".", extra = main))

            return await step_context.replace_dialog("passing") 


    async def ninth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration2
        global dayss

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("P9", str(duration2))

        if dropfor3 == "drop kothay3":        
            place = step_context.result
            med_type = "1"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = times[0]
            color_code = ""
            shape_type = "-1"
            dosage_ml = ""
            duration2 = str(duration2)
            duration2 = duration2.lower()
            duration2 = duration2.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_by_day(dayss, duration2)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage3, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage3) + " drops of " + str(pill_name) + " at " + str(pill_time)  + " for " + str(duration2) + ".", extra = main))

            return await step_context.replace_dialog("passing")