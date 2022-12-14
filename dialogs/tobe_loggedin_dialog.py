import gspread
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from registration import new_user_id, register, new_token
from nlp_model.predict import predict_class
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.book_non_dialog import BookNonInDialog
from dialogs.non_upload_dialog import UploadNonInDialog
from dialogs.any_non_dialog import NonAnyDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.adv_health_record_dialog import AdvHealthRecordDialog
from validate_email import email_or_gmail, validateuser, user_id_email,  email_token
from username import check_name_email, check_passwrd_email
from reset_pass import sendcode, resetpass
from user_info import check_name
from validateotp import validatecode
from lib.message_factory import MessageFactory
from lib.card import CardAction
from dialogs.book_appointment import AppointmentDialog
from botbuilder.schema import ActionTypes, SuggestedActions
from dialogs.adv_appoint_dialog import SupAdvBookAppDialog

class ToBeLoggedInDialog(ComponentDialog):
    def __init__(self, dialog_id: str = "login-process"):
        super(ToBeLoggedInDialog, self).__init__(dialog_id or ToBeLoggedInDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(AppointmentDialog(AppointmentDialog.__name__))
        self.add_dialog(UploadNonInDialog(UploadNonInDialog.__name__))
        self.add_dialog(NonAnyDialog(NonAnyDialog.__name__))
        self.add_dialog(SupAdvBookAppDialog(SupAdvBookAppDialog.__name__))
        self.add_dialog(BookNonInDialog(BookNonInDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(AdvPillReminderDialog(AdvPillReminderDialog.__name__))
        self.add_dialog(AdvHealthRecordDialog(AdvHealthRecordDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.scnd2_step,
                    self.third_step,
                    self.fourths_step,
                    self.register_step,
                    self.reset1_step,
                    self.reset2_step,
                    self.reset3_step,
                    self.reset4_step,
                    self.reset5_step,
                    self.reset6_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"

    # async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

       
        # msg = predict_class(step_context.context.activity.text)
        # if msg == "morning":
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("Good Morning! How are you doing today?", extra = step_context.context.activity.text)),)
        # if msg == "afternoon":
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("Good Afternoon! How can I help you today?", extra = step_context.context.activity.text)),)
        # if msg == "evening":
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("Good Evening! How may I assist you today?", extra = step_context.context.activity.text)),)

        # if msg ==  "whatsup":
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("I'm good. How about you?", extra = step_context.context.activity.text)),)

        # if msg == "meet":
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("Good to see you too. How may I help you today?", extra = step_context.context.activity.text)),)

        # if msg == "hey":
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("Hey there, how are you feeling today?", extra = step_context.context.activity.text)),)

        # else:

        #     await step_context.context.send_activity(
        #         MessageFactory.text(f"Hello there! I am Jarvis, your personalized health assistant.", extra = step_context.context.activity.text))
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("How are you feeling today?", extra = step_context.context.activity.text)),)


    async def scnd2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global prompts

        global main

        main = step_context.context.activity.text
        prompts = "nothing"
        
        health = predict_class(main)

        if health == "good":
            prompts = "Would you like to subscribe to a daily health tip from an expert?"
            await step_context.context.send_activity(
                MessageFactory.text(f"Glad to hear it.\n\nHow can I help you today?", extra = main))
            reply = MessageFactory.text("Would you like my help with any of these?" , extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title = "Book an Appointment",
                        type  = ActionTypes.im_back,
                        value = "Book an Appointment",
                        extra = main),
                    CardAction(
                        title = "Pill Reminder",
                        type  = ActionTypes.im_back,
                        value = "Pill Reminder",
                        extra = main),
                    CardAction(
                        title = "Upload Health Records",
                        type  = ActionTypes.im_back,
                        value = "Upload Health Records",
                        extra = main),
                        ])
            return await step_context.context.send_activity(reply, step_context.result)  
        if health == "bad":
            prompts = "Have you consulted with a Doctor/Pharmacist?"
            await step_context.context.send_activity(
                MessageFactory.text(f"Sorry to hear that!", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("Have you consulted with any Doctor/Pharmacist?", extra = main)),)
        else:
            prompts = "What would you like to start with?"
            await step_context.context.send_activity(
                MessageFactory.text(f"I can help you connect with a pharmacist, set a pill reminder, and upload health records.", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("What would you like to start with?", extra = main)),)    


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global email1
        step_context.values["command"] = step_context.result 
        email1 =  "svomnmvosmn"

        if prompts == "Would you like to subscribe to a daily health tip from an expert?" or prompts == "What would you like to start with?" or prompts == "Have you consulted with a Doctor/Pharmacist?":
            email1 = "email taken"
            await step_context.context.send_activity(
                MessageFactory.text(f"Alright! But look like you are not logged in or registered yet with the Jarvis App.", extra = main))
            return await step_context.prompt(
                "email_prompt",
                PromptOptions(prompt=MessageFactory.text("Please enter your e-mail address.", extra = main)),)


    async def fourths_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global email
        global passwrd
        global login
        global names
        global pharmacyId

        pharmacyId = step_context.context.activity.from_property.name
        email = step_context.result

        passwrd = "jsvisvl"
        login = "siovnosnvn"
        names = "sivnsgvffg"


        if email1 == "email taken":
            status = validateuser(email, pharmacyId)
            status1 = email_or_gmail(email, pharmacyId)

            if status == "Fail" and status1 == "Fail" :
                login = "logged in"
                await step_context.context.send_activity(MessageFactory.text("Thank you for sharing your email address. Let's get you logged in.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("google login", extra = main)),)  

            if status == "Fail" and status1 == "Success":
                passwrd = "paswrd nibo"
                await step_context.context.send_activity(MessageFactory.text("Thank you for sharing your email address.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"Please enter your password to login or you can login manually.", extra = main)))

            if status == "Success":
                names = "name nite hbe2"
                await step_context.context.send_activity(MessageFactory.text("Thank you for sharing your email address.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text(f"Please enter your good name-", extra = main)))                
                            

    async def register_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global items
        global named
        global email
        global pharmacyId

        items = "ks vls vol" 
        named = "sicvsv"          

        if login == "logged in":

            userid = step_context.context.activity.from_property.id
            token  = step_context.context.activity.from_property.role
            name = check_name(userid, token)

            if name != "not found":
                await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully.", extra = main))
                if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                    job = predict_class(step_context.values["command"])
                    
                    if job == "appointment":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Please wait for a second...", extra = main))
                        return await step_context.begin_dialog(AppointmentDialog.__name__)

                    if job == "adv_health_record":
                        return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                    if job == "adv_appointment":
                        return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)
                        
                    if job == "reminder":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                        return await step_context.begin_dialog(PillReminderDialog.__name__)

                    if job == "adv_pill_reminder":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                        return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                    else:
                        return await step_context.begin_dialog(NonAnyDialog.__name__)

                if prompts == "What would you like to start with?":
                    job = predict_class(step_context.values["command"])
                    if job == "appointment":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Please wait for a second...", extra = main))
                        return await step_context.begin_dialog(AppointmentDialog.__name__)

                    if job == "adv_health_record":
                        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                        sh = ac.open("chatbot_logger")
                        wks = sh.worksheet("Sheet1")
                        wks.update_acell("H22", str(extra = main))
                        return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)
                    
                    if job == "adv_appointment":
                        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                        sh = ac.open("chatbot_logger")
                        wks = sh.worksheet("Sheet1")
                        wks.update_acell("L20", str(extra = main))
                        return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)
                    
                    if job == "reminder":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                        return await step_context.begin_dialog(PillReminderDialog.__name__)

                    if job == "adv_pill_reminder":
                        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                        sh = ac.open("chatbot_logger")
                        wks = sh.worksheet("Sheet1")
                        wks.update_acell("A2", str(step_context.values["command"]))
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                        return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                    else:
                        return await step_context.begin_dialog(NonAnyDialog.__name__)

                if prompts == "Have you consulted with a Doctor/Pharmacist?":
                    jobs = predict_class(step_context.values["command"])
                    
                    if jobs == "positive":
                        return await step_context.begin_dialog(UploadNonInDialog.__name__)
                    
                    if jobs == "negative":
                        return await step_context.begin_dialog(BookNonInDialog.__name__)
                    
                    if jobs == "appointment":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Please wait for a second...", extra = main))
                        return await step_context.begin_dialog(AppointmentDialog.__name__)

                    if jobs == "adv_health_record":
                        return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                    if jobs == "adv_appointment":
                        return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                    if jobs == "reminder":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                        return await step_context.begin_dialog(PillReminderDialog.__name__)

                    if jobs == "adv_pill_reminder":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                        return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

                    else:
                        return await step_context.begin_dialog(NonAnyDialog.__name__)
            else:
                named = "name nite hobe3e"
                await step_context.context.send_activity(MessageFactory.text("You've logged in successfully! But I can't find your name in the App!", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(prompt=MessageFactory.text("Please enter your good name-", extra = main)))                 

        if names == "name nite hbe2":
            name = step_context.result
            job = predict_class(step_context.values["command"])
            register(email,pharmacyId, name)
            id = new_user_id(email, pharmacyId)
            token = new_token(email, pharmacyId)

            await step_context.context.send_activity(
                MessageFactory.text("Thanks " + str(name) + ". You have registered successfully.", extra = main))
            reply = MessageFactory.text("do login", extra = main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= id,
                        type=ActionTypes.im_back,
                        value= token,
                        extra = main)])
            await step_context.context.send_activity(reply)

            if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            if prompts == "What would you like to start with?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

            if prompts == "Have you consulted with a Doctor/Pharmacist?":
                if job == "positive":               
                    return await step_context.begin_dialog(UploadNonInDialog.__name__)

                if job == "negative": 
                    return await step_context.begin_dialog(BookNonInDialog.__name__)

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)
 

        if passwrd == "paswrd nibo":
            password = step_context.result
            verify = check_passwrd_email(email, pharmacyId, password)

            if verify == "Success":
                name = check_name_email(email, pharmacyId, password) 
                if name is None:
                    items = "name nibo re"
                    await step_context.context.send_activity(
                        MessageFactory.text(f"You've logged in successfully. But I can't find your name in the APP.", extra = main))
                    userid = user_id_email(email, pharmacyId, password)
                    token = email_token(email, pharmacyId, password)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,
                                extra = main)])
                    await step_context.context.send_activity(reply)
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Please tell me your full name.", extra = main)),)
                else:
                    await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully!", extra = main))
                    userid = user_id_email(email, pharmacyId, password)
                    token = email_token(email, pharmacyId, password)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    job = predict_class(step_context.values["command"])

                    if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)

                    if prompts == "What would you like to start with?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

                    if prompts == "Have you consulted with a Doctor/Pharmacist?":
                        
                        if job == "positive":
                            return await step_context.begin_dialog(UploadNonInDialog.__name__)  

                        if job == "negative":
                            return await step_context.begin_dialog(BookNonInDialog.__name__)

                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)

            if verify == "Fail":
                items = "arekbar passwrd den"
                await step_context.context.send_activity(
                    MessageFactory.text(f"You've entered an incorrect password.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please enter the correct password", extra = main)),)                                       



    async def reset1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global port
        global email
        global pharmacyId
        port = "abcdefg"


        if named == "name nite hobe3e":
            if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                name = step_context.result
                job = predict_class(step_context.values["command"])
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks " + str(name) + ".", extra = main))
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)
            
            if prompts == "What would you like to start with?":
                name = step_context.result
                job = predict_class(step_context.values["command"])
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks " + str(name) + ".", extra = main))
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)
            
            if prompts == "Have you consulted with a Doctor/Pharmacist?":
                job = predict_class(step_context.values["command"])
                name = step_context.result
                await step_context.context.send_activity(
                    MessageFactory.text("Thanks " + str(name) + ".", extra = main))
                if job == "positive":
                    return await step_context.begin_dialog(UploadNonInDialog.__name__)
                
                if job == "negative":
                    return await step_context.begin_dialog(BookNonInDialog.__name__)

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)


        if items == "name nibo re":
            name = step_context.result
            job = predict_class(step_context.values["command"])
            await step_context.context.send_activity(MessageFactory.text("Thanks"+ str(name) + ".", extra = main))
            if prompts == "Would you like to subscribe to a daily health tip from an expert?":

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

            if prompts == "What would you like to start with?":

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

            if prompts == "Have you consulted with a Doctor/Pharmacist?":

                if job == "positive":
                    return await step_context.begin_dialog(UploadNonInDialog.__name__)

                if job == "negative":
                    return await step_context.begin_dialog(BookNonInDialog.__name__)

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)
        
        if items == "arekbar passwrd den":
            password = step_context.result
            verify = check_passwrd_email(email, pharmacyId, password)
            
            ############# if password is correct but name not given #############################
            if verify == "Success":
                name = check_name_email(email, pharmacyId, password)
                if name is None:
                    port = "ki ar kora, nam deya nai22"
                    await step_context.context.send_activity(
                        MessageFactory.text(f"You've logged in successfully.", extra = main))
                    userid = user_id_email(email, pharmacyId, password)
                    token = email_token(email, pharmacyId, password)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,
                                extra = main)])
                    await step_context.context.send_activity(reply)
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("But I can't find your name in the APP. Please tell me your full name.", extra = main)),)
                else:
                    await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully!", extra = main))
                    userid = user_id_email(email, pharmacyId, password)
                    token = email_token(email, pharmacyId, password)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,)])
                    await step_context.context.send_activity(reply)

                    job = predict_class(step_context.values["command"])

                    if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

                    if prompts == "What would you like to start with?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)

                    if prompts == "Have you consulted with a Doctor/Pharmacist?":
                        
                        if job == "positive":
                            return await step_context.begin_dialog(UploadNonInDialog.__name__)

                        if job == "negative":
                            return await step_context.begin_dialog(BookNonInDialog.__name__)

                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)
        
            
            if verify == "Fail":
                port = "reset pass kore den"
                await step_context.context.send_activity(
                    MessageFactory.text(f"You've entered an incorrect password.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Do you want me to reset the password?", extra = main)),) 


    async def reset2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global sorts
        global email
        global pharmacyId
        sorts = "vvnovnos"

        if port == "ki ar kora, nam deya nai22":
            name = step_context.result
            job = predict_class(step_context.values["command"])
            await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully!", extra = main))

            if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__) 

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

            if prompts == "What would you like to start with?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

            if prompts == "Have you consulted with a Doctor/Pharmacist?":
                if job == "positive":
                    return await step_context.begin_dialog(UploadNonInDialog.__name__)

                if job == "negative":
                    return await step_context.begin_dialog(BookNonInDialog.__name__)

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

        if port == "reset pass kore den":
            msg =  step_context.result
            msg = predict_class(msg)
            if msg == "positive":
                sorts = "reset kora otp dibe"
                sendcode(email, pharmacyId)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I am reseting your password.", extra = main))
                return await step_context.prompt(
                    NumberPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("I have send a code to your email. Please enter the code to reset your password.", extra = main)),)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! I can't let you login then!", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Please come again after login with the app.", extra = main))

                return await step_context.end_dialog()


    async def reset3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global dot
        global code
        global email
        global pharmacyId

        dot = "sdo ovonio"
        code = "sd vvi vo"

        if sorts == "reset kora otp dibe":
            codes = step_context.result
            code = int(codes)
            stats = validatecode(email, code, pharmacyId)
            if stats == "correct code":
                dot = "passwrd update kore dibo"
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for the OTP!", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please enter a new password!", extra = main)),)

            if stats == "incorrect code":
                dot = "otp nite hbe abr email user--"
                await step_context.context.send_activity(
                    MessageFactory.text(f"You have entered an invalid OTP.", extra = main))
                return await step_context.prompt(
                    NumberPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please try again!", extra = main)),) 


    async def reset4_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global pot
        global dot1
        global email
        global pharmacyId
        global code 

        dot1 = "vion vn vb"
        pot = "isniusn"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("F1", code)
        wks.update_acell("F2", email)
        wks.update_acell("F3", pharmacyId)

        if dot == "passwrd update kore dibo":
            passwords = step_context.result
            try:
                wks.update_acell("G1", str(passwords))
            except:
                pass
            send = resetpass(email, code, passwords, pharmacyId)
            wks.update_acell("G5", str(send))
            if send == "done":
                name = check_name_email(email, pharmacyId, passwords)
                wks.update_acell("G6", str(name))
                if name is None:
                    wks.update_acell("G7", str(name))
                    pot = "name niye asi"
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Thank You! Password updated successfully.", extra = main))
                    userid = user_id_email(email, pharmacyId, passwords)
                    token = email_token(email, pharmacyId, passwords)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,
                                extra = main)])
                    await step_context.context.send_activity(reply)
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("But I can't find your name in the APP. Please tell me your full name.", extra = main)),)
                else:                      
                    await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully!", extra = main))
                    userid = user_id_email(email, pharmacyId, passwords)
                    token = email_token(email, pharmacyId, passwords)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,
                                extra = main)])
                    await step_context.context.send_activity(reply)
                    
                    job = predict_class(step_context.values["command"])  

                    if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)

                    if prompts == "What would you like to start with?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)

                    if prompts == "Have you consulted with a Doctor/Pharmacist?":
                        if job == "positive":
                            return await step_context.begin_dialog(UploadNonInDialog.__name__)

                        if job == "negative":
                            return await step_context.begin_dialog(BookNonInDialog.__name__)

                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! I can't let you login then!", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Please come again after login with the app.", extra = main))

                return await step_context.end_dialog()
        
        if dot == "otp nite hbe abr email user--":
            codes = step_context.result
            code = int(codes)
            stats = validatecode(email, code, pharmacyId)
            if stats == "correct code":
                dot1 = "passwrd update kore dibo"
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thanks for the OTP!", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please enter a new password!", extra = main)),)
            else:
                await step_context.context.send_activity(
                    MessageFactory.text(f"Sorry! I can't let you login then!", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Please come again after login with the app.", extra = main))
                return await step_context.replace_dialog("passing")               

    async def reset5_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global pot1
        global code
        pot1 = "ios nvin vn "


        if pot == "name niye asi":
            name = step_context.result
            job = predict_class(step_context.values["command"]) 
            await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully!", extra = main))
            if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__) 

            if prompts == "What would you like to start with?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

            if prompts == "Have you consulted with a Doctor/Pharmacist?":
                if job == "positive":
                    return await step_context.begin_dialog(UploadNonInDialog.__name__)

                if job == "negative":
                    return await step_context.begin_dialog(BookNonInDialog.__name__)

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

        if dot1 == "passwrd update kore dibo":
            password = step_context.result
            code = int(code)
            send = resetpass(email, code, password, pharmacyId)

            if send == "done":
                name = check_name_email(email, pharmacyId, password)
                if name is None:
                    pot1 = "name niye asi"
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Thank You! Password updated successfully.", extra = main))
                    userid = user_id_email(email, pharmacyId, password)
                    token = email_token(email, pharmacyId, password)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,
                                extra = main)])
                    await step_context.context.send_activity(reply)
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("But I can't find your name in the APP. Please tell me your full name.", extra = main)),)
                else:                      
                    await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully!", extra = main))
                    userid = user_id_email(email, pharmacyId, password)
                    token = email_token(email, pharmacyId, password)
                    reply = MessageFactory.text("do login", extra = main)
                    reply.suggested_actions = SuggestedActions(
                        actions=[
                            CardAction(
                                title= userid,
                                type=ActionTypes.im_back,
                                value= token,
                                extra = main)])
                    await step_context.context.send_activity(reply)

                    job = predict_class(step_context.values["command"]) 

                    if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)

                    if prompts == "What would you like to start with?":
                        
                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)

                    if prompts == "Have you consulted with a Doctor/Pharmacist?":
                        
                        if job == "positive":
                            return await step_context.begin_dialog(UploadNonInDialog.__name__)

                        if job == "negative":
                            return await step_context.begin_dialog(BookNonInDialog.__name__)

                        if job == "appointment":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Please wait for a second...", extra = main))
                            return await step_context.begin_dialog(AppointmentDialog.__name__)

                        if job == "adv_health_record":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("H22", str(extra = main))
                            return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                        if job == "adv_appointment":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("L20", str(extra = main))
                            return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                        if job == "reminder":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(PillReminderDialog.__name__)

                        if job == "adv_pill_reminder":
                            ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                            sh = ac.open("chatbot_logger")
                            wks = sh.worksheet("Sheet1")
                            wks.update_acell("A2", str(step_context.values["command"]))
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                            return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                        else:
                            return await step_context.begin_dialog(NonAnyDialog.__name__)


    async def reset6_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        if pot1 == "name niye asi":
            name = step_context.result
            await step_context.context.send_activity(MessageFactory.text(str(name) + ", You have logged in successfully!", extra = main))
            job = predict_class(step_context.values["command"]) 

            if prompts == "Would you like to subscribe to a daily health tip from an expert?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

            if prompts == "What would you like to start with?":
                
                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("H22", str(extra = main))
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__)

                if job == "adv_appointment":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("L20", str(extra = main))
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                    sh = ac.open("chatbot_logger")
                    wks = sh.worksheet("Sheet1")
                    wks.update_acell("A2", str(step_context.values["command"]))
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)

            if prompts == "Have you consulted with a Doctor/Pharmacist?":
                
                if job == "positive":
                    return await step_context.begin_dialog(UploadNonInDialog.__name__)

                if job == "negative":
                    return await step_context.begin_dialog(BookNonInDialog.__name__)

                if job == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Please wait for a second...", extra = main))
                    return await step_context.begin_dialog(AppointmentDialog.__name__)

                if job == "adv_health_record":
                    return await step_context.begin_dialog(AdvHealthRecordDialog.__name__) 

                if job == "adv_appointment":
                    return await step_context.begin_dialog(SupAdvBookAppDialog.__name__)

                if job == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(PillReminderDialog.__name__)

                if job == "adv_pill_reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Okay. I am setting up a pill reminder!", extra = main))
                    return await step_context.begin_dialog(AdvPillReminderDialog.__name__)
                else:
                    return await step_context.begin_dialog(NonAnyDialog.__name__)
   