import gspread
from lib.card import CardAction
from user_info import check_user
from googletrans import Translator
from botbuilder.core import UserState
from prompt.time_prompt import TimePrompt
from prompt.date_prompt import DatePrompt
from prompt.email_prompt import EmailPrompt
from nlp_model.predict import predict_class, response
from lib.message_factory import MessageFactory
from dialogs.book_appointment import AppointmentDialog
from dialogs.adv_book_app_dialog import AdvBookAppDialog
from dialogs.adv_appoint_dialog import SupAdvBookAppDialog
from botbuilder.schema import ActionTypes, SuggestedActions
from dialogs.tobe_loggedin_dialog import ToBeLoggedInDialog
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog
from dialogs.simple_reminder_dialog import SimplePillReminderDialog
from dialogs.profile_update_dialog import HealthProfileDialog
from dialogs.adv_pill_remind_dialog import AdvPillReminderDialog
from dialogs.bypass_appoint_dialog import ByPassAppointmentDialog
from dialogs.adv_health_record_dialog import AdvHealthRecordDialog
from dialogs.upcoming_appoint_dialog import UpcomingAppointmentDialog
from dialogs.health_info_dialog import HealthInfoDialog
from dialogs.non_upapp_dialog import UploadNonInDialogApp
from dialogs.dialog_extra import DialogExtra
from dialogs.conv1 import Conv1Dialog
from dialogs.conv2 import Conv2Dialog
from botbuilder.dialogs import ComponentDialog, WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, DateTimePrompt, ChoicePrompt, PromptOptions
translator = Translator()



