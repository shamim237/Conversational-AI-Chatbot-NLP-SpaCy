import gspread
import re
from word2number import w2n
from datetime import datetime
from recognizers_suite import Culture 
import recognizers_suite as Recognizers
from recognizers_number import recognize_number, Culture
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from lib.message_factory import MessageFactory
from lib.card import CardAction
from prompt.email_prompt import EmailPrompt
from nlp_model.pill_predict import reminder_class
from date_regex import cal_date_adv
from adv_pill_reminder import save_reminder_spec_days
from dialogs.simple_reminder_dialog import SimplePillReminderDialog
from botbuilder.schema import ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from dialogs.reminder_case.case_1 import caseOneDialog
from dialogs.reminder_case.case_2 import caseTwoDialog
from dialogs.reminder_case.case_3 import caseThreeDialog
from dialogs.reminder_case.case_4 import caseFourDialog
from dialogs.reminder_case.case_5 import caseFiveDialog
from dialogs.reminder_case.case_6 import caseSixDialog
from dialogs.reminder_case.case_7 import caseSevenDialog






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
        self.add_dialog(caseOneDialog(caseOneDialog.__name__))
        self.add_dialog(caseTwoDialog(caseTwoDialog.__name__))
        self.add_dialog(caseThreeDialog(caseThreeDialog.__name__))
        self.add_dialog(caseFourDialog(caseFourDialog.__name__))
        self.add_dialog(caseFiveDialog(caseFiveDialog.__name__))
        self.add_dialog(caseSixDialog(caseSixDialog.__name__))
        self.add_dialog(caseSevenDialog(caseSevenDialog.__name__))
        self.add_dialog(SimplePillReminderDialog(SimplePillReminderDialog.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,
                    self.scnd_step,
                    self.thrd_step,
                    self.fourth_step,
                    self.fifth_step,
                    self.sixth_step,

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
        global doses_times
        global dropfor66

        dropfor66   = "snvnvsvnsv"
        doses_times = "sisinsidfr"
        time_med    = "jadfaffgbd"
        date_med    = "jhsmsi9rki"
        not_med     = "dmmdmdofim"
        
        global userId
        global token
        global pharmacyId
        global main

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")


        main = step_context.context.activity.text
        wks.update_acell("A5", str(main))

        pred = reminder_class(main)

        try:
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
            if x == "MULTI_REMIND":
                multi_dose = pred[x]
                multi_doses.append(multi_dose)
                classes.append(x)

        
        #remind me to take napa. (done)
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            type_med = "just name is here-med_type needs to be added"
            return await step_context.begin_dialog(caseSevenDialog.__name__)
        
        #remind me to take Sapa at 4pm. (done)
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            await step_context.context.send_activity(
                MessageFactory.text("Please wait for a second...", extra = main))           
            return await step_context.begin_dialog(caseOneDialog.__name__, main)

        
        #remind me to take Maxpro 50mg at morning. (done)
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            await step_context.context.send_activity(
                MessageFactory.text("Please wait for a second...", extra = main))           
            return await step_context.begin_dialog(caseTwoDialog.__name__, main)

        
        #remind me to take 10ml Benadryl from tomorrow (done)
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            await step_context.context.send_activity(
                MessageFactory.text("Please wait for a second...", extra = main))           
            return await step_context.begin_dialog(caseThreeDialog.__name__, main)

        #set a pill reminder for bendix tablet daily at 9 pm (done)
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" in classes and "MULTI_REMIND" not in classes:
            await step_context.context.send_activity(
                MessageFactory.text("Please wait for a second...", extra = main))           
            return await step_context.begin_dialog(caseFourDialog.__name__, main)        

        #set a pill reminder for bendix tablet daily at 9 pm for 6 months (done)
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" in classes and "MULTI_REMIND" not in classes:
            await step_context.context.send_activity(
                MessageFactory.text("Please wait for a second...", extra = main))           
            return await step_context.begin_dialog(caseFiveDialog.__name__, main)   

        #remind me to take 5ml glucoplus twice a day
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" not in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" in classes and "MED_TYPE" not in classes and "MULTI_REMIND" in classes:
            await step_context.context.send_activity(
                MessageFactory.text("Please wait for a second...", extra = main))           
            return await step_context.begin_dialog(caseSixDialog.__name__, main)            

        #remind me to take Fexo daily at 4pm. (done)
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            date_med = "just name,time and period is here-med_date needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How long do you have to take this medicine? Ex:- 7 days or 2 weeks or 3 months.", extra = main)),)

        
        #remind me to take napa everyday at night. (done)
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" in classes and "DURATION" not in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            time_med = "just name,u_time and period is here-med_time needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?", extra = main)),)

        #remind me to take napa daily at 4pm for three weeks. (done)
        if "MED_NAME" in classes and "TIME" in classes and "PERIOD" in classes and "DURATION" in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            wks.update_acell("G1", "dhukse2")
            not_med = "just name,time,period and duration is here-med_not needs to be added"
            reply = MessageFactory.text("Please help me to recognize the type of medicine-", extra= main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Tablet",
                        type=ActionTypes.im_back,
                        value= "Tablet",
                        extra= main),
                    CardAction(
                        title= "Drop",
                        type=ActionTypes.im_back,
                        value= "Drop",
                        extra= main),
                    CardAction(
                        title= "Capsule",
                        type=ActionTypes.im_back,
                        value= "Capsule",
                        extra= main),
                    CardAction(
                        title= "Syringe",
                        type=ActionTypes.im_back,
                        value= "Syringe",
                        extra= main),
                    CardAction(
                        title= "Syrup",
                        type=ActionTypes.im_back,
                        value= "Syrup",
                        extra= main),])
            return await step_context.context.send_activity(reply) 

        
        #remind me to take napa daily at morning for two weeks.
        if "MED_NAME" in classes and "TIME" not in classes and "PERIOD" in classes and "DURATION" in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" in classes and "QUANT" not in classes and "MED_TYPE" not in classes and "MULTI_REMIND" not in classes:
            time_med = "just name,u_time,period and duration is here-med_time needs to be added"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("At what time in the " + str(u_times[0]) + " you need to take the medicine?", extra = main)),)

        #remind me to take 4 Napa tablets daily at 5 pm for 3 months
        if "MED_NAME" in classes and "TIME" in classes and "MED_TYPE" in classes and "DURATION" in classes and "PERIOD" in classes and "QUANT" in classes and "START_DATE" not in classes and "END_DATE" not in classes and "U_TIME" not in classes and "MULTI_REMIND" not in classes:
            
            tablet = ["tablet", "tablets", "tabs", "tab."] 
            drop = ["drops", "drop"]
            syrup = ["syrup", "syrups"]
            syringe = ["syringe", "syringes", "injections", "injection"]
            caps = ["capsules", "capsule", "caps", "cap."]
            types = med_types[0].lower()

            if types in tablet:
                med_types = "0"
                nums = []
                if "a" != quants[0] or "an" != quants[0]:
                    result = recognize_number(quants[0], Culture.English)
                    for i in result:
                        k = i.resolution
                        num = k['value']
                        nums.append(num)
                else:
                    num = "1"
                    nums.append(num)
                dosage = nums[0]
                pill_name = med_names[0]
                pill_time = times[0]

                extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
                times = [] 
                tk = []    
                for i in extract:
                    keys = i.resolution
                    values = keys['values']
                    for j in values:
                        timea = j['value']  
                        times.append(timea) 

                for i in times:
                    dp = datetime.strptime(i, "%H:%M:%S")
                    dt = datetime.strftime(dp, "%I:%M %p")
                    tk.append(dt)

                pill_time = tk[0]
                patientid = userId
                pharmacyid = pharmacyId
                tokens = token
                color_code = "#DB4F64"
                shape_type = "0"
                place = ""
                dosage_ml = ""
                dates = cal_date_adv(durations[0])
                save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_types, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))
                return await step_context.replace_dialog("passing") 

            if types in drop:
                dropfor66 = "drop kothay"
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

            if types in caps:
                med_types = "2"
                pill_name = med_names[0]
                patientid = userId
                pharmacyid = pharmacyId
                tokens = token
                pill_time = times[0]

                extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
                times = [] 
                tk = []    
                for i in extract:
                    keys = i.resolution
                    values = keys['values']
                    for j in values:
                        timea = j['value']  
                        times.append(timea) 

                for i in times:
                    dp = datetime.strptime(i, "%H:%M:%S")
                    dt = datetime.strftime(dp, "%I:%M %p")
                    tk.append(dt)

                pill_time = tk[0]
                shape_type = "-1"
                place = ""
                dosage_ml = ""
                dosage = quants[0]
                dates = cal_date_adv(durations[0])

                save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_types, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

                return await step_context.replace_dialog("passing") 

            if types in syringe:
                med_types = "3"
                pill_name = med_names[0]
                patientid = userId
                pharmacyid = pharmacyId
                tokens = token
                color_code = ""
                pill_time = times[0]

                extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
                times = [] 
                tk = []    
                for i in extract:
                    keys = i.resolution
                    values = keys['values']
                    for j in values:
                        timea = j['value']  
                        times.append(timea) 

                for i in times:
                    dp = datetime.strptime(i, "%H:%M:%S")
                    dt = datetime.strftime(dp, "%I:%M %p")
                    tk.append(dt)

                pill_time = tk[0] 
                shape_type = "-1"
                place = ""
                dose = "1"
                dosage_ml = quants[0]
                dates = cal_date_adv(durations[0])

                save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_types, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

                return await step_context.replace_dialog("passing")   

            if types in syrup:
                med_types = "4"
                pill_name = med_names[0]
                patientid = userId
                pharmacyid = pharmacyId
                tokens = token
                color_code = ""
                pill_time = times[0]

                extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
                times = [] 
                tk = []    
                for i in extract:
                    keys = i.resolution
                    values = keys['values']
                    for j in values:
                        timea = j['value']  
                        times.append(timea) 

                for i in times:
                    dp = datetime.strptime(i, "%H:%M:%S")
                    dt = datetime.strftime(dp, "%I:%M %p")
                    tk.append(dt)

                pill_time = tk[0]
                shape_type = "-1"
                place = ""
                dose = "1"
                dosage_ml = quants[0]
                dates = cal_date_adv(durations[0])

                save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_types, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))
                return await step_context.replace_dialog("passing")  
        else:
            return await step_context.begin_dialog(SimplePillReminderDialog.__name__)



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

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

