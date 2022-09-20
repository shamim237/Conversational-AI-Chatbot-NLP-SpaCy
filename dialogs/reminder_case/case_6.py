from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from lib.message_factory import MessageFactory
from lib.card import CardAction
from prompt.email_prompt import EmailPrompt
from nlp_model.pill_predict import reminder_class
from adv_pill_reminder import save_reminder_spec_days_multi_time
from date_regex import cal_date_adv, cal_date_by_day
from botbuilder.schema import ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
import recognizers_suite as Recognizers
from recognizers_suite import Culture 
import gspread

####################################################  remind me to take 5ml glucoplus twice a day  #################################################################

class caseSixDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseSixDialog, self).__init__(dialog_id or caseSixDialog.__name__)

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
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global userId
        global token
        global main
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        main = step_context.context.activity.text
        pred = reminder_class(main)
        
        global med_names
        global multi_doses
        global quants

        classes      = []
        med_names    = []
        multi_doses  = []
        quantsx      = []

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")



################################################################# remind me to take 5ml glucoplus twice a day ################################################################################
        
        for x in pred.keys():
            if x == "MED_NAME":
                med_name = pred[x]
                med_names.append(med_name)
                classes.append(x)
            if x == "MULTI_REMIND":
                multi_dose = pred[x]
                multi_doses.append(multi_dose)
                classes.append(x)
            if x == "QUANT":
                quant = pred[x]
                quantsx.append(quant)
                classes.append(x)


        quants = "".join(quantsx)

        try:
            wks.update_acell("F6", str(quants))
        except:
            pass

        await step_context.context.send_activity(
            MessageFactory.text("What times of the day do you want to take the medicine? Hint- 9AM, 2PM or 10PM.", extra = main))
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Please enter those times in the day.", extra = main)),) 

    
    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global timess

        times = step_context.result
        culture = Culture.English
        raw = Recognizers.recognize_datetime(str(times), culture) 
        timess = []     
        for i in raw:
            raw = i.resolution
            dd = raw['values']
            for j in dd:
                tim = j['value']  
                timess.append(tim)    


        return await step_context.prompt(
            TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How many days do you have to take this medicine? Hint- 7 days/2 weeks/3 months.", extra = main)),)  

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global duration
        duration = step_context.result

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
        
        global med_type1
        global spec
        med_type1   = "auyauas"
        spec        = "auauaua"

        msg = step_context.result

        if msg == "Daily":

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


        if msg == "Specific Days":
            spec = "specific days nite chaise"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please enter those days on which you want to take the medicine. Hint- Saturday/Monday/Friday.", extra = main)),)  


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global timess
        global duration
        global dropfor1
        global dosage1

        dropfor1 = "dksbnkjs"
        dosage1  = "kjsnkjsn"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        wks.update_acell("F1", str(med_type1))
        wks.update_acell("F2", str(step_context.result))
        wks.update_acell("F6", str(quants))

        if med_type1 == "type nite hobe1":

            typeo = step_context.result

            wks.update_acell("G1", str(typeo))
            wks.update_acell("F3", "entered")
            wks.update_acell("G2", str(duration))
            wks.update_acell("F4", "entered")

            if typeo == "Tablet":
                dosage      = quants
                wks.update_acell("G4", str(dosage))
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage      = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
                wks.update_acell("G5", str(dosage))
                med_type    = "0"
                pill_name   = med_names[0]
                wks.update_acell("G6", str(pill_name))
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = "#DB4F64"
                pill_time   = timess
                wks.update_acell("G7", str(pill_time))
                shape_type  = "0"
                place       = ""
                dosage_ml   = ""
                wks.update_acell("G8", str(duration))
                duration    = str(duration)
                duration    = duration.lower()
                duration    = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
                wks.update_acell("G9", str(duration))
                dates       = cal_date_adv(duration)
                wks.update_acell("G10", str(duration))
                wks.update_acell("G11", str(dates))
                save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog() 
    

            if typeo == "Drop": 

                dropfor1    = "drop kothay"
                dosage      = quants
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


            if typeo == "Capsule":
                dosage      = quants
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage      = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
                med_type    = "2"
                pill_name   = med_names[0]
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = ""
                pill_time   = timess
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
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog() 
        

            if typeo == "Syringe":
                wks.update_acell("G3", str(quants))
                dosage      = quants
                wks.update_acell("G4", str(dosage))
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage_ml   = dosage.replace("mL", "").replace("ml", "")
                wks.update_acell("G5", str(dosage_ml))
                med_type    = "3"
                pill_name   = med_names[0]
                wks.update_acell("G6", str(pill_name))
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = ""
                pill_time   = timess
                wks.update_acell("G7", str(pill_time))
                shape_type  = "-1"
                place       = ""
                dose        = "1"
                wks.update_acell("G8", str(duration))
                duration    = str(duration)
                duration    = duration.lower()
                duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
                wks.update_acell("G9", str(duration))
                dates = cal_date_adv(duration)
                wks.update_acell("G10", str(duration))
                wks.update_acell("G11", str(dates))
                save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()    


            if typeo == "Syrup":
                dosage      = quants
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage_ml   = dosage.replace("mL", "").replace("ml", "")

                med_type    = "4"
                pill_name   = med_names[0]
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = ""
                pill_time   = timess
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
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()  

        global dayss
        global med_type2

        dayss       = "ssisisi"
        med_type2   = "atatats"


        if spec == "specific days nite chaise":
            dayss = step_context.result
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
        
        global dayss
        global timess
        global duration
        global dropfor2
        global dosage2

        dropfor2 = "dksbnkjs"
        dosage2  = "kjsnkjsn"

        if dropfor1 == "drop kothay":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            pill_time   = timess
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
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage1) + " drops of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("end dialog", extra = main))
            return await step_context.end_dialog() 



        if med_type2 == "type nite hobe2":   

            typeos = step_context.result

            if typeos == "Tablet":                     
                dosage      = quants
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage      = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
                med_type    = "0"
                pill_name   = med_names[0]
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = "#DB4F64"
                pill_time   = timess
                shape_type  = "0"
                place       = ""
                dosage_ml   = ""
                duration    = str(duration)
                duration    = duration.lower()
                duration    = duration.replace("for ", "").replace("about ", "").replace("almost ", "")
                dates       = cal_date_by_day(dayss, duration)
                save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()  

            if typeos == "Drop": 
                dropfor2    = "drop kothay2"
                dosage      = quants
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

            
            if typeos == "Capsule":
                dosage      = quants
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage      = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
                med_type    = "2"
                pill_name   = med_names[0]
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = ""
                pill_time   = timess
                shape_type  = "-1"
                place       = ""
                dosage_ml   = ""
                duration    = str(duration)
                duration    = duration.lower()
                duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
                dates       = cal_date_by_day(dayss, duration)
                save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()       


            if typeos == "Syringe":
                dosage      = quants
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage_ml   = dosage.replace("mL", "").replace("ml", "")
                med_type    = "3"
                pill_name   = med_names[0]
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = ""
                pill_time   = timess
                shape_type  = "-1"
                place       = ""
                dose        = "1"
                duration    = str(duration)
                duration    = duration.lower()
                duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
                dates       = cal_date_by_day(dayss, duration)
                save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()    


            if typeos == "Syrup":
                dosage      = quants
                dosage      = str(dosage)
                dosage      = dosage.lower()
                dosage_ml   = dosage.replace("mL", "").replace("ml", "")

                med_type    = "4"
                pill_name   = med_names[0]
                patientid   = userId
                pharmacyid  = pharmacyId
                tokens      = token
                color_code  = ""
                pill_time   = timess
                shape_type  = "-1"
                place       = ""
                dose        = "1"
                duration    = str(duration)
                duration    = duration.lower()
                duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
                dates       = cal_date_by_day(dayss, duration)
                save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()          


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 
        
        global dayss
        global timess
        global duration


        if dropfor2 == "drop kothay2":
            place       = step_context.result
            med_type    = "1"
            pill_name   = med_names[0]
            patientid   = userId
            pharmacyid  = pharmacyId
            tokens      = token
            pill_time   = timess
            color_code  = ""
            shape_type  = "-1"
            dosage_ml   = ""
            duration    = str(duration)
            duration    = duration.lower()
            duration    = duration.replace("for", "").replace("about", "").replace("almost", "")
            dates       = cal_date_by_day(dayss, duration)
            save_reminder_spec_days_multi_time(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage2, color_code, shape_type, place, dosage_ml)    
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage1) + " drops of " + str(pill_name) + " " + str(multi_doses[0])+ " for " + str(duration) + ".", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("end dialog", extra = main))
            return await step_context.end_dialog()         