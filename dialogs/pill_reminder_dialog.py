from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from botbuilder.dialogs.choices import Choice
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from pill_reminder import save_reminder_spec_days_multi, save_reminder_multi_time, save_reminder_one_time, save_reminder_spec_days_one, save_reminder_spec_days_one_capsule, save_reminder_spec_days_multi_capsule,\
    save_reminder_one_time_capsule, save_reminder_multi_time_capsule, save_reminder_spec_days_one_syrup, save_reminder_spec_days_multi_syrup, save_reminder_spec_days_one_syringe, save_reminder_spec_days_multi_syringe,\
        save_reminder_spec_days_one_drops, save_reminder_spec_days_multi_drops, save_reminder_one_time_syrup, save_reminder_multi_time_syrup,save_reminder_one_time_syringe, save_reminder_multi_time_syringe, save_reminder_one_time_drop,\
            save_reminder_multi_time_drop
from datetime import date, timedelta
from word2number import w2n
import recognizers_suite as Recognizers
from recognizers_suite import Culture 
from date_regex import cal_date
from botbuilder.schema import CardAction, ActionTypes, SuggestedActions
class PillReminderDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(PillReminderDialog, self).__init__(dialog_id or PillReminderDialog.__name__)

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
                    self.times_step,
                    self.times1_step,
                    self.times2_step,
                    self.recur_step,
                    self.date_step,
                    self.medicine_step,
                    self.dosage_step,
                    self.dosage2_step,
                    self.dosage3_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def times_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("How many times in a day do you want to take medicine?")),)  


    async def times1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global single_time
        global multi_time
        global dosage_time

        single_time = "mvionnvb"
        multi_time = "svso3rq3nr"
        dosage_time = "sssdfsrq3nr"

        times = step_context.result 
        times = str(times)
        pred = predict_class(times)

        if pred == "times":
            multi_time = "multiple time taking"
            dosage_time = times.replace(" times", "").replace("times", "").replace(" time", "").replace("time", "").replace("for", "").replace("for ", "")
            try:
                dosage_time = w2n.word_to_num(dosage_time)
            except:
                dosage_time = 2

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Okay! Please enter those times at when you want to take medicine. Hint- 9AM, 2PM and 10PM.")),)           
        
        else:
            single_time = "single time taking"
            dosage_time = times.replace("times", "").replace("time", "").replace("for", "").replace("only", "")
            try:
                dosage_time = w2n.word_to_num(dosage_time)
            except:
                dosage_time = 1

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Okay! Please enter the time at when you want to take medicine. Hint- 9AM.")),)

    async def times2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global timess
        
        timess = "nsinvbnsvb"

        if single_time == "single time taking":
            time = step_context.result
            culture = Culture.English
            ss = Recognizers.recognize_datetime(time, culture) 
            times = []     
            for i in ss:
                ss = i.resolution
                dd = ss['values']
                for j in dd:
                    tim = j['value']  
                    times.append(tim)   
            timess = times[0]
        
        if multi_time == "multiple time taking":
            times = step_context.result
            culture = Culture.English
            ss = Recognizers.recognize_datetime(times, culture) 
            timess = []     
            for i in ss:
                ss = i.resolution
                dd = ss['values']
                for j in dd:
                    tim = j['value']  
                    timess.append(tim)   
                  
        reply = MessageFactory.text("Do you want this reminder recurring or for specific days?")
        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title= "Recurring",
                    type=ActionTypes.im_back,
                    value= "Recurring",),
                CardAction(
                    title = "Not Recurring",
                    type = ActionTypes.im_back,
                    value = "Not Recurring",),
                    ])
        return await step_context.context.send_activity(reply)

            
    async def recur_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global recur
        global option
        recur = "asdhjasdfjh"

        option = step_context.result

        if option == "Recurring":
            recur = "want recurring"
            reply = MessageFactory.text("Okay! For how long do you want to recur the reminder?")
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Two Weeks",
                        type=ActionTypes.im_back,
                        value= "Two Weeks"),
                    CardAction(
                        title= "Three Weeks",
                        type=ActionTypes.im_back,
                        value= "Three Weeks"),
                    CardAction(
                        title= "1 Month",
                        type=ActionTypes.im_back,
                        value= "1 Month"),
                    CardAction(
                        title= "2 Months",
                        type=ActionTypes.im_back,
                        value= "2 Months"),
                    CardAction(
                        title= "3 Months",
                        type=ActionTypes.im_back,
                        value= "3 Months"),])
            return await step_context.context.send_activity(reply)

        if option == "Not Recurring":
            recur = "don't want recurring"
            await step_context.context.send_activity(
                MessageFactory.text(f"Okay! Please enter date on that you want to set the reminder."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("You can enter multiple dates (more than one day). Date Fromat- YYYY-MM-DD.")),) 

    async def date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global var
        global long_date
        global spec_dates

        spec_dates = "sinisuuvb"
        var = "abcdefgh"
        long_date = "anfnivv"

        if recur == "want recurring":
            var = "long_date_nilam"
            long_date = step_context.result
            await step_context.context.send_activity(
                MessageFactory.text(f"Please enter dates that you want to set the reminder and I will repeatedly remind you on those dates for " + str(long_date) + "."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("It can be a single day or multiple days. Date Format- YYYY-MM-DD")),)

        if recur == "don't want recurring":
            var = "med_name"
            culture = Culture.English
            ss = Recognizers.recognize_datetime(step_context.result, culture)
            spec_dates = []
            for i in ss:
                ss = i.resolution
                dd = ss['values']
                for j in dd:
                    tim = j['value']  
                    spec_dates.append(tim)
            await step_context.context.send_activity(
                MessageFactory.text(f"Which medicine would you like to take?"))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please enter the medicine name.")),) 
        
    async def medicine_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global meds
        global dose
        global type
        global recur_dates
        global dosage_ml
        global meds_typ
        global meds_name

        meds_name = "smnvsuionvin"
        meds_typ = "vksvosv"
        dosage_ml = 'boibiobn'
        recur_dates = "mnnnv"
        type = "smivmnn"
        dose = "msomnwon"
        meds = "medsxzmvsoinv"

        if var == "long_date_nilam":
            meds = "med name nibo"
            culture = Culture.English
            ss = Recognizers.recognize_datetime(step_context.result, culture)
            recur_dates = []
            for i in ss:
                ss = i.resolution
                dd = ss['values']
                for j in dd:
                    tim = j['value']  
                    recur_dates.append(tim)
            await step_context.context.send_activity(
                MessageFactory.text(f"Which medicine would you like to take?"))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Please enter the medicine name.")),) 

        if var == "med_name":
            meds_name = step_context.result
            meds_type = predict_class(meds_name)
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time

            if meds_type == "tablet":
                if dosage_times == 1:
                    save_reminder_spec_days_one(patientid, pharmacyid, tokens, pillName, pill_time, dates)
                else:
                    save_reminder_spec_days_multi(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times)   

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time)+ "."))
                return await step_context.end_dialog()

            if meds_type == "capsule":
                if dosage_times == 1:
                    save_reminder_spec_days_one_capsule(patientid, pharmacyid, tokens, pillName, pill_time, dates)
                else:
                    save_reminder_spec_days_multi_capsule(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times)   

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time)+ "."))
                return await step_context.end_dialog()

            if meds_type == "syrup":
                dosage_ml = "dosage_ml koto"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)

            if meds_type == "syringe":
                dosage_ml = "dosage_ml koto_syringe"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)

            if meds_type == "drops":
                dosage_ml = "dosage_ml koto drops"
                await step_context.context.send_activity(
                    MessageFactory.text(f"How many drops are recommended by the doctor?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the quantity of drops. Hint- 2 drops.")),)

            else:
                meds_typ = "medicine type kmn"
                reply = MessageFactory.text("What type of medicine is it?")
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

            
    async def dosage_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global prob
        global typessd
        global dosage_mls
        global med_name

        med_name = "vn svinsvn"
        dosage_mls = "mivivniinn"
        typessd = "vnoiwnvonvo"
        prob = "ssjnvisnv"

        if meds == "med name nibo":
            med_name= step_context.result
            med_type = predict_class(med_name)

            if med_type == "tablet":
                if option == "Recurring":
                    patientid = userId
                    pharmacyid = 1
                    tokens = token
                    pillName = med_name
                    pillType = "0"
                    dosage = "1"
                    isRecurring = "true"
                    pill_time = timess


                    dates_initial = cal_date(recur_dates[0], long_date)
                    if len(recur_dates) > 1:
                        dates_final = cal_date(recur_dates[-1], long_date)

                    dates_initials = []
                    dates_finals = []

                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 84:
                                break
    ##########################################################
                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 84:
                                break

                    final_days = []

                    if long_date == "Two Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 14):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass

                    if long_date == "Three Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 21):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass                        

                    if long_date == "1 Month":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 28):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass
                    if long_date == "2 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 56):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass   

                    if long_date == "3 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 84):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass 
                    if dosage_time == 1:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                    
                    if dosage_time >= 2:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)

                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your pill reminder has been set."))
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + "."))
                    return await step_context.end_dialog()

            if med_type == "capsule":
                if option == "Recurring":
                    patientid = userId
                    pharmacyid = 1
                    tokens = token
                    pillName = med_name
                    pillType = "2"
                    dosage = "1"
                    isRecurring = "true"
                    pill_time = timess


                    dates_initial = cal_date(recur_dates[0], long_date)
                    if len(recur_dates) > 1:
                        dates_final = cal_date(recur_dates[-1], long_date)

                    dates_initials = []
                    dates_finals = []

                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 84:
                                break
    ##########################################################
                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 84:
                                break

                    final_days = []

                    if long_date == "Two Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 14):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass

                    if long_date == "Three Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 21):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass                        

                    if long_date == "1 Month":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 28):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass
                    if long_date == "2 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 56):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass   

                    if long_date == "3 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 84):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass 
                    if dosage_time == 1:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                    
                    if dosage_time >= 2:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)

                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your pill reminder has been set."))
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + "."))
                    return await step_context.end_dialog()
            
            if med_type == "syrup":
                prob = "syrup dose koto"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)

            if med_type == "syringe":
                prob = "syringe dose koto"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)                

            if med_type == "drops":
                prob = "drop dose koto"
                await step_context.context.send_activity(
                    MessageFactory.text(f"How many drops are recommended by the doctor?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the quantity of drops. Hint- 2 drops.")),)

            else: 
                typessd = "types kmn"
                reply = MessageFactory.text("What type of medicine is it?")
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

        
        if dosage_ml == "dosage_ml koto":
            doses = step_context.result
            dose = str(doses)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time

            if dosage_times == 1:
                save_reminder_spec_days_one_syrup(patientid, pharmacyid, tokens, pillName, pill_time, dates, dose)
            else:
                save_reminder_spec_days_multi_syrup(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times, dose)   

            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(doses) + " of " + str(pillName) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()

        if dosage_ml == "dosage_ml koto_syringe":
            doses = step_context.result
            dose = str(doses)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time
            if dosage_times == 1:
                save_reminder_spec_days_one_syringe(patientid, pharmacyid, tokens, pillName, pill_time, dates, dose)
            else:
                save_reminder_spec_days_multi_syringe(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times, dose)   

            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(doses) + " of " + str(pillName) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()

        if dosage_ml == "dosage_ml koto drops":
            doses = step_context.result
            dose = str(doses)
            dose = dose.lower()
            dose = dose.replace(" drops", "").replace("drops", "").replace(" drop", "").replace("drop", "")
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time
            if dosage_times == 1:
                save_reminder_spec_days_one_drops(patientid, pharmacyid, tokens, pillName, pill_time, dates, dose)
            else:
                save_reminder_spec_days_multi_drops(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times, dose)   

            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(doses) + " of " + str(pillName) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()

        if meds_typ == "medicine type kmn":
            types = step_context.result
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time

            if types == "Tablet":
                if dosage_times == 1:
                    save_reminder_spec_days_one(patientid, pharmacyid, tokens, pillName, pill_time, dates)
                else:
                    save_reminder_spec_days_multi(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times)   

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time)+ "."))
                return await step_context.end_dialog()

            if types == "Capsule":
                if dosage_times == 1:
                    save_reminder_spec_days_one_capsule(patientid, pharmacyid, tokens, pillName, pill_time, dates)
                else:
                    save_reminder_spec_days_multi_capsule(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times)   

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time)+ "."))
                return await step_context.end_dialog()

            if types == "Syringe":
                dosage_mls = "dosage_ml koto_syringess"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)

            if types == "Syrup":
                dosage_mls = "dosage_ml koto_syrupss"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)

            if types == "Drop":
                dosage_mls = "dosage_ml koto_dropsaa"
                await step_context.context.send_activity(
                    MessageFactory.text(f"How many drops are recommended by the doctor?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the quantity of drops. Hint- 2 drops.")),)                


        

    async def dosage2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global dosu

        dosu = "vosvovn"

        if dosage_mls == "dosage_ml koto_syringess":
            doses = step_context.result
            dose = str(doses)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time
            if dosage_times == 1:
                save_reminder_spec_days_one_syringe(patientid, pharmacyid, tokens, pillName, pill_time, dates, dose)
            else:
                save_reminder_spec_days_multi_syringe(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times, dose)   

            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(doses) + " of " + str(pillName) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()

        if dosage_mls == "dosage_ml koto_syrupss":
            doses = step_context.result
            dose = str(doses)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time
            if dosage_times == 1:
                save_reminder_spec_days_one_syrup(patientid, pharmacyid, tokens, pillName, pill_time, dates, dose)
            else:
                save_reminder_spec_days_multi_syrup(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times, dose)   

            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(doses) + " of " + str(pillName) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()

        if dosage_mls == "dosage_ml koto_dropsaa":
            doses = step_context.result
            dose = str(doses)
            dose = dose.lower()
            dose = dose.replace(" drops", "").replace("drops", "").replace(" drop", "").replace("drop", "")
            patientid = userId
            pharmacyid = 1
            tokens = token
            pillName = meds_name
            pill_time = timess 
            dates = spec_dates
            dosage_times = dosage_time
            if dosage_times == 1:
                save_reminder_spec_days_one_drops(patientid, pharmacyid, tokens, pillName, pill_time, dates, dose)
            else:
                save_reminder_spec_days_multi_drops(patientid, pharmacyid, tokens, pillName, pill_time, dates, dosage_times, dose)   

            await step_context.context.send_activity(
                MessageFactory.text(f"Your pill reminder has been set."))
            await step_context.context.send_activity(
                MessageFactory.text("I will remind you to take " + str(doses) + " of " + str(pillName) + " at " + str(pill_time) + "."))
            return await step_context.end_dialog()

        if prob == "syrup dose koto":

            dosess = step_context.result
            dose = str(dosess)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            if option == "Recurring":
                patientid = userId
                pharmacyid = 1
                tokens = token
                pillName = med_name
                isRecurring = "true"
                pill_time = timess

                dates_initial = cal_date(recur_dates[0], long_date)
                if len(recur_dates) > 1:
                    dates_final = cal_date(recur_dates[-1], long_date)

                dates_initials = []
                dates_finals = []

                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 84:
                            break
