from date_regex import date_validate
from date_regex import time_validate
from lib.message_factory import MessageFactory
from lib.card import CardAction
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from botbuilder.dialogs.choices import Choice
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from pill_reminder import get_patient_id
from outlets import check_outlet, outlet_name, get_avail_slot, get_timeslots, match, get_timeslots2, timeConversion
from user_info import check_email
from appointment import save_appoint, appoint_id
from botbuilder.dialogs.choices import Choice
from botbuilder.schema import ActionTypes, SuggestedActions
import gspread



class AppointmentDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "book-appoint"):
        super(AppointmentDialog, self).__init__(dialog_id or AppointmentDialog.__name__)

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
                    self.date_step,
                    self.pharmacist_step,
                    self.time_step,
                    self.slot_step,
                    self.save1_step,
                    self.save2_step,
                    self.save3_step,
                    self.save4_step,
                    self.save5_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId
        global main

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role  
        main = step_context.context.activity.text

        return await step_context.prompt(TextPrompt.__name__, PromptOptions(
            prompt=MessageFactory.text("On which date you would like to book an appointment?", extra = main)),)


    async def pharmacist_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global outletid
        global outletName
        global pharmacists
        global date
        global email


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

            date = date_validate(step_context.result)
            email = check_email(userId, token)
            outletid = check_outlet(email, pharmacyId, token)
            outletName = outlet_name(outletid, token)
            pharmacists = get_avail_slot(outletid, pharmacyId, token)
        
            if len(pharmacists) == 0:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! No slots are available for the selected outlet. Please try again after changing an outlet.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"In the meantime...", extra = main))
                return await step_context.begin_dialog("bypass-record") 
            
            if len(pharmacists) == 1:
                listofchoice = [Choice(pharmacists[0])]
                return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = main),choices=listofchoice))

            if len(pharmacists) == 2:
                listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1])]
                return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = main),choices=listofchoice))

            if len(pharmacists) == 3:
                listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2])]
                return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = main),choices=listofchoice))

            if len(pharmacists) == 4:
                listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3])]
                return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = main),choices=listofchoice))

            if len(pharmacists) == 5:
                listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3]), Choice(pharmacists[4])]
                return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = main),choices=listofchoice))

            if len(pharmacists) == 6:
                listofchoice = [Choice(pharmacists[0]),Choice(pharmacists[1]), Choice(pharmacists[2]), Choice(pharmacists[3]), Choice(pharmacists[4]), Choice(pharmacists[5])]
                return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Currently, the following pharmacists of " + str(outletName) + " are available for consultation", extra = main),choices=listofchoice))


    async def time_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global pharmacist


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
            pharmacist = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("At what time would you like to consult?", extra = main)),)


    async def slot_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global confirmation
        global timeslot
        global slot
        global ids
        global take_time

        take_time       = "sksmism"
        confirmation    = "aaa1aha"
        timeslot        = "aaa2ajj"


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

            timey = step_context.context.activity.additional_properties
            time_now = timey.get('local_timestamp')


            pharmas = pharmacist.lower()
            ids = match(pharmas, outletid, pharmacyId)
            time = time_validate(step_context.result)
            slot = get_timeslots(ids, date, time[0], time_now, token)
            
            if slot == "No slots available":
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("No slots are available for " + str(pharmacist) + " on " + str(date) + ". Please try another date or pharmacist!", extra = main)),)

            if slot == "NOPE":
                timeslot = "again"
                aslots = get_timeslots2(ids, date, token)

                reply = MessageFactory.text("Sorry!. Pharmacist is not available at " + str(time[0]) + ". Please choose a different time slot", extra = main)
                reply.suggested_actions = SuggestedActions(
                    actions=[
                        CardAction(
                            title= aslots[0],
                            type=ActionTypes.im_back,
                            value= aslots[0]),
                        CardAction(
                            title= aslots[1],
                            type=ActionTypes.im_back,
                            value= aslots[1]),
                        CardAction(
                            title= aslots[2],
                            type=ActionTypes.im_back,
                            value= aslots[2]),
                        CardAction(
                            title= aslots[3],
                            type=ActionTypes.im_back,
                            value= aslots[3]),])
                return await step_context.context.send_activity(reply) 

            if slot is None:
                take_time = "valid future time"
                await step_context.context.send_activity(
                    MessageFactory.text(f"You can't book an appointment on the past time!", extra = main)) 
                
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please enter an upcoming time at when you want consult to a pharmacist.", extra = main)),)                          
            
            else:
                confirmation = "confirm or not"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(slot) + " on " + str(date) + ". Shall I confirm the appointment?", extra = main)),)


    async def save1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global times
        global question
        global scnd_time
        global appointId1
        global wks
        global timeslot2
        global slott
        global idt
        global confirmation2
        
        slott           = "skskksss"
        timeslot2       = "kskvmkss"
        confirmation2   = "kjasnfsj"
        idt             = "sisiisis"
        appointId1       = "auauauau"

        question    = "ssiojgv"
        times       = "vmsovo"
        scnd_time   = "sinnsivn"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("A22", str(confirmation))

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

            if timeslot == "again":
                times = step_context.result
                scnd_time = "ask to save 2nd time"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(times) + " on " + str(date) + ". Shall I confirm the appointment?", extra = main)),)


            wks.update_acell("A23", str(confirmation))

            if confirmation == "confirm or not":
                msg = step_context.result
                confirm = predict_class(msg)

                if confirm == "positive":
                    question = "ask question"
                    time = slot.split(" - ")
                    time1 = timeConversion(time[0])
                    time2 = timeConversion(time[1])
                    patientId = step_context.context.activity.from_property.id
                    pharmacistId = ids
                    save_appoint(date[0], time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                    appointId1 = appoint_id(patientId, token)
                    await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on" + str(date) + ".", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would  you like to answer it now?", extra = main)),)

                else:
                    await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = main))

                    return await step_context.end_dialog()


            if take_time == "valid future time":

                timey = step_context.context.activity.additional_properties
                time_now = timey.get('local_timestamp')
                wks.update_acell("B29", str(time_now))
                time_scnds = time_validate(step_context.result)
                wks.update_acell("B30", str(time_scnds))
                pharmas = pharmacist.lower()
                idt = match(pharmas, outletid, pharmacyId)
                slott = get_timeslots(idt, date, time_scnds[0], time_now, token)
                wks.update_acell("B31", str(slott))

                if slott == "No slots available":
                    await step_context.context.send_activity(
                        MessageFactory.text("No slots are available for " + str(pharmacist) + " on " + str(date) + ". Please try another date or pharmacist!", extra = main))

                    return await step_context.end_dialog()

                if slott == "NOPE":
                    timeslot2 = "again2"
                    aslots = get_timeslots2(idt, date, token)
                    reply = MessageFactory.text("Sorry!. Pharmacist is not available at " + str(time_scnds[0]) + ". Please choose a different time slot", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= aslots[0],
                                type=ActionTypes.im_back,
                                value= aslots[0]),
                            CardAction(
                                title= aslots[1],
                                type=ActionTypes.im_back,
                                value= aslots[1]),
                            CardAction(
                                title= aslots[2],
                                type=ActionTypes.im_back,
                                value= aslots[2]),
                            CardAction(
                                title= aslots[3],
                                type=ActionTypes.im_back,
                                value= aslots[3]),])
                    return await step_context.context.send_activity(reply) 

                if slott is None:
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Sorry! You have failed to provide a valid time.", extra = main)) 

                    return await step_context.end_dialog()
                
                else:
                    confirmation2 = "confirm or not2"
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(slott) + " on " + str(date) + ". Shall I confirm the appointment?", extra = main)),)



    async def save2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global question2
        global appointId2
        global times2
        global scnd_time2 
        global question21
        global appointId3

        times2     = "ahshshs"
        appointId3 = "aajajjj"
        scnd_time2 = "sjkskns"
        question21 = "skkskss"

        appointId2 = "auauuau"
        question2 = "ksnvinsin"

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

            if question == "ask question":
                yesno = predict_class(step_context.result)

                if yesno == "positive":
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = main))

                    reply = MessageFactory.text("go to question page", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title   = "go to question page",
                                type    = ActionTypes.im_back,
                                value   = str(appointId1),
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    return await step_context.replace_dialog("passing")  

                else:
                    question2 = "health_profile update"
                    await step_context.context.send_activity(MessageFactory.text("Keep your health profile updated. This will help pharmacist to better assess your health condition.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to update health profile now?", extra = main)),)

            if scnd_time == "ask to save 2nd time":
                msgs = predict_class(step_context.result)

                if msgs == "positive":
                    wks.update_acell("G1", "entered")
                    wks.update_acell("G2", str(times))
                    timet = times.split(" - ")
                    wks.update_acell("G3", str(timet))
                    time1 = timeConversion(timet[0])
                    wks.update_acell("G4", str(time1[0]))
                    time2 = timeConversion(timet[1])
                    wks.update_acell("G5", str(time1[1]))
                    patientId = userId
                    wks.update_acell("G6", str(patientId))
                    pharmacistId = ids
                    wks.update_acell("G7", str(pharmacistId))
                    question2 = "questionnare ask2"
                    save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                    wks.update_acell("G8", "entered2")
                    appointId2 = appoint_id(patientId, token)
                    wks.update_acell("G9", "entered3")
                    wks.update_acell("G10", str(appointId2))
                    await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on " + str(date) + ".", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would  you like to answer it now?", extra = main)),)

                else:
                    await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = main))

                    return await step_context.end_dialog()




            if timeslot2 == "again2":
                times2 = step_context.result
                scnd_time2 = "ask to save 2nd time2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(str(pharmacist) + " is available at " + str(times2) + " on " + str(date) + ". Shall I confirm the appointment?", extra = main)),)

            if confirmation2 == "confirm or not2":

                msg = step_context.result
                confirm = predict_class(msg)

                if confirm == "positive":
                    question21 = "ask question2"
                    time = slott.split(" - ")
                    time1 = timeConversion(time[0])
                    time2 = timeConversion(time[1])
                    patientId = step_context.context.activity.from_property.id
                    pharmacistId = idt
                    save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                    appointId3 = appoint_id(patientId, token)
                    await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on " + str(date) + ".", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would  you like to answer it now?", extra = main)),)

                if confirm == "negative":
                    await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = main))

                    return await step_context.end_dialog()



    async def save3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global question3
        global question22
        global question24
        global appointId4

        question22 = "sskahah"
        appointId4 = "aujajaj"
        question24 = "ghshshh"
        question3 = "sknskl"

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
        
            if question2 == "health_profile update":

                msg = predict_class(step_context.result)

                if msg == "positive":
                    return await step_context.begin_dialog("health-profile") 
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = main))

                    return await step_context.replace_dialog("passing")   

            if question2 == "questionnare ask2":
                
                msg = predict_class(step_context.result)

                if msg == "positive":
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = main))
                    reply = MessageFactory.text("go to question page", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= "go to question page",
                                type=ActionTypes.im_back,
                                value= str(appointId2),
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    return await step_context.replace_dialog("passing")  

                else:
                    question3 = "health_profile update2"
                    await step_context.context.send_activity(MessageFactory.text("Keep your health profile updated. This will help pharmacist to better assess your health condition.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to update health profile now?", extra = main)),)



            if scnd_time2 == "ask to save 2nd time2":
                yesno = predict_class(step_context.result)
                if yesno == "positive":
                    timet = times2.split(" - ")
                    time1 = timeConversion(timet[0])
                    time2 = timeConversion(timet[1])
                    patientId = get_patient_id(email, pharmacyId)
                    pharmacistId = id
                    question22 = "questionnare ask22"
                    save_appoint(date, time1, time2, patientId, pharmacistId, pharmacist, pharmacyId, token)
                    appointId4 = appoint_id(patientId, token)
                    await step_context.context.send_activity(MessageFactory.text("Thank You! Your appointment with " + str(pharmacist) + " has been booked at " + str(time1) + " on " + str(date) + ".", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("It is recommended by the pharmacist to answer a questionnaire prior to the appointment.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would  you like to answer it now?", extra = main)),)

                else:
                    await step_context.context.send_activity(MessageFactory.text("Okay! I will not save your appointment.", extra = main))
                    await step_context.context.send_activity(MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = main))

                    return await step_context.end_dialog()

            if question21 == "ask question2":
                yesno = predict_class(step_context.result)
                if yesno == "positive":
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = main))
                    reply = MessageFactory.text("go to question page", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= "go to question page",
                                type=ActionTypes.im_back,
                                value= str(appointId3),
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    return await step_context.replace_dialog("passing")  

                else:
                    question24 = "health_profile update2"
                    await step_context.context.send_activity(MessageFactory.text("Keep your health profile updated. This will help pharmacist to better assess your health condition.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to update health profile now?", extra = main)),)


        
    async def save4_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global question32
        question32 = "usususka"

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

            if question3 == "health_profile update2":
                msg = predict_class(step_context.result)

                if msg == "positive":

                    return await step_context.begin_dialog("health-profile") 
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = main))

                    return await step_context.replace_dialog("passing") 

            if question22 == "questionnare ask22":
                msg = predict_class(step_context.result)
                if msg == "positive":
                    await step_context.context.send_activity(
                        MessageFactory.text("Thank You! I am opening the questionnare page.", extra = main))
                    reply = MessageFactory.text("go to question page", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= "go to question page",
                                type=ActionTypes.im_back,
                                value= str(appointId4),
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    return await step_context.replace_dialog("passing")  
                else:
                    question32 = "health_profile update22"
                    await step_context.context.send_activity(MessageFactory.text("Keep your health profile updated. This will help pharmacist to better assess your health condition.", extra = main))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Would you like to update health profile now?", extra = main)),)

            if question24 == "health_profile update2":
                msg = predict_class(step_context.result)

                if msg == "positive":
                    return await step_context.begin_dialog("health-profile") 
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = main))

                    return await step_context.replace_dialog("passing")   


    async def save5_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
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
            if question32 == "health_profile update22":
                msg = predict_class(step_context.result)

                if msg == "positive":
                    return await step_context.begin_dialog("health-profile") 
                else:
                    await step_context.context.send_activity(
                        MessageFactory.text("Thanks for connecting with Jarvis Care.", extra = main))
                    return await step_context.replace_dialog("passing") 