################################################################################ CASE-6 ###################################################################################################################################################
############################################################## remind me to take 4 Napa tablets daily at 5 pm for 3 months #############################################################################################################################################
###########################################################################################################################################################################################################################################
        if dropfor66 == "drop kothay":
            place = step_context.result
            med_types = "1"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = times[0]

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0] 
            color_code = ""
            shape_type = "-1"
            dose = quants[0]
            dosage_ml = "2 ml"

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_types, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)

            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dose) + " drops of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))
            return await step_context.replace_dialog("passing")           
            

################################################################################ CASE-3 ############################################################################################################################################
############################################################## remind me to take Fexo daily at 4pm. #############################################################################################################################################
#############################################################################################################################################################################################################################
        
        
        global type_case3
        global duration33
        type_case3 = "snsjvnsljv"
        duration33 = "snssxbxbxb"

        if date_med == "just name,time and period is here-med_date needs to be added":
            duration33 = step_context.result
            type_case3 = "tell med type"
            reply = MessageFactory.text("Please help me to recognize the type of medicine-", extra= main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Tablet",
                        type=ActionTypes.im_back,
                        value= "Tablet",
                        extra= main),
                    CardAction(
                        title= "Drop",
                        type=ActionTypes.im_back,
                        value= "Drop",
                        extra= main),
                    CardAction(
                        title= "Capsule",
                        type=ActionTypes.im_back,
                        value= "Capsule",
                        extra= main),
                    CardAction(
                        title= "Syringe",
                        type=ActionTypes.im_back,
                        value= "Syringe",
                        extra= main),
                    CardAction(
                        title= "Syrup",
                        type=ActionTypes.im_back,
                        value= "Syrup",
                        extra= main),])
            return await step_context.context.send_activity(reply) 