##########################################################
                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 84:
                            break

                final_days = []

                if long_date == "Two Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 14):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass

                if long_date == "Three Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 21):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass                        

                if long_date == "1 Month":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 28):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass
                if long_date == "2 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 56):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass   

                if long_date == "3 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 84):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass 
                if dosage_time == 1:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                
                if dosage_time >= 2:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosess) + " of " + str(pillName) + " at " + str(pill_time) + "."))
                return await step_context.end_dialog()
        
        if prob == "syringe dose koto":
            dosess = step_context.result
            dose = str(dosess)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            if option == "Recurring":
                patientid = userId
                pharmacyid = 1
                tokens = token
                pillName = med_name
                isRecurring = "true"
                pill_time = timess

                dates_initial = cal_date(recur_dates[0], long_date)
                if len(recur_dates) > 1:
                    dates_final = cal_date(recur_dates[-1], long_date)

                dates_initials = []
                dates_finals = []

                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 84:
                            break
##########################################################
                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 84:
                            break

                final_days = []

                if long_date == "Two Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 14):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass

                if long_date == "Three Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 21):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass                        

                if long_date == "1 Month":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 28):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass
                if long_date == "2 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 56):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass   

                if long_date == "3 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 84):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass 
                if dosage_time == 1:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                
                if dosage_time >= 2:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosess) + " of " + str(pillName) + " at " + str(pill_time) + "."))
                return await step_context.end_dialog()

        if prob == "drop dose koto":
            doses = step_context.result
            dose = str(doses)
            dose = dose.lower()
            dose = dose.replace(" drops", "").replace("drops", "").replace(" drop", "").replace("drop", "")
            if option == "Recurring":
                patientid = userId
                pharmacyid = 1
                tokens = token
                pillName = med_name
                isRecurring = "true"
                pill_time = timess

                dates_initial = cal_date(recur_dates[0], long_date)
                if len(recur_dates) > 1:
                    dates_final = cal_date(recur_dates[-1], long_date)

                dates_initials = []
                dates_finals = []

                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 84:
                            break
