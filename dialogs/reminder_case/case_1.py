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


####################################################   remind me to take Sapa at 4pm.  #################################################################

class caseOneDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseOneDialog, self).__init__(dialog_id or caseOneDialog.__name__)

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
        
        global userId
        global token
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        
        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        wks.update_acell("Q1", "ENTERED")

        main = step_context.context.activity.text
        wks.update_acell("R1", str(main))    
        pred = reminder_class(main)
        
        global med_names
        global times

        classes = []
        med_names = []
        times = []


        for x in pred.keys():
            if x == "MED_NAME":
                med_name = pred[x]
                med_names.append(med_name)
                classes.append(x)
            if x == "TIME":
                time = pred[x]
                times.append(time)
                classes.append(x)
   

        #remind me to take Sapa at 4pm.
        reply = MessageFactory.text("How often you would like to take the medicine? Will it be for daily or only for some specific days?")
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
        
    
    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

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
                PromptOptions(prompt=MessageFactory.text("For how long you want to take the medicine? Hints- 7 days/ 2 weeks/ 3 months.")),) 

        if periodss == "Specific Days":
            specific = "specific days nite chaise"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please enter those days on which you want to take the medicine. Hint- Saturday/ Monday/ Friday.")),)        


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

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


        if specific == "specific days nite chaise":
            duras = "duration nite hbe"
            dayss = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Do you want to recurr (repeat) the reminder on the selected days?")),) 


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

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
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if med_types == "Drop":
                dosage_drop = "koto drop12"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)

            if med_types == "Capsule":
                dosage_cap = "koto dosage13"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?")),)

            if med_types == "Syringe":
                dosage_inj = "koto dosage14"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)

            if med_types == "Syrup":
                dosage_syrup = "koto dosage15"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)


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
                    PromptOptions(prompt=MessageFactory.text("For how long you want to recurr this reminder? Hint: 2 weeks/ 1 month/ 3 months.")),)
            else:
                med_types2 = "type nite hobe2"
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


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        
        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("P3", str(duration))

        if dosage_tab == "koto dosage11":            
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
            pill_time   = times[0]
            shape_type  = "0"
            place       = ""
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
            dates       = cal_date_adv(duration)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog() 

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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog()  

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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog()  

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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog() 


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
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if med_type5I == "Drop":
                dosage_drop_2 = "koto drop2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)

            if med_type5I == "Capsule":
                dosage_cap_2 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?")),)

            if med_type5I == "Syringe":
                dosage_inj_2 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)

            if med_type5I == "Syrup":
                dosage_syrup_2 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)


        global med_types3
        global duration2

        med_types3      = "jnsvbubsv"
        duration2       = "snvsuivsv"

        if recurr_or_not == "asking":
            duration2 = step_context.result
            med_types3 = "type nite hobe3"

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



    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global duration
        global duration2

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("P7", str(duration2))
        
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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage1) + " drops of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration) + "."))
            return await step_context.end_dialog()



        if dosage_tab_2 == "koto dosage2":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            # try:
            #     dosage = w2n.word_to_num(dosage)
            # except:
            #     dosage = 1
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
            dates = cal_day(dayss)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ "."))
            return await step_context.end_dialog() 

        global dropfor2
        global dosage2

        dropfor2 = "dksbnkjs"
        dosage2  = "kjsnkjsn"

        if dosage_drop_2 == "koto drop2":
            dropfor2 = "drop kothay2"
            dosage   = step_context.result
            dosage   = str(dosage)
            dosage   = dosage.lower()
            dosage2   = dosage.replace("drops", "").replace("drop ", "")

            # try:
            #     dosage2 = w2n.word_to_num(dosage)
            # except:
            #     dosage2 = 1

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

        if dosage_cap_2 == "koto dosage2":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            # try:
            #     dosage = w2n.word_to_num(dosage)
            # except:
            #     dosage = 1
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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+  "."))
            return await step_context.end_dialog()  

        if dosage_inj_2 == "koto dosage2":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            # try:
            #     dosage_ml = w2n.word_to_num(dosage)
            # except:
            #     dosage_ml = 1
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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()  

        if dosage_syrup_2 == "koto dosage2":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage_ml = dosage.replace("mL", "").replace("ml", "")
            # try:
            #     dosage_ml = w2n.word_to_num(dosage)
            # except:
            #     dosage_ml = 1
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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog() 


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
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if med_type5I == "Drop":
                dosage_drop_3 = "koto drop3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)

            if med_type5I == "Capsule":
                dosage_cap_3 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?")),)

            if med_type5I == "Syringe":
                dosage_inj_3 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)

            if med_type5I == "Syrup":
                dosage_syrup_3 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global duration2

        if dropfor2 == "drop kothay2":

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

            dates = cal_day(dayss)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage2, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage2) + " drops of " + str(pill_name) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()


        if dosage_tab_3 == "koto dosag3":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
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
            duration2 = str(duration2)
            duration2 = duration2.lower()
            duration2 = duration2.replace("for", "").replace("about", "").replace("almost", "")
            dates = cal_date_by_day(dayss, duration2)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration2) + "."))
            return await step_context.end_dialog()    


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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration2) + "."))
            return await step_context.end_dialog()  


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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(duration2) + "."))
            return await step_context.end_dialog()


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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time) + " for " + str(duration2) + "."))
            return await step_context.end_dialog() 


    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration2

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
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage3) + " drops of " + str(pill_name) + " at " + str(pill_time)  + " for " + str(duration2) + "."))
            return await step_context.end_dialog()