################################################################################ CASE-4 ############################################################################################################################################
############################################################## remind me to take Fexo daily at morning. #############################################################################################################################################
#############################################################################################################################################################################################################################

        global times44
        global dura44
        times44 = "snsjljv"
        dura44  = "snxsgsdg"

        if time_med == "just name,u_time and period is here-med_time needs to be added":
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

            times44 = times[0]
            dura44 = "duration nite hbe"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("How long do you have to take this medicine? Ex:- 7 days or 2 weeks or 3 months.", extra = main)),)

################################################################################ CASE-2 ############################################################################################################################################
############################################################## remind me to take napa daily at morning for three weeks. #############################################################################################################################################
###########################################################################################################################################################################################################################

        if time_med == "just name,u_time,period and duration is here-med_time needs to be added":
            types_med = "type nite hobe"   
            time = step_context.result
            time = str(time)
            
            culture = Culture.English
            times1 = [] 
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
                        times1.append(tim)     
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
                        times1.append(tim)    
                          
            timess = times1[0]

            wks.update_acell("A3", str(timess))

            reply = MessageFactory.text("Please help me to recognize the type of medicine-", extra= main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Tablet",
                        type=ActionTypes.im_back,
                        value= "Tablet",
                        extra= main),
                    CardAction(
                        title= "Drop",
                        type=ActionTypes.im_back,
                        value= "Drop",
                        extra= main),
                    CardAction(
                        title= "Capsule",
                        type=ActionTypes.im_back,
                        value= "Capsule",
                        extra= main),
                    CardAction(
                        title= "Syringe",
                        type=ActionTypes.im_back,
                        value= "Syringe",
                        extra= main),
                    CardAction(
                        title= "Syrup",
                        type=ActionTypes.im_back,
                        value= "Syrup",
                        extra= main),])
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
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if med_type == "Drop":
                dosage_drop_1 = "koto drop1"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if med_type == "Capsule":
                dosage_cap_1 = "koto dosage2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many caposules you have to take at a time?", extra = main)),)

            if med_type == "Syringe":
                dosage_inj_1 = "koto dosage3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)

            if med_type == "Syrup":
                dosage_syrup_1 = "koto dosage4"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)



    async def thrd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        global type_case3
        
        global dosage11
        global dropfor
        dropfor = "smvinmvnsin"
        dosage11 = "sjvisdnin"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
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

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            shape_type = "0"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing") 

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

            reply = MessageFactory.text("Where to use the drop?", extra= main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Eye",
                        type= ActionTypes.im_back,
                        value= "Eye",
                        extra= main),
                    CardAction(
                        title= "Nose",
                        type= ActionTypes.im_back,
                        value= "Nose",
                        extra= main),
                    CardAction(
                        title= "Ear",
                        type= ActionTypes.im_back,
                        value= "Ear",
                        extra= main),
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

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            shape_type = "-1"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(durations[0])

            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))
            return await step_context.replace_dialog("passing")

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

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0] 
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(durations[0])

            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing")  

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

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing")   

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
        # wks.update_acell("A5", time_med)

        if types_med == "type nite hobe" and time_med == "just name,u_time,period and duration is here-med_time needs to be added":
            med_type1 = step_context.result
            if med_type1 == "Tablet":
                dosage_tab_11 = "koto dosage11"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if med_type1 == "Drop":
                dosage_drop_11 = "koto drop12"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if med_type1 == "Capsule":
                dosage_cap_11 = "koto dosage13"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)

            if med_type1 == "Syringe":
                dosage_inj_11 = "koto dosage14"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)

            if med_type1 == "Syrup":
                dosage_syrup_11 = "koto dosage15"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)