##########################################################
                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 84:
                            break

                final_days = []

                if long_date == "Two Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 14):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass

                if long_date == "Three Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 21):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass                        

                if long_date == "1 Month":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 28):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass
                if long_date == "2 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 56):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass   

                if long_date == "3 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 84):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass 
                if dosage_time == 1:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                
                if dosage_time >= 2:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosess) + " of " + str(pillName) + " at " + str(pill_time) + "."))
                return await step_context.end_dialog()

        if typessd == "types kmn":
            typo = step_context.result
            if typo == "Tablet":
                if option == "Recurring":
                    patientid = userId
                    pharmacyid = 1
                    tokens = token
                    pillName = med_name
                    pillType = "0"
                    dosage = "1"
                    isRecurring = "true"
                    pill_time = timess

                    dates_initial = cal_date(recur_dates[0], long_date)
                    if len(recur_dates) > 1:
                        dates_final = cal_date(recur_dates[-1], long_date)

                    dates_initials = []
                    dates_finals = []

                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 84:
                                break
    ##########################################################
                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 84:
                                break

                    final_days = []

                    if long_date == "Two Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 14):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass

                    if long_date == "Three Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 21):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass                        

                    if long_date == "1 Month":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 28):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass
                    if long_date == "2 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 56):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass   

                    if long_date == "3 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 84):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass 
                    if dosage_time == 1:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_one_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                    
                    if dosage_time >= 2:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_multi_time(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)

                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your pill reminder has been set."))
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + "."))
                    return await step_context.end_dialog()

            if typo == "Capsule":
                if option == "Recurring":
                    patientid = userId
                    pharmacyid = 1
                    tokens = token
                    pillName = med_name
                    pillType = "2"
                    dosage = "1"
                    isRecurring = "true"
                    pill_time = timess

                    dates_initial = cal_date(recur_dates[0], long_date)
                    if len(recur_dates) > 1:
                        dates_final = cal_date(recur_dates[-1], long_date)

                    dates_initials = []
                    dates_finals = []

                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_initial)):
                            count += 1
                            dates_initials.append(dates_initial[i])
                            if count == 84:
                                break
    ##########################################################
                    if long_date == "1 Month":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 28:
                                break

                    if long_date == "2 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 56:
                                break

                    if long_date == "3 Months":
                        count = 0
                        for i in range(len(dates_final)):
                            count += 1
                            dates_finals.append(dates_final[i])
                            if count == 84:
                                break

                    final_days = []

                    if long_date == "Two Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 14):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass

                    if long_date == "Three Weeks":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 21):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initial or i in dates_final:
                                    final_days.append(i)
                                else:
                                    pass                        

                    if long_date == "1 Month":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 28):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass
                    if long_date == "2 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 56):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass   

                    if long_date == "3 Months":
                        for i in recur_dates:
                            recur_dates1 = i
                            recur_dates1 = recur_dates1.split("-")
                            date_list = []
                            for x in range(0, 84):
                                dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                                date_list.append(dates.strftime("%Y-%m-%d"))
                            for i in date_list:
                                if i in dates_initials or i in dates_finals:
                                    final_days.append(i)
                                else:
                                    pass 
                    if dosage_time == 1:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_one_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue)
                    
                    if dosage_time >= 2:
                        if long_date == "Two Weeks":
                            recurringValue = "2"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "Three Weeks":
                            recurringValue = "3"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "1 Month":
                            recurringValue = "4"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "2 Months":
                            recurringValue = "8"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)
                        if long_date == "3 Months":
                            recurringValue = "12"
                            save_reminder_multi_time_capsule(patientid, pharmacyid, tokens, pillName, pillType, dosage, pill_time, final_days, isRecurring, recurringValue, dosage_time)

                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your pill reminder has been set."))
                    await step_context.context.send_activity(
                        MessageFactory.text("I will remind you to take 1 dose of " + str(pillName) + " at " + str(pill_time) + " for " + str(long_date) + "."))
                    return await step_context.end_dialog()

            if typo == "Syrup":
                dosu = "syrup dose kotos"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)

            if typo == "Syringe":
                dosu = "syringe dose kotos"
                await step_context.context.send_activity(
                    MessageFactory.text(f"What's the recommended dosage in ml?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the dosage. Hint- 20 ml.")),)                

            if typo == "Drop":
                dosu = "drop dose kotos"
                await step_context.context.send_activity(
                    MessageFactory.text(f"How many drops are recommended by the doctor?"))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter the quantity of drops. Hint- 2 drops.")),)

    async def dosage3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if dosu == "syrup dose kotos":
            dosus = step_context.result
            dose = str(dosus)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            if option == "Recurring":
                patientid = userId
                pharmacyid = 1
                tokens = token
                pillName = med_name
                isRecurring = "true"
                pill_time = timess

                dates_initial = cal_date(recur_dates[0], long_date)
                if len(recur_dates) > 1:
                    dates_final = cal_date(recur_dates[-1], long_date)

                dates_initials = []
                dates_finals = []

                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 84:
                            break
