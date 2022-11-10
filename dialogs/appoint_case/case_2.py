import gspread
from date_regex import time_validate
from outlets import outlet_name
from user_info import check_name
from user_info import outlet_ids
from appointment import appoint_id, save_appoint, date_cal
from recognizers_suite import Culture
from datetime import datetime, timedelta
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from lib.message_factory import MessageFactory
from lib.card import CardAction
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class
from nlp_model.appoint_predict import predict_appoint
from outlets2 import get_pharmacist_id, get_slots_sup, pharmacist_name
from botbuilder.schema import ActionTypes, SuggestedActions
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
culture = Culture.English

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################


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
                    self.first_step,
                    self.scnd_step,
                    self.third_step,
                    self.fourth_step,
                    self.fifth_step,
                    self.sixth_step,
                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global wks
        global main
        global date
        global datex
        global token
        global timey
        global userId
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 
        timey = step_context.context.activity.additional_properties
        timey = timey.get('local_timestamp')

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        main = step_context.context.activity.text
        pred = predict_appoint(main)
        wks.update_acell("A17", str(pred))

        classes         = []
        date            = []

        for x in pred.keys():
            if x == "DATE":
                dates = pred[x]
                date.append(dates)
                classes.append(x)
                    
        datex = date_cal(date[0])
        
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("At what time would you like to consult?", extra = step_context.context.activity.text)),)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################
        global case2b
        global timesxx
        global outletId
        global endTimex
        global use_timex
        global doc_namex
        global outletNamex
        global pharmacistIdx
        global pharmacistsIds

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

            timex           = time_validate(step_context.result)
            outletId        = outlet_ids(userId, token)
            pharmacistsIds  = get_pharmacist_id(pharmacyId, outletId)         
            slotsx          = get_slots_sup(pharmacistsIds, datex, timex[0], timey, token)

            if slotsx is None:
                case2b = "different time2x"
                await step_context.context.send_activity(
                    MessageFactory.text("Sorry! All our pharmacists are occupied at the selected time.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to book the appointment at a different time?", extra = main)),)
            
            if slotsx == "time is past":
                case2b = "again time"
                await step_context.context.send_activity(
                    MessageFactory.text("I can only book appointments for times in the future.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("When do you want to book the appointment?", extra = main)),) 
            else:             
                doc_namex       = pharmacist_name(slotsx[1])  
                pharmacistIdx   = slotsx[1]
                userName        = check_name(userId, token) 
                outletNamex     = outlet_name(outletId, token)
                timesxx         = slotsx[0]
                ss              = datetime.strptime(timesxx, "%H:%M:%S")
                dd              = ss + timedelta(minutes= 15)
                endTimex        = datetime.strftime(dd, "%H:%M:%S")
                use_timex       = datetime.strptime(timesxx, "%H:%M:%S").strftime("%I:%M %p")


                if userName != "not found":
                    case2b = "confirm or notx"
                    await step_context.context.send_activity(
                        MessageFactory.text("Hey " + str(userName) + ", on " + str(datex) + " at " + str(use_timex) + ", " + str(doc_namex) + " of " + str(outletNamex) + " outlet is available.", extra = main))
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("On " + str(datex) + " at " + str(use_timex) + ", " + str(doc_namex) + " of " + str(outletNamex) + " outlet is available.", extra = main))            
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to confirm the appointment?", extra = main)),)


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

##########################################################################################################################################################################################################
############################################################## case-2: book an appointment on today ######################################################################################################

        global case2c 
        global doc_namexy
        global pharmacistIdy
        global userNamey
        global timesxy
        global use_timexy
        global endTimexy
        global outletNamexy 
        global appointId

        appointId       = "aayayyaaa"
        doc_namexy      = "aajhajahd"
        pharmacistIdy   = "ahahhaaaa"
        userNamey       = "sjsjsjsdc"
        timesxy         = "ssususuxx"
        use_timexy      = "asjsusuww"
        endTimexy       = "suusususx"
        outletNamexy    = "saususuax"
        case2c          = "ruauausss"

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

            if case2b == "confirm or notx":            
                msgsx = predict_class(step_context.result)
                if msgsx == "positive":
                    case2c = "question ask3x"
                    save_appoint(datex, timesxx, endTimex, userId, pharmacistIdx, doc_namex, pharmacyId, token)
                    appointId = appoint_id(userId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! Your appointment with " + str(doc_namex) + " has been booked on " + str(datex) + " at "  + str(use_timex) + ".", extra = main)) 
                    await step_context.context.send_activity(
                        MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?", extra = main)),)     

                else:
                    return await step_context.begin_dialog("book-appoint")  

            if case2b == "again time":
                timef  = time_validate(step_context.result)
                slotsxx = get_slots_sup(pharmacistsIds, datex, timef[0], timey, token)
                if slotsxx == "time is past":
                    await step_context.context.send_activity(
                        MessageFactory.text("Sorry! You have entered a time in the past! I can only book appointments for times in the future.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = main))

                    return await step_context.end_dialog()
                else:
                    doc_namexy       = pharmacist_name(slotsxx[1])  
                    pharmacistIdy   = slotsxx[1]
                    userNamey        = check_name(userId, token) 
                    outletNamexy     = outlet_name(outletId, token)
                    timesxy         = slotsxx[0]
                    ss              = datetime.strptime(timesxy, "%H:%M:%S")
                    dd              = ss + timedelta(minutes= 15)
                    endTimexy        = datetime.strftime(dd, "%H:%M:%S")
                    use_timexy       = datetime.strptime(timesxy, "%H:%M:%S").strftime("%I:%M %p")

                    if userNamey != "not found":
                        case2c = "confirm or notxy"
                        await step_context.context.send_activity(
                            MessageFactory.text("Hey " + str(userNamey) + ", on " + str(datex) + " at " + str(use_timexy) + ", " + str(doc_namexy) + " of " + str(outletNamexy) + " outlet is available.", extra = main))
                    else:
                        await step_context.context.send_activity(
                            MessageFactory.text("On " + str(datex) + " at " + str(use_timexy) + ", " + str(doc_namexy) + " of " + str(outletNamexy) + " outlet is available.", extra = main))            
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to confirm the appointment?", extra = main)),)                


            if case2b == "different time2x":
                msg2x = predict_class(step_context.result)
                if msg2x == "positive":
                    return await step_context.begin_dialog("book-appoint")
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = main))

                    return await step_context.replace_dialog("passing")


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1d
        global appointIdx

        appointIdx = "sjsjsus"
        case1d = "sjksksk"

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

            if case2c == "question ask3x":
                msgs = predict_class(step_context.result)
                if msgs == "positive":       
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = main))
                    reply = MessageFactory.text("go to question page", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= "go to question page",
                                type=ActionTypes.im_back,
                                value= str(appointId), 
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    return await step_context.replace_dialog("passing")   
                else:
                    case1d = "update or not2"
                    await step_context.context.send_activity(
                        MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition.", extra = main))    
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to update health profile now?", extra = main)),)     

            if case2c == "confirm or notxy":  
                msgsxy = predict_class(step_context.result)
                if msgsxy == "positive":
                    case1d = "question ask3xy"
                    save_appoint(datex, timesxy, endTimexy, userId, pharmacistIdy, doc_namexy, pharmacyId, token)
                    appointIdx = appoint_id(userId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! Your appointment with " + str(doc_namexy) + " has been booked on " + str(datex) + " at "  + str(use_timexy) + ".", extra = main)) 
                    await step_context.context.send_activity(
                        MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would  you like to attempt the questionnaire now?", extra = main)),)     

                else:
                    return await step_context.begin_dialog("book-appoint")              

    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1e
        case1e = "sjsjsjsj"

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

            if case1d == "update or not2":
                msg = predict_class(step_context.result) 

                if msg == "positive":
                    return await step_context.begin_dialog("health-profile") 
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Thanks for connecting with Jarvis Care.", extra = main))

                    return await step_context.replace_dialog("passing")

            if case1d == "question ask3xy":
                msgsc = predict_class(step_context.result)
                if msgsc == "positive":       
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = main))
                    reply = MessageFactory.text("go to question page", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= "go to question page",
                                type=ActionTypes.im_back,
                                value= str(appointIdx),
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    return await step_context.replace_dialog("passing")   
                else:
                    case1e = "update or not2x"
                    await step_context.context.send_activity(
                        MessageFactory.text("Keep your health profile updated. This will help pharmacist better assess your health condition.", extra = main))    
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to update health profile now?", extra = main)),) 
        

    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

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

            if case1e == "update or not2x":
                msg = predict_class(step_context.result) 
                if msg == "positive":
                    return await step_context.begin_dialog("health-profile") 
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Thanks for connecting with Jarvis Care.", extra = main))

                    return await step_context.replace_dialog("passing")