################################################################################ CASE-3 ############################################################################################################################################
############################################################## remind me to take Fexo daily at 4pm. #############################################################################################################################################
#############################################################################################################################################################################################################################

        global dosage_tab_33
        global dosage_drop_33
        global dosage_cap_33
        global dosage_inj_33
        global dosage_syrup_33

        dosage_tab_33   = "skcvvbvb"
        dosage_drop_33  = "skcdscws"
        dosage_cap_33   = "saaqdkcs"
        dosage_inj_33   = "sk232cds"
        dosage_syrup_33 = "vczvzwss"

        if type_case3 == "tell med type":
            med_type3 = step_context.result
            if med_type3 == "Tablet":
                dosage_tab_33 = "koto dosage11"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)
            if med_type3 == "Drop":
                dosage_drop_33 = "koto drop12"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)
            if med_type3 == "Capsule":
                dosage_cap_33 = "koto dosage13"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)
            if med_type3 == "Syringe":
                dosage_inj_33 = "koto dosage14"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)
            if med_type3 == "Syrup":
                dosage_syrup_33 = "koto dosage15"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)


################################################################################ CASE-4 ############################################################################################################################################
############################################################## remind me to take Fexo daily at morning. #############################################################################################################################################
#############################################################################################################################################################################################################################
        global duration44
        global med_type44

        duration44 = "sjfsjdfj"
        med_type44 = "msoososa"

        if dura44 == "duration nite hbe":
            duration44 = step_context.result
            med_type44 = "type nite hobe44"

            reply = MessageFactory.text("Please help me to recognize the type of medicine-", extra= main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Tablet",
                        type=ActionTypes.im_back,
                        value= "Tablet",
                        extra= main),
                    CardAction(
                        title= "Drop",
                        type=ActionTypes.im_back,
                        value= "Drop",
                        extra= main),
                    CardAction(
                        title= "Capsule",
                        type=ActionTypes.im_back,
                        value= "Capsule",
                        extra= main),
                    CardAction(
                        title= "Syringe",
                        type=ActionTypes.im_back,
                        value= "Syringe",
                        extra= main),
                    CardAction(
                        title= "Syrup",
                        type=ActionTypes.im_back,
                        value= "Syrup",
                        extra= main),])
            return await step_context.context.send_activity(reply)  





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

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            color_code = ""
            shape_type = "-1"
            dosage_ml = ""

            dates = cal_date_adv(durations[0])
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage11, color_code, shape_type, place, dosage_ml)

            #remind me to take napa daily at 4pm for three weeks.
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage11) + " drops of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing")

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
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing")

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

            reply = MessageFactory.text("Where to use the drop?", extra= main)
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
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing")

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
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing")  

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
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing") 

