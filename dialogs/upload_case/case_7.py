import gspread
from user_info import check_name
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from lib.message_factory import MessageFactory
from lib.card import CardAction
from prompt.email_prompt import EmailPrompt
from nlp_model.record_predict import predict_record
from dialogs.attachment_prompt import AttachmentPrompt
from health_record import save_health_record_1, save_health_record_2
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt,PromptOptions
from botbuilder.schema import ActionTypes, SuggestedActions


class caseSevenRecordDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseSevenRecordDialog, self).__init__(dialog_id or caseSevenRecordDialog.__name__)

        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(NumberPrompt(NumberPrompt.__name__))
        self.add_dialog(DatePrompt("date_prompt"))
        self.add_dialog(EmailPrompt("email_prompt"))
        self.add_dialog(TimePrompt("time_prompt"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(AttachmentPrompt(AttachmentPrompt.__name__))
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
                    self.seventh_step,
                    self.eighth_step,
                    self.ninth_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global wks
        global main
        global pharmacyId

        main = step_context.context.activity.text
        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        last = step_context.context.activity.text
        wks.update_acell("A7", str(last))

        pred = predict_record(last)

        try:
            wks.update_acell("H3", str(pred))
        except:
            pass

        global patient_name

        classes         = []
        patient_name    = []



        for x in pred.keys():
            if x == "PATIENT_NAME":
                names = pred[x]
                patient_name.append(names)
                classes.append(x)


        await step_context.context.send_activity(
            MessageFactory.text("Sure. Please upload the document.", extra = main))            
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(
                "Tap \U0001F4CE to upload", extra = main),)
        return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)  



    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global urls1a
        global ids1a

        urls1a = "ajnajnc"
        ids1a  = "smnkzxk"

        image = step_context.context.activity.additional_properties

        for i in image.keys():
            if i == "attachmentUrl":
                urls1a = image[i]
            if i == "attachmentId":
                ids1a = image[i]                

        if image is not None:
            await step_context.context.send_activity(
                MessageFactory.text("The file is uploaded successfully.", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?", extra = main)),)  


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
                

        global case1c
        case1c = "ksvkiw0s"

        respo = predict_class(step_context.result)
        
        if respo == "positive":
            case1c = "add more attachments"
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Please attach more files if you would like to upload them.", extra = main),
                retry_prompt=MessageFactory.text(
                    "The attachment must be in jpeg/png/pdf format.", extra = main),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
        
        else:
            case1c = "report_type should take"
            reply = MessageFactory.text("Okay! What best describes the report?", extra= main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Prescriptions",
                        type= ActionTypes.im_back,
                        value= "Prescriptions",
                        extra= main),
                    CardAction(
                        title= "Diagonstic Reports",
                        type= ActionTypes.im_back,
                        value= "Diagonstic Reports",
                        extra= main),
                    CardAction(
                        title= "Medical Claims",
                        type= ActionTypes.im_back,
                        value= "Medical Claims",
                        extra= main),
                ])
            return await step_context.context.send_activity(reply) 


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1d 
        global ids1b
        global urls1b
        global reportType1

        case1d          = "vshhshss" 
        ids1b           = "kafnnkad"
        urls1b          = "smvsvovs"
        reportType1     = "aninaini"

        if case1c == "add more attachments":
            
            image = step_context.context.activity.additional_properties

            for i in image.keys():
                if i == "attachmentUrl":
                    urls1b = image[i]
                if i == "attachmentId":
                    ids1b = image[i]        

            case1d = "report_type should take2"
            reply = MessageFactory.text("Okay! What best describes the report?", extra= main)
            reply.suggested_actions = SuggestedActions(
                actions=[
                    CardAction(
                        title= "Prescriptions",
                        type= ActionTypes.im_back,
                        value= "Prescriptions",
                        extra= main),
                    CardAction(
                        title= "Diagonstic Reports",
                        type= ActionTypes.im_back,
                        value= "Diagonstic Reports",
                        extra= main),
                    CardAction(
                        title= "Medical Claims",
                        type= ActionTypes.im_back,
                        value= "Medical Claims",
                        extra= main),
                ])
            return await step_context.context.send_activity(reply) 


        if case1c == "report_type should take":
            reportType1 = step_context.result
            case1d = "report_doctor should take"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),)    


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global case1e
        global reportType2
        global reportDoctor1

        case1e          = "aatetat"
        reportType2     = "aarwrwr"
        reportDoctor1   = "aauauaa"

        
        if case1d == "report_type should take2":
            reportType2 = step_context.result
            case1e      = "report_doctor should take2"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),)  

        if case1d == "report_doctor should take":
            reportDoctor1 = step_context.result
            case1e        = "report name should take"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(reportType1) + ".", extra = main)),)


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global case1f
        global reportName1
        global reportDoctor2

        case1f          = "alalala"
        reportName1     = "aoapapa"
        reportDoctor2   = "atatata"

        if case1e == "report_doctor should take2":
            reportDoctor2 = step_context.result
            case1f        = "report name should take2"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(reportType1) + ".", extra = main)),)            


        if case1e == "report name should take":
            reportName1 = step_context.result
            case1f = "summary asking"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?", extra = main)),)


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global case1g
        global reportName2

        case1g      = "akakaka"
        reportName2 = "awraaaa"
        
        if case1f == "report name should take2":
            reportName2 = step_context.result
            case1g = "summary asking2"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?", extra = main)),)

        if case1f == "summary asking":
            
            respo = predict_class(step_context.result)
            
            if respo == "positive":
                case1g = "add summary"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the report summary.", extra = main)),)
            else:
                selff = ["myself", "my", "i", "me"]
                if patient_name[0].lower() in selff:
                    namet = check_name(userId, token)
                    if namet == "not found":
                        namett = "User"
                        summary = ""
                        save_health_record_1(userId, reportName1, summary, reportType1, reportDoctor1, namett, ids1a, urls1a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(reportType1) + " has been uploaded successfully.", extra = main))

                        return await step_context.end_dialog()
                    else:
                        summary = ""
                        save_health_record_1(userId, reportName1, summary, reportType1, reportDoctor1, namet, ids1a, urls1a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(reportType1) + " has been uploaded successfully.", extra = main))

                        return await step_context.replace_dialog("passing") 
                else:
                    summary = ""
                    save_health_record_1(userId, reportName1, summary, reportType1, reportDoctor1, patient_name[0], ids1a, urls1a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(reportType1) + " has been uploaded successfully.", extra = main))

                    return await step_context.replace_dialog("passing")


    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1h 

        case1h = "aiaiaia"

        if case1g == "summary asking2":

            respos = predict_class(step_context.result)
            
            if respos == "positive":
                case1h = "add summary2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the report summary.", extra = main)),)
            else:
                selff = ["myself", "my", "i", "me"]
                if patient_name[0].lower() in selff:
                    namet = check_name(userId, token)
                    if namet == "not found":
                        namett = "User"
                        summary = ""
                        save_health_record_2(userId, reportName2, summary, reportType2, reportDoctor2, namett, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(reportType2) + " has been uploaded successfully.", extra = main))

                        return await step_context.replace_dialog("passing")
                    else:
                        summary = ""
                        save_health_record_2(userId, reportName2, summary, reportType2, reportDoctor2, namet, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(reportType2) + " has been uploaded successfully.", extra = main))

                        return await step_context.replace_dialog("passing")
                else:
                    summary = ""
                    save_health_record_2(userId, reportName2, summary, reportType2, reportDoctor2, patient_name[0], ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(reportType2) + " has been uploaded successfully.", extra = main))

                    return await step_context.end_dialog()



        if case1g == "add summary": 

            summarys = step_context.result
            selff = ["myself", "my", "i", "me"]
            if patient_name[0].lower() in selff:
                namet = check_name(userId, token)
                if namet == "not found":
                    namett = "User"
                    save_health_record_1(userId, reportName1, summarys, reportType1, reportDoctor1, namett, ids1a, urls1a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(reportType1) + " has been uploaded successfully.", extra = main))

                    return await step_context.replace_dialog("passing")
                else:
                    save_health_record_1(userId, reportName1, summarys, reportType1, reportDoctor1, namet, ids1a, urls1a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(reportType1) + " has been uploaded successfully.", extra = main))

                    return await step_context.replace_dialog("passing")
            else:
                save_health_record_1(userId, reportName1, summarys, reportType1, reportDoctor1, patient_name[0], ids1a, urls1a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(reportType1) + " has been uploaded successfully.", extra = main))

                return await step_context.end_dialog()


    async def ninth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if case1h == "add summary2":

            summarys = step_context.result
            selff = ["myself", "my", "i", "me"]

            if patient_name[0].lower() in selff:
                namet = check_name(userId, token)
                if namet == "not found":
                    namett = "User"
                    save_health_record_2(userId, reportName2, summarys, reportType2, reportDoctor2, namett, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(reportType2) + " has been uploaded successfully.", extra = main))

                    return await step_context.replace_dialog("passing")
                else:
                    save_health_record_2(userId, reportName2, summarys, reportType2, reportDoctor2, namet, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(reportType2) + " has been uploaded successfully.", extra = main))

                    return await step_context.replace_dialog("passing") 
            else:
                save_health_record_2(userId, reportName2, summarys, reportType2, reportDoctor2, patient_name[0], ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(reportType2) + " has been uploaded successfully.", extra = main))

                return await step_context.end_dialog()