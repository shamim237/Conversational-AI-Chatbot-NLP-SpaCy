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
import recognizers_suite as Recognizers
from recognizers_suite import Culture 
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
                    self.fourth_step,
                    self.fifth_step,
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

        wks.update_acell("F1", "dhukse")
        wks.update_acell("F2", ' '.join(map(str, classes)))
        
        #remind me to take napa.
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            type_med = "just name is here-med_type needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time of the day would you like to take the medicine?")),)
        
        #remind me to take Sapa at 4pm.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            type_med = "just name nand time is here-med_type needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How often you would like to take the medicine? Will it be for daily or only for some specific days?")),)
        
        #remind me to take Maxpro 50mg at morning.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            type_med = "just name nand time and u_time is here-med_type needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?")),)

        #remind me to take Fexo daily at 4pm.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
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
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            time_med = "just name,u_time and period is here-med_time needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?")),)

        #remind me to take napa daily at 4pm for three weeks.
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            wks.update_acell("G1", "dhukse2")
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
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" in classes and "DURATION" in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_DOSE" not in classes:
            time_med = "just name,u_time,period and duration is here-med_time needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?")),)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global dosage_q
        global dosage_drop_1
        global dosage_cap_1
        global dosage_inj_1
        global dosage_syrup_1
        global types_med
        global timess
        timess = "suvnvusvsn"
        types_med = "cbsbvjsv"
        dosage_q = "sivnisvi"
        dosage_drop_1 = "sivdfcfnisvi"
        dosage_cap_1 = "sivcvxxnisvi"
        dosage_inj_1 = "sivdvdnisvi"
        dosage_syrup_1 = "vdvdvdv"

        ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
        sh = ac.open("logs_checker")
        wks = sh.worksheet("Sheet1")

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

################################################################################ CASE-2 ############################################################################################################################################
############################################################## remind me to take napa daily at morning for three weeks. #############################################################################################################################################
#############################################################################################################################################################################################################################

        if time_med == "just name,u_time and period is here-med_time needs to be added" or time_med == "just name,u_time,period and duration is here-med_time needs to be added":
            types_med = "type nite hobe"   
            times1 = []
            time1 = step_context.result
            culture = Culture.English
            ss = Recognizers.recognize_datetime(time1, culture)  
            for i in ss:
                ss = i.resolution
                dd = ss['values']
                for j in dd:
                    tim = j['value']  
                    times1.append(tim)   
            timess = times1[0]

            wks.update_acell("A3", str(timess))

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

################################################################################ CASE-1 ############################################################################################################################################
############################################################## remind me to take napa daily at 4pm for three weeks. #############################################################################################################################################
#############################################################################################################################################################################################################################

        #remind me to take napa daily at 4pm for three weeks.
        if not_med == "just name,time,period and duration is here-med_not needs to be added": 
            med_type = step_context.result
            if med_type == "Tablet":
                dosage_q = "koto dosage"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if med_type == "Drop":
                dosage_drop_1 = "koto drop1"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)

            if med_type == "Capsule":
                dosage_cap_1 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many caposules you have to take at a time?")),)

            if med_type == "Syringe":
                dosage_inj_1 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)

            if med_type == "Syrup":
                dosage_syrup_1 = "koto dosage4"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)



    async def thrd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global dosage11
        global dropfor
        dropfor = "smvinmvnsin"
        dosage11 = "sjvisdnin"

        ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
        sh = ac.open("logs_checker")
        wks = sh.worksheet("Sheet1")