##########################################################
                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 84:
                            break

                final_days = []

                if long_date == "Two Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 14):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass

                if long_date == "Three Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 21):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass                        

                if long_date == "1 Month":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 28):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass
                if long_date == "2 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 56):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass   

                if long_date == "3 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 84):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass 
                if dosage_time == 1:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_one_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                
                if dosage_time >= 2:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_multi_time_syrup(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosus) + " of " + str(pillName) + " at " + str(pill_time) + "."))
                return await step_context.end_dialog()

        if dosu == "syringe dose kotos":
            dosus = step_context.result
            dose = str(dosus)
            dose = dose.lower()
            dose = dose.replace(" ml", "").replace("ml", "")
            if option == "Recurring":
                patientid = userId
                pharmacyid = 1
                tokens = token
                pillName = med_name
                isRecurring = "true"
                pill_time = timess

                dates_initial = cal_date(recur_dates[0], long_date)
                if len(recur_dates) > 1:
                    dates_final = cal_date(recur_dates[-1], long_date)

                dates_initials = []
                dates_finals = []

                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 84:
                            break
##########################################################
                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 84:
                            break

                final_days = []

                if long_date == "Two Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 14):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass

                if long_date == "Three Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 21):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass                        

                if long_date == "1 Month":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 28):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass
                if long_date == "2 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 56):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass   

                if long_date == "3 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 84):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass 
                if dosage_time == 1:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_one_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                
                if dosage_time >= 2:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_multi_time_syringe(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosus) + " of " + str(pillName) + " at " + str(pill_time) + "."))
                return await step_context.end_dialog()


        if dosu == "drop dose kotos":
            dosus = step_context.result
            dose = str(dosus)
            dose = dose.lower()
            dose = dose.replace(" drops", "").replace("drops", "").replace(" drop", "").replace("drop", "")
            if option == "Recurring":
                patientid = userId
                pharmacyid = 1
                tokens = token
                pillName = med_name
                isRecurring = "true"
                pill_time = timess

                dates_initial = cal_date(recur_dates[0], long_date)
                if len(recur_dates) > 1:
                    dates_final = cal_date(recur_dates[-1], long_date)

                dates_initials = []
                dates_finals = []

                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_initial)):
                        count += 1
                        dates_initials.append(dates_initial[i])
                        if count == 84:
                            break