class UserProfileDialog(ComponentDialog):

    def __init__(self, user_state: UserState):
        super(UserProfileDialog, self).__init__(UserProfileDialog.__name__)
        self.user_profile_accessor = user_state.create_property("UserProfile")
        self.user_state = user_state
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.initial_step,
                    self.secnd_step,
                    # self.third_step,
                    # self.fourth_step,
                    # self.fifth_step,
                ],))
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(DateTimePrompt(DateTimePrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(DialogExtra("passing"))
        self.add_dialog(HealthInfoDialog("goodbad"))
        self.add_dialog(Conv1Dialog("conv1"))
        self.add_dialog(Conv2Dialog("conv2"))
        self.add_dialog(AppointmentDialog("book-appoint"))
        self.add_dialog(AdvBookAppDialog("early-book"))
        self.add_dialog(ByPassAppointmentDialog("bypass-appoint"))
        self.add_dialog(SupAdvBookAppDialog("spacy-book"))
        self.add_dialog(ToBeLoggedInDialog("login-process"))
        self.add_dialog(HealthRecordDialog("health-record"))
        self.add_dialog(PillReminderDialog("bypass-reminder"))
        self.add_dialog(SimplePillReminderDialog("pill-reminder"))
        self.add_dialog(AdvPillReminderDialog("adv-reminder"))
        self.add_dialog(AdvHealthRecordDialog("adv-record"))
        self.add_dialog(HealthProfileDialog("health-profile"))
        self.add_dialog(UpcomingAppointmentDialog("up-appoints"))
        self.add_dialog(UploadNonInDialogApp("bypass-record"))
        self.initial_dialog_id = "WFDialog"

        

    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global main
        global wks
        global pharmacyId
        global prompts

        prompts = "nothing"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        
        main = step_context.context.activity.text
        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role

        try:
            wks.update_acell("B1", str(userId))
            wks.update_acell("B30", str(token))
            wks.update_acell("B2", str(pharmacyId))
        except:
            pass
        
        status = check_user(userId, token)

        if userId == 0 or status == "Fail" or status == 400:
            return await step_context.begin_dialog("login-process")
        else:
            if status == "Success":
                msg = predict_class(step_context.context.activity.text)


                # if msg == "good":
                #     prompts = "Would you like to subscribe to a daily health tip from an expert?"
                #     await step_context.context.send_activity(
                #         MessageFactory.text("Okay. I am assuming that your health is well.", extra = main))
                #     reply = MessageFactory.text("Would you like my help with any of these?", extra = main)
                #     reply.suggested_actions = SuggestedActions(
                #         actions=[
                #             CardAction(
                #                 title= "Book an Appointment",
                #                 type=ActionTypes.im_back,
                #                 value= "Book an Appointment",
                #                 extra = main),
                #             CardAction(
                #                 title = "Pill Reminder",
                #                 type = ActionTypes.im_back,
                #                 value = "Pill Reminder",
                #                 extra = main),
                #             CardAction(
                #                 title = "Upload Health Records",
                #                 type = ActionTypes.im_back,
                #                 value = "Upload Health Records",
                #                 extra = main),
                #                 ])
                #     return await step_context.context.send_activity(reply)      

                # if msg == "bad":
                #     prompts = "Have you consulted with a Doctor/Pharmacist?"
                #     await step_context.context.send_activity(
                #         MessageFactory.text("Sorry to hear that!", extra = main))
                #     return await step_context.prompt(
                #         TextPrompt.__name__,
                #         PromptOptions(prompt=MessageFactory.text("Have you consulted with any Doctor or Pharmacist?", extra = main)),)
                
                # if msg == "morning":
                #     prompts = "morning"
                #     return await step_context.prompt(
                #         TextPrompt.__name__,
                #         PromptOptions(
                #             prompt=MessageFactory.text("Good Morning! How are you doing today?", extra = step_context.context.activity.text)),)
                
                # if msg == "afternoon":
                #     prompts = "afternoon"
                #     return await step_context.prompt(
                #         TextPrompt.__name__,
                #         PromptOptions(
                #             prompt=MessageFactory.text("Good Afternoon! How can I help you today?", extra = step_context.context.activity.text)),)
                
                # if msg == "evening":
                #     prompts = "evening"
                #     return await step_context.prompt(
                #         TextPrompt.__name__,
                #         PromptOptions(
                #             prompt=MessageFactory.text("Good Evening! How may I assist you today?", extra = step_context.context.activity.text)),)

                # if msg ==  "whatsup":
                #     prompts = "whatup"
                #     return await step_context.prompt(
                #         TextPrompt.__name__,
                #         PromptOptions(
                #             prompt=MessageFactory.text("I'm good. How about you?", extra = step_context.context.activity.text)),)

                # if msg == "meet":
                #     prompts = "meet"
                #     return await step_context.prompt(
                #         TextPrompt.__name__,
                #         PromptOptions(
                #             prompt=MessageFactory.text("Good to see you too. How may I help you today?", extra = step_context.context.activity.text)),)

                # if msg == "hey":
                #     prompts = "hey"
                #     return await step_context.prompt(
                #         TextPrompt.__name__,
                #         PromptOptions(
                #             prompt=MessageFactory.text("Hey there, how are you feeling today?", extra = step_context.context.activity.text)),)

                if msg == "appointment":
                    await step_context.context.send_activity(
                        MessageFactory.text("Let me check the earliest appointment slots for you.", extra = step_context.context.activity.text))
                    return await step_context.begin_dialog("early-book")

                if msg == "adv_appointment":
                    return await step_context.begin_dialog("adv-book")

                if msg == "reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
                    return await step_context.begin_dialog("pill-reminder") 

                if msg == "health_profile":
                    return await step_context.begin_dialog("health-profile") 

                if msg == "adv_pill_reminder":
                    await step_context.context.send_activity(
                        MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
                    return await step_context.begin_dialog("adv-reminder") 

                if msg == "adv_health_record":
                    return await step_context.begin_dialog("adv-record")  

                if msg == "upcoming_app":
                    await step_context.context.send_activity(
                        MessageFactory.text("Okay. Please let me check...", extra = main))
                    return await step_context.begin_dialog("up-appoints")

                if msg == "bypass_appoint":
                    return await step_context.begin_dialog("bypass-appoint")                                  

                else:
                    prompts = "nothing understand"
                    wks.update_acell("B27", str(msg))
                    wks.update_acell("B28", str(main))
                    resp = response(main)
                    wks.update_acell("B29", str(resp))
                    resp = resp.replace(". ", ".\n")
                    wks.update_acell("B30", str(resp))
                    resp = list(resp.split("\n"))
                    wks.update_acell("B31", str(resp))

                    if len(resp) == 1:
                        return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                prompt=MessageFactory.text(resp[0], extra = step_context.context.activity.text)),)
                    if len(resp) == 2:
                        await step_context.context.send_activity(
                            MessageFactory.text(resp[0], extra = main))                        
                        return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                prompt=MessageFactory.text(resp[1], extra = step_context.context.activity.text)),)
                    if len(resp) == 3:
                        await step_context.context.send_activity(
                            MessageFactory.text(resp[0], extra = main)) 
                        await step_context.context.send_activity(
                            MessageFactory.text(resp[1], extra = main))                         
                        return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                prompt=MessageFactory.text(resp[2], extra = step_context.context.activity.text)),)
                    # return await step_context.prompt(
                    #     TextPrompt.__name__,
                    #     PromptOptions(
                    #         prompt=MessageFactory.text("Can you please rephrase it for me?", extra = step_context.context.activity.text)),)

                    # return await step_context.prompt(
                    #     TextPrompt.__name__,
                    #     PromptOptions(
                    #         prompt=MessageFactory.text(resp, extra = step_context.context.activity.text)),)



    async def secnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        msg = predict_class(step_context.result)

        if msg == "appointment":
            await step_context.context.send_activity(
                MessageFactory.text("Let me check the earliest appointment slots for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("early-book")

        if msg == "adv_appointment":
            return await step_context.begin_dialog("adv-book")

        if msg == "reminder":
            await step_context.context.send_activity(
                MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("pill-reminder") 

        if msg == "health_profile":
            return await step_context.begin_dialog("health-profile") 

        if msg == "adv_pill_reminder":
            await step_context.context.send_activity(
                MessageFactory.text("Let me set a pill reminder for you.", extra = step_context.context.activity.text))
            return await step_context.begin_dialog("adv-reminder") 

        if msg == "adv_health_record":
            return await step_context.begin_dialog("adv-record")  

        if msg == "upcoming_app":
            await step_context.context.send_activity(
                MessageFactory.text("Okay. Please let me check...", extra = main))
            return await step_context.begin_dialog("up-appoints")

        if msg == "bypass_appoint":
            return await step_context.begin_dialog("bypass-appoint")                                  

        else:
            prompts = "nothing understand"
            wks.update_acell("C27", str(msg))
            wks.update_acell("C28", str(step_context.result))
            resp = response(step_context.result)
            wks.update_acell("C29", str(resp))
            resp = resp.replace(". ", ".\n")
            wks.update_acell("C30", str(resp))
            resp = list(resp.split("\n"))
            wks.update_acell("C31", str(resp))

            if len(resp) == 1:
                await step_context.context.send_activity(
                    MessageFactory.text(resp[0], extra = main)) 
                return await step_context.begin_dialog("conv1") 

            if len(resp) == 2:
                await step_context.context.send_activity(
                    MessageFactory.text(resp[0], extra = main))       
                await step_context.context.send_activity(
                    MessageFactory.text(resp[1], extra = main))                   
                return await step_context.begin_dialog("conv1") 

            if len(resp) == 3:
                await step_context.context.send_activity(
                    MessageFactory.text(resp[0], extra = main)) 
                await step_context.context.send_activity(
                    MessageFactory.text(resp[1], extra = main))   
                await step_context.context.send_activity(
                    MessageFactory.text(resp[2], extra = main))                       
                return await step_context.begin_dialog("conv1")      


    # async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
    #     global upload
    #     global book
    #     global anythings

    #     upload  = "39jnxonjnxn"
    #     book    = "auyayay"
    #     anythings = "cisdddb"        

    #     if prompts == "Would you like to subscribe to a daily health tip from an expert?":
    #         msgs = step_context.result
    #         if msgs == "Book an Appointment" or msgs == "Reservar una cita":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")
    #         if msgs == "Upload Health Records" or msgs == "Cargar registros de salud":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Okay. I am initializing the process of uploading health records!", extra = main))
    #             return await step_context.begin_dialog("health-record")
    #         if msgs == "Pill Reminder" or msgs == "Recordatorio de pastillas":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")  

    #     if prompts == "Have you consulted with a Doctor/Pharmacist?":
    #         msg = predict_class(step_context.result)
    #         if msg == "positive":
    #             upload = "asking 1st"
    #             return await step_context.prompt(
    #                 TextPrompt.__name__,
    #                 PromptOptions(prompt=MessageFactory.text("Would you like to save the prescription, or medical reports with me? I'll keep them all at one safe place.", extra = main)))
            
    #         if msg == "negative":
    #             book = "asking 1st"
    #             return await step_context.prompt(
    #                 TextPrompt.__name__,
    #                 PromptOptions(prompt=MessageFactory.text("I think you should see a Doctor or pharmacist. Would you like to book an appointment with a pharmacist?", extra = main)))
            
    #         if msg == "appointment":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")

    #         if msg == "reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")

    #         if msg == "health_profile":
    #             return await step_context.begin_dialog("health-profile")

    #         if msg == "adv_pill_reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("adv-reminder")

    #         if msg == "adv_health_record":
    #             return await step_context.begin_dialog("adv-record")

    #         if msg == "adv_appointment":
    #             return await step_context.begin_dialog("adv-book")

    #         if msg == "upcoming_app":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Okay. Please let me check...", extra = main))
    #             return await step_context.begin_dialog("up-appoints")

    #         if msg == "bypass_appoint":
    #             return await step_context.begin_dialog("bypass-appoint")

    #         else:
    #             anythings = "ki bole"
    #             return await step_context.prompt(
    #                 TextPrompt.__name__,
    #                 PromptOptions(prompt=MessageFactory.text("I can help you connect with a pharmacist, set a pill reminder, and upload health records. What would you like me to do?", extra = main)))

    #     if prompts == "nothing understand" or prompts == "morning" or prompts == "afternoon" or prompts == "evening" or prompts == "whatsup" or prompts == "meet" or prompts == "hey":
    #         msgk = predict_class(step_context.result)

    #         if msgk == "good":
    #             return await step_context.begin_dialog("goodbad")

    #         if msgk == "bad":
    #             return await step_context.begin_dialog("goodbad")

    #         if msgk == "appointment":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")
            
    #         if msgk == "reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")

    #         if msgk == "health_profile":

    #             return await step_context.begin_dialog("health-profile")

    #         if msgk == "adv_pill_reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("adv-reminder")

    #         if msgk == "adv_health_record":
    #             return await step_context.begin_dialog("adv-record")

    #         if msgk == "adv_appointment":
    #             return await step_context.begin_dialog("adv-book")

    #         if msgk == "upcoming_app":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Okay. Please let me check...", extra = main))
    #             return await step_context.begin_dialog("up-appoints")
            
    #         if msgk == "bypass_appoint":
    #             return await step_context.begin_dialog("bypass-appoint")

    #         else:
    #             upload = "asking 1st"
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Sorry, I can't help you with that! As a Jarvis Health assistant, I can help you with the things which are on the Jarvis APP!", extra = main))
    #             return await step_context.prompt(
    #                 TextPrompt.__name__,
    #                 PromptOptions(prompt=MessageFactory.text("Would you like to save the prescription, or medical reports with me? I'll keep them all at one safe place.", extra = main)))                
            
                

    # async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

    #     global prompts
    #     global more_work

    #     more_work = "buttons"


    #     if upload == "asking 1st":
    #         msg = step_context.result
    #         msg = predict_class(msg)

    #         if msg == "good" or msg == "bad":
    #             return await step_context.begin_dialog("goodbad")

    #         if msg == "positive":
    #             return await step_context.begin_dialog("health-record")

    #         if msg == "negative":
    #             more_work = "askin me"
    #             reply = MessageFactory.text("What would you like to do?", extra = main)
    #             reply.suggested_actions = SuggestedActions(
    #                 actions=[
    #                     CardAction(
    #                         title= "Book an Appointment",
    #                         type=ActionTypes.im_back,
    #                         value= "Book an Appointment",
    #                         extra = main),
    #                     CardAction(
    #                         title = "Pill Reminder",
    #                         type = ActionTypes.im_back,
    #                         value = "Pill Reminder",
    #                         extra = main),
    #                         ])
    #             return await step_context.context.send_activity(reply)

    #         if msg == "appointment":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")

    #         if msg == "reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")

    #         if msg == "health_profile":
    #             return await step_context.begin_dialog("health-profile")

    #         if msg == "adv_pill_reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("adv-reminder")

    #         if msg == "adv_health_record":
    #             return await step_context.begin_dialog("adv-record")

    #         if msg == "adv_appointment":
    #             return await step_context.begin_dialog("adv-book")

    #         if msg == "upcoming_app":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Okay. Please let me check...", extra = main))
    #             return await step_context.begin_dialog("up-appoints")

    #         if msg == "bypass_appoint":
    #             return await step_context.begin_dialog("bypass-appoint")

    #         else:
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Sorry! I am not able to understand.", extra = main))
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = main))
    #             return await step_context.end_dialog()

    #     if book == "asking 1st":
    #         msgt = predict_class(step_context.result)

    #         if msgt == "good" or msgt == "bad":
    #             return await step_context.begin_dialog("goodbad")

    #         if msgt  ==  "positive":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")

    #         if msgt == "negative":
    #             more_work = "dusking me"
    #             reply = MessageFactory.text("What would you like to do?", extra = main)
    #             reply.suggested_actions = SuggestedActions(
    #                 actions=[
    #                     CardAction(
    #                         title   = "Upload Health Records",
    #                         type    = ActionTypes.im_back,
    #                         value   = "Upload Health Records",
    #                         extra = main),
    #                     CardAction(
    #                         title   = "Pill Reminder",
    #                         type    = ActionTypes.im_back,
    #                         value   = "Pill Reminder",
    #                         extra = main),
    #                         ])
    #             return await step_context.context.send_activity(reply) 

    #         if msgt == "appointment":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")

    #         if msgt == "reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")

    #         if msgt == "health_profile":
    #             return await step_context.begin_dialog("health-profile")

    #         if msgt == "adv_pill_reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("adv-reminder")

    #         if msgt == "adv_health_record":
    #             return await step_context.begin_dialog("adv-record")

    #         if msgt == "adv_appointment":
    #             return await step_context.begin_dialog("adv-book")

    #         if msgt == "upcoming_app":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Okay. Please let me check...", extra = main))
    #             return await step_context.begin_dialog("up-appoints")

    #         if msgt == "bypass_appoint":
    #             return await step_context.begin_dialog("bypass-appoint")

    #         else:
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Sorry! I am not able to understand.", extra = main))
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = main))
    #             return await step_context.end_dialog()                

    #     if anythings == "ki bole":
    #         msgs = predict_class(step_context.result)

    #         if msgs == "good" or msgs == "bad":
    #             return await step_context.begin_dialog("goodbad")
                
    #         if msgs == "appointment":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")

    #         if msgs == "reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")

    #         if msg == "health_profile":
    #             return await step_context.begin_dialog("health-profile")

    #         if msgs == "adv_pill_reminder":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("adv-reminder")  

    #         if msg == "adv_health_record":
    #             return await step_context.begin_dialog("adv-record")

    #         if msg == "adv_appointment":
    #             return await step_context.begin_dialog("adv-book")

    #         if msg == "upcoming_app":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Okay. Please let me check...", extra = main))
    #             return await step_context.begin_dialog("up-appoints")     
            
    #         if msg == "bypass_appoint":
    #             return await step_context.begin_dialog("bypass-appoint") 

    #         else:
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Sorry! I am not able to understand.", extra = main))
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Thanks for connecting with Jarvis Care!", extra = main))
    #             return await step_context.end_dialog()        



    # async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


    #     if more_work == "askin me":
    #         msg = step_context.result
    #         if msg == "Book an Appointment" or msg == "Reservar una cita":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me check the earliest appointment slots for you.", extra = main))
    #             return await step_context.begin_dialog("early-book")
    #         if msg == "Pill Reminder" or msg == "Recordatorio de pastillas":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")

    #     if more_work == "dusking me":
    #         msg = step_context.result
    #         if msg == "Upload Health Records" or msg == "Cargar registros de salud":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Okay! I am initializing the health record upload process!", extra = main))
    #             return await step_context.begin_dialog("health-record")
    #         if msg == "Pill Reminder" or msg == "Recordatorio de pastillas":
    #             await step_context.context.send_activity(
    #                 MessageFactory.text("Let me set a pill reminder for you.", extra = main))
    #             return await step_context.begin_dialog("pill-reminder")