################################################################################ CASE-3 ############################################################################################################################################
############################################################## remind me to take Fexo daily at 4pm. #############################################################################################################################################
#############################################################################################################################################################################################################################

        if dosage_tab_33 == "koto dosage11":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("tablets", "").replace("tabs", "").replace("tablet", "").replace("tab", "")
            try:
                dosage = w2n.word_to_num(dosage)
            except:
                dosage = dosage

            med_type = "0"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = "#DB4F64"
            pill_time = times[0]

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            shape_type = "0"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(duration33)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration33) + ".", extra = main))

            return await step_context.replace_dialog("passing")

        global dropfor33
        global dosage33

        dropfor33 = "dksbnkjs"
        dosage33  = "kjsnkjsn"

        if dosage_drop_33 == "koto drop12":
            dropfor33 = "drop kothay"
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("drops", "").replace("drop ", "")

            try:
                dosage33 = w2n.word_to_num(dosage)
            except:
                dosage33 = dosage

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

        if dosage_cap_33 == "koto dosage13":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace(" capsules", "").replace(" capsule", "").replace("caps", "")
            try:
                dosage = w2n.word_to_num(dosage)
            except:
                dosage = dosage
            med_type = "2"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            shape_type = "-1"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(duration33)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration33) + ".", extra = main))

            return await step_context.replace_dialog("passing")  

        if dosage_inj_33 == "koto dosage14":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml = w2n.word_to_num(dosage)
            except:
                dosage_ml = dosage
            med_type = "3"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(duration33)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration33) + ".", extra = main))

            return await step_context.replace_dialog("passing") 

        if dosage_syrup_33 == "koto dosage15":
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("mL", "").replace("ml", "")
            try:
                dosage_ml = w2n.word_to_num(dosage)
            except:
                dosage_ml = dosage
            med_type = "4"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            color_code = ""
            pill_time = times[0]

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(duration33)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration33) + ".", extra = main))

            return await step_context.replace_dialog("passing")

################################################################################ CASE-4 ############################################################################################################################################
############################################################## remind me to take Fexo daily at morning. #############################################################################################################################################
#############################################################################################################################################################################################################################

        global dosage_tab_44
        global dosage_cap_44
        global dosage_drop_44
        global dosage_inj_44
        global dosage_syrup_44

        dosage_tab_44   = "amsmamsm"
        dosage_cap_44   = "awmxdjnd"
        dosage_drop_44  = "sknkzvns"
        dosage_inj_44   = "eeevvass"
        dosage_syrup_44 = "kjsnkjsn"


        if med_type44 == "type nite hobe44":
            med_type4 = step_context.result
            if med_type4 == "Tablet":
                dosage_tab_44 = "koto dosage11"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many tablets you have to take at a time?", extra = main)),)

            if med_type4 == "Drop":
                dosage_drop_44 = "koto drop12"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("What is the recommended drops of medicine you need to consume?", extra = main)),)

            if med_type4 == "Capsule":
                dosage_cap_44 = "koto dosage13"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many capsules you have to take at a time?", extra = main)),)

            if med_type4 == "Syringe":
                dosage_inj_44 = "koto dosage14"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)

            if med_type4 == "Syrup":
                dosage_syrup_44 = "koto dosage15"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("How many mL has it been recommended?", extra = main)),)


    
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
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage22) + " drops of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(durations[0]) + ".", extra = main))

            return await step_context.replace_dialog("passing")