##########################################################
                if long_date == "1 Month":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 28:
                            break

                if long_date == "2 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 56:
                            break

                if long_date == "3 Months":
                    count = 0
                    for i in range(len(dates_final)):
                        count += 1
                        dates_finals.append(dates_final[i])
                        if count == 84:
                            break

                final_days = []

                if long_date == "Two Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 14):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass

                if long_date == "Three Weeks":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 21):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initial or i in dates_final:
                                final_days.append(i)
                            else:
                                pass                        

                if long_date == "1 Month":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 28):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass
                if long_date == "2 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 56):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass   

                if long_date == "3 Months":
                    for i in recur_dates:
                        recur_dates1 = i
                        recur_dates1 = recur_dates1.split("-")
                        date_list = []
                        for x in range(0, 84):
                            dates = date(int(recur_dates1[0]),int(recur_dates1[1]),int(recur_dates1[2])) + timedelta(days=7*x)
                            date_list.append(dates.strftime("%Y-%m-%d"))
                        for i in date_list:
                            if i in dates_initials or i in dates_finals:
                                final_days.append(i)
                            else:
                                pass 
                if dosage_time == 1:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_one_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dose)
                
                if dosage_time >= 2:
                    if long_date == "Two Weeks":
                        recurringValue = "2"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "Three Weeks":
                        recurringValue = "3"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "1 Month":
                        recurringValue = "4"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "2 Months":
                        recurringValue = "8"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)
                    if long_date == "3 Months":
                        recurringValue = "12"
                        save_reminder_multi_time_drop(patientid, pharmacyid, tokens, pillName, pill_time, final_days, isRecurring, recurringValue, dosage_time, dose)

                await step_context.context.send_activity(
                    MessageFactory.text(f"Your pill reminder has been set."))
                await step_context.context.send_activity(
                    MessageFactory.text("I will remind you to take " + str(dosus) + " of " + str(pillName) + " at " + str(pill_time) + "."))
                return await step_context.end_dialog()