################################################################################ CASE-1 ############################################################################################################################################
############################################################## remind me to take napa daily at 4pm for three weeks. #############################################################################################################################################
#############################################################################################################################################################################################################################

        if dosage_q == "koto dosage":
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
            color_code = "#DB4F64"
            pill_time = times[0] 
            shape_type = "0"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()

        if dosage_drop_1 == "koto drop1":
            dropfor = "drop kothay"
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("drops", "").replace("drop ", "")

            try:
                dosage11 = w2n.word_to_num(dosage)
            except:
                dosage11 = 1

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

        if dosage_cap_1 == "koto dosage2":
            dosage = step_context.result
            try:
                dosage = w2n.word_to_num(dosage)
            except:
                dosage = 1
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

            dates = cal_date_adv(durations[0])

            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()

        if dosage_inj_1 == "koto dosage3":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml = w2n.word_to_num(dosage)
            except:
                dosage_ml = 1
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

            dates = cal_date_adv(durations[0])

            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()   

        if dosage_syrup_1 == "koto dosage4":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml = w2n.word_to_num(dosage)
            except:
                dosage_ml = 1
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

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()   

################################################################################ CASE-2 ############################################################################################################################################
############################################################## remind me to take napa daily at morning for three weeks. #############################################################################################################################################
#############################################################################################################################################################################################################################
        global dosage_tab_11
        global dosage_drop_11
        global dosage_cap_11
        global dosage_inj_11
        global dosage_syrup_11

        dosage_tab_11 = "kbdfkbdjf"
        dosage_drop_11 = "akajkjajf"
        dosage_cap_11 = "SONSOVNONV"
        dosage_inj_11 = "QIDIOQDNOI"
        dosage_syrup_11 = "IQ2H3BB89BC"
        wks.update_acell("A5", time_med)

        if types_med == "type nite hobe" and time_med == "just name,u_time,period and duration is here-med_time needs to be added":
            med_type1 = step_context.result
            wks.update_acell("A4", str(med_type1))
            if med_type1 == "Tablet":
                dosage_tab_11 = "koto dosage11"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?")),)

            if med_type1 == "Drop":
                dosage_drop_11 = "koto drop12"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?")),)

            if med_type1 == "Capsule":
                dosage_cap_11 = "koto dosage13"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?")),)

            if med_type1 == "Syringe":
                dosage_inj_11 = "koto dosage14"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)

            if med_type1 == "Syrup":
                dosage_syrup_11 = "koto dosage15"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?")),)


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


################################################################################ CASE-1 ############################################################################################################################################
############################################################## remind me to take napa daily at 4pm for three weeks. #############################################################################################################################################
#############################################################################################################################################################################################################################
        
        if dropfor == "drop kothay":
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

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage11, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage11) + " drops of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()

################################################################################ CASE-2 ############################################################################################################################################
############################################################## remind me to take napa daily at morning for three weeks. #############################################################################################################################################
#############################################################################################################################################################################################################################


        if dosage_tab_11 == "koto dosage11":
            dosage = step_context.result
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
            pill_time = timess
            shape_type = "0"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()

        global dropfor22
        global dosage22

        dropfor22 = "dksbnkjs"
        dosage22 = "kjsnkjsn"

        if dosage_drop_11 == "koto drop12":
            dropfor22 = "drop kothay"
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("drops", "").replace("drop ", "")

            try:
                dosage22 = w2n.word_to_num(dosage)
            except:
                dosage22 = 1

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

        if dosage_cap_11 == "koto dosage13":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            try:
                dosage = w2n.word_to_num(dosage)
            except:
                dosage = 1
            med_type = "2"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = timess 
            shape_type = "-1"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()  

        if dosage_inj_11 == "koto dosage14":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml = w2n.word_to_num(dosage)
            except:
                dosage_ml = 1
            med_type = "3"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = timess 
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()  

        if dosage_syrup_11 == "koto dosage15":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml = w2n.word_to_num(dosage)
            except:
                dosage_ml = 1
            med_type = "4"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = timess
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()  

    
    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

################################################################################ CASE-2 ############################################################################################################################################
############################################################## remind me to take napa daily at morning for three weeks. #############################################################################################################################################
#############################################################################################################################################################################################################################

        if dropfor22 == "drop kothay":
            place22 = step_context.result
            med_type = "1"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = timess 
            color_code = ""
            shape_type = "-1"
            dosage_ml = ""

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage22, color_code, shape_type, place22, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage11) + " drops of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + "."))
            return await step_context.end_dialog()




        





        


                 
        
       

           

        

        