################################################################################ CASE-3 ############################################################################################################################################
############################################################## remind me to take Fexo daily at 4pm. #############################################################################################################################################
#############################################################################################################################################################################################################################

        if dropfor33 == "drop kothay":
            place33 = step_context.result
            med_type = "1"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = times[0]

            extract = Recognizers.recognize_datetime(pill_time, culture= Culture.English) 
            times = [] 
            tk = []    
            for i in extract:
                keys = i.resolution
                values = keys['values']
                for j in values:
                    timea = j['value']  
                    times.append(timea) 

            for i in times:
                dp = datetime.strptime(i, "%H:%M:%S")
                dt = datetime.strftime(dp, "%I:%M %p")
                tk.append(dt)

            pill_time = tk[0]
            color_code = ""
            shape_type = "-1"
            dosage_ml = ""

            dates = cal_date_adv(duration33)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage33, color_code, shape_type, place33, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage33) + " drops of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration33) + ".", extra = main))

            return await step_context.replace_dialog("passing")


################################################################################ CASE-4 ############################################################################################################################################
############################################################## remind me to take Fexo daily at morning. #############################################################################################################################################
#############################################################################################################################################################################################################################

        if dosage_tab_44 == "koto dosage11":
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
            pill_time = times44
            shape_type = "0"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(duration44)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration44) + ".", extra = main))

            return await step_context.replace_dialog("passing") 

        global dropfor44
        global dosage44

        dropfor44 = "dksbnkjs"
        dosage44  = "kjsnkjsn"

        if dosage_drop_44 == "koto drop12":
            dropfor44 = "drop kothay"
            dosage = step_context.result
            dosage = str(dosage)
            dosage = dosage.lower()
            dosage = dosage.replace("drops", "").replace("drop ", "")

            try:
                dosage44 = w2n.word_to_num(dosage)
            except:
                dosage44 = 1

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

        if dosage_cap_44 == "koto dosage13":
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
            pill_time = times44 
            shape_type = "-1"
            place = ""
            dosage_ml = ""

            dates = cal_date_adv(duration44)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration44) + ".", extra = main))

            return await step_context.replace_dialog("passing")  

        if dosage_inj_44 == "koto dosage14":
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
            pill_time = times44
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(duration44)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration44) + ".", extra = main))

            return await step_context.replace_dialog("passing") 

        if dosage_syrup_44 == "koto dosage15":
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
            pill_time = times44
            shape_type = "-1"
            place = ""
            dose = "1"

            dates = cal_date_adv(duration44)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dose, color_code, shape_type, place, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage_ml) + " dose of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration44) + ".", extra = main))

            return await step_context.replace_dialog("passing")


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

################################################################################ CASE-4 ############################################################################################################################################
############################################################## remind me to take Fexo daily at morning. #############################################################################################################################################
#############################################################################################################################################################################################################################        
        
        if dropfor44 == "drop kothay":
            place44 = step_context.result
            med_type = "1"
            pill_name = med_names[0]
            patientid = userId
            pharmacyid = pharmacyId
            tokens = token
            pill_time = times44
            color_code = ""
            shape_type = "-1"
            dosage_ml = ""

            dates = cal_date_adv(duration44)
            save_reminder_spec_days(patientid, pharmacyid, tokens, pill_name, med_type, pill_time, dates, dosage44, color_code, shape_type, place44, dosage_ml)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(dosage44) + " drops of " + str(pill_name) + " " + str(periods[0]) + " at " + str(pill_time)+ " for " + str(duration44) + ".", extra = main))

            return await step_context.replace_dialog("passing")


       

           

        

        

