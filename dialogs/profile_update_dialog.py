from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt, PromptOptions
from nlp_model.predict import predict_class
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from dialogs.appoint_extra import AppointExtraDialog
from dialogs.health_record_dialog import HealthRecordDialog
from dialogs.pill_reminder_dialog import PillReminderDialog

class HealthProfileDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(HealthProfileDialog, self).__init__(dialog_id or HealthProfileDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))             
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(AppointExtraDialog(AppointExtraDialog.__name__))
        self.add_dialog(HealthRecordDialog(HealthRecordDialog.__name__))
        self.add_dialog(PillReminderDialog(PillReminderDialog.__name__))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(
            WaterfallDialog(
                "WFDialog",
                [
                    self.temp_step,
                    self.temp1_step,
                    self.temp2_step,
                    self.temp3_step,
                    self.temp4_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def temp_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global main
        global pharmacyId

        main  =  step_context.context.activity.text
        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role  

        return await step_context.prompt(
            NumberPrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("What's your body temperature in Celcius?", extra = main)),)

    async def temp1_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global profile1
        profile1 = "xkxksvk"

        temp  = step_context.result

        if "36.1" <= str(temp) <= "37.2" or "98.2" <= str(temp) <= "99.9":
            profile1 = "normal health"
            await step_context.context.send_activity(
                MessageFactory.text(f"Your body temperature is pretty normal.", extra = main))
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please measure your blood pressure using a BP (Blood Pressure) apparatus and share the BP readings.", extra = main)),)   

        if "37.3" <= str(temp) <= "38.9" or "100.0" <= str(temp) <= "100.4":
            profile1 = "mild fever"
            await step_context.context.send_activity(
                MessageFactory.text(f"Your body temperature shows you have mild fever.", extra = main))
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please measure your blood pressure using a BP (Blood Pressure) apparatus and share the BP readings.", extra = main)),) 

        if "39.0" <= str(temp) <= "40.6" or "100.4" <= str(temp) <= "102.6":
            profile1 = "high fever"
            await step_context.context.send_activity(
                MessageFactory.text(f"Your body temperature shows you have high fever. I suggest you should see a doctor or pharmacist.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text(f"Keep monitoring your temperature every three hours.", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("I can book an appointment with currently available pharmacist. Would you like book the appointment now?", extra = main)),)

        else:
            profile1 = "out of range"
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter a valid body temperature. It could be from 36-41 degree celcius.", extra = main)),)

    async def temp2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global profile2
        profile2 = "xkxksvkaaa"

        if profile1 == "normal health" or profile1 == "mild fever":
            bp = step_context.result
            if "60" < str(bp) <= "130":
                profile2 = "bp normal"
                return await step_context.prompt(
                    NumberPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Your blood pressure is normal. Please enter the pulse rate.", extra = main)),)
            
            if "130" < str(bp) <= "179":
                profile2 = "bp high"
                await step_context.context.send_activity(
                    MessageFactory.text("Your blood pressure is higher than normal.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Are you on medication and taking them on time?", extra = main)),)

            if str(bp) >= "180":
                await step_context.context.send_activity(
                    MessageFactory.text("Your blood pressure is higher than normal.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("You are in the state of emergency. Please call 911 or call for emergency help.", extra = main))
                return await step_context.end_dialog()            

        if profile1 == "high fever":
            yesno = predict_class(step_context.result)

            if yesno == "positive":
                profile2 = "emergency appointment"
                await step_context.context.send_activity(
                    MessageFactory.text("Okay! Let me search a emergency appointment slot for you!", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"I am initializing the appointment process!", extra = main))
                return await step_context.begin_dialog(AppointExtraDialog.__name__)

            if yesno == "negative":
                await step_context.context.send_activity(
                    MessageFactory.text("Okay! No problem, Please take care of yourself.", extra = main))
                return await step_context.end_dialog() 


        if profile1 == "out of range":
            
            temp  = step_context.result

            if "36.1" <= str(temp) <= "37.2" or "98.2" <= str(temp) <= "99.9":
                profile2 = "normal health2"
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your body temperature is pretty normal.", extra = main))
                return await step_context.prompt(
                    NumberPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please measure your blood pressure using a BP (Blood Pressure) apparatus and share the BP readings.", extra = main)),)   

            if "37.3" <= str(temp) <= "38.9" or "100.0" <= str(temp) <= "100.4":
                profile2 = "mild fever2"
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your body temperature shows you have mild fever.", extra = main))
                return await step_context.prompt(
                    NumberPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please measure your blood pressure using a BP (Blood Pressure) apparatus and share the BP readings.", extra = main)),) 

            if "39.0" <= str(temp) <= "40.6" or "100.4" <= str(temp) <= "102.6":
                profile2 = "high fever2"
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your body temperature shows you have high fever. I suggest you should see a doctor or pharmacist.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"Keep monitoring your temperature every three hours.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("I can book an appointment with currently available pharmacist. Would you like book the appointment now?", extra = main)),)
            


    async def temp3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:  

        global profile3
        profile3 = "xssvbs"  


        if profile2 == "bp normal":
            profile3 = "sugrar level"
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please share your blood sugar levels.", extra = main)),)
            
        if profile2 == "bp high":
            yesno = predict_class(step_context.result)
            if yesno == "positive":
                profile3 = "appointment"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to review your prescription with our pharmacist?", extra = main)),)

            if yesno == "negative":
                await step_context.context.send_activity(MessageFactory.text("No Problem. I can setup pill reminders for you, so you can never forget on your medication.", extra = main))  
                await step_context.context.send_activity(
                    MessageFactory.text(f"I am initializing the pill reminder process!", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)


        if profile2 == "normal health2" or profile2 == "mild fever2":

            bp = step_context.result
            if "110" <= str(bp) <= "130":
                profile3 = "bp normal2"
                return await step_context.prompt(
                    NumberPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Your blood pressure is normal. Please enter the pulse rate.", extra = main)),)
            
            if "130" < str(bp) <= "179":
                profile3 = "bp high2"
                await step_context.context.send_activity(
                    MessageFactory.text("Your blood pressure is higher than normal.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Are you on medication and taking them on time?", extra = main)),)

            if str(bp) >= "180":
                await step_context.context.send_activity(
                    MessageFactory.text("Your blood pressure is higher than normal.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("You are in the state of emergency. Please call 911 or call for emergency help.", extra = main))
                return await step_context.end_dialog() 


        if profile2 == "high fever2":
            yesno = predict_class(step_context.result)

            if yesno == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text("Okay! Let me search a emergency appointment slot for you!", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"I am initializing the appointment process!", extra = main))
                return await step_context.begin_dialog(AppointExtraDialog.__name__)

            if yesno == "negative":
                await step_context.context.send_activity(
                    MessageFactory.text("Okay! No problem, Please take care of yourself.", extra = main))
                return await step_context.end_dialog() 


    async def temp4_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global profile4
        profile4 = "xsdssvbs"  

        if profile3 == "appointment":
            yesno = predict_class(step_context.result)

            if yesno == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I'll help you with that.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"I am initializing the appointment process...", extra = main))
                return await step_context.begin_dialog(AppointExtraDialog.__name__)

            if yesno == "negative":    
                await step_context.context.send_activity(
                    MessageFactory.text("Okay. Thanks for connecting with jarvis!", extra = main))
                return await step_context.end_dialog()           
        
        if profile3 == "sugrar level":

            await step_context.context.send_activity(
                MessageFactory.text("Thank You! I will remember it for you.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("Thanks for connecting with jarvis!", extra = main))
            return await step_context.end_dialog()


        if profile3 == "bp normal2":
            profile4 = "sugrar level2"
            return await step_context.prompt(
                NumberPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please share your blood sugar levels.", extra = main)),)
            
        if profile3 == "bp high2":
            yesno = predict_class(step_context.result)
            if yesno == "positive2":
                profile4 = "appointment2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Would you like to review your prescription with our pharmacist?", extra = main)),)

            if yesno == "negative":
                await step_context.context.send_activity(MessageFactory.text("No Problem. I can setup pill reminders for you, so you can never forget on your medication.", extra = main))  
                await step_context.context.send_activity(
                    MessageFactory.text(f"I am initializing the pill reminder process!", extra = main))
                return await step_context.begin_dialog(PillReminderDialog.__name__)



    async def temp5_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        if profile4 == "appointment2":
            yesno = predict_class(step_context.result)

            if yesno == "positive":
                await step_context.context.send_activity(
                    MessageFactory.text(f"Okay! I'll help you with that.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text(f"I am initializing the appointment process...", extra = main))
                return await step_context.begin_dialog(AppointExtraDialog.__name__)

            if yesno == "negative":  
                await step_context.context.send_activity(
                    MessageFactory.text("Okay. Thanks for connecting with jarvis!", extra = main))
                return await step_context.end_dialog()            
        
        if profile4 == "sugrar level2":

            await step_context.context.send_activity(
                MessageFactory.text("Thank You! I will remember it for you.", extra = main))
            await step_context.context.send_activity(
                MessageFactory.text("Thanks for connecting with jarvis!", extra = main))
            return await step_context.end_dialog() 