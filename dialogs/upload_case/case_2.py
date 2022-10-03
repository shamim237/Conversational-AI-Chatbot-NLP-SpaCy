import gspread
from user_info import check_name
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from prompt.email_prompt import EmailPrompt
from lib.message_factory import MessageFactory
from nlp_model.record_predict import predict_record
from dialogs.attachment_prompt import AttachmentPrompt
from health_record import save_health_record_1, save_health_record_2
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt,PromptOptions



class caseTwoRecordDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseTwoRecordDialog, self).__init__(dialog_id or caseTwoRecordDialog.__name__)

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
        global report_type

        classes         = []
        patient_name    = []
        report_type     = []



        for x in pred.keys():
            if x == "PATIENT_NAME":
                name = pred[x]
                patient_name.append(name)
                classes.append(x)
            if x == "REPORT_TYPE":
                types = pred[x]
                report_type.append(types)
                classes.append(x)


        await step_context.context.send_activity(
            MessageFactory.text("Sure. Please upload the document.", extra = main))            
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(
                "Tap \U0001F4CE to upload", extra = main),)
        return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)  



    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global urls2a
        global ids2a

        urls2a = "ajnajnc"
        ids2a  = "smnkzxk"

        image = step_context.context.activity.additional_properties

        for i in image.keys():
            if i == "attachmentUrl":
                urls2a = image[i]
            if i == "attachmentId":
                ids2a = image[i]                

        if image is not None: 
            await step_context.context.send_activity(
                MessageFactory.text("The files are uploaded successfully.", extra = main))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?", extra = main)),)      

    
    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case2c
        global report_types_case2a

        report_types_case2a  = "vklmvmls"
        case2c               = "ksvkiw0s"
        
        
        respos = predict_class(step_context.result)
        
        if respos == "positive":
            case2c = "add more attachments_case2"
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Please attach more files you would like to uplaod", extra = main),
                retry_prompt=MessageFactory.text(
                    "The attachment must be a jpeg/png/pdf files.", extra = main),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
        
        else:
            pres    = ["prescriptions", "prescription"]
            med     = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia     = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

            if report_type[0].lower() in pres:
                report_types_case2a = "Prescriptions"
            if report_type[0].lower() in med:
                report_types_case2a = "Medical Claims"
            if report_type[0].lower() in dia:
                report_types_case2a = "Diagnostic Reports"  

            case2c = "report_name should take_case2"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(report_types_case2a) + ".", extra = main)),)   


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 2: upload my medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

        global case2d 
        global ids2b
        global urls2b
        global report_types_case2b
        global reportName2a

        case2d                  = "vknsuiss" 
        ids2b                   = "kafnnkad"
        urls2b                  = "smvsvovs"
        report_types_case2b     = "aninaini"
        reportName2a            = "skkvioss"

        if case2c == "add more attachments_case2":

            image = step_context.context.activity.additional_properties

            for i in image.keys():
                if i == "attachmentUrl":
                    urls2b = image[i]
                if i == "attachmentId":
                    ids2b = image[i]         

            pres = ["prescriptions", "prescription"]
            med = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

            if report_type[0].lower() in pres:
                report_types_case2b = "Prescriptions"
            if report_type[0].lower() in med:
                report_types_case2b = "Medical Claims"
            if report_type[0].lower() in dia:
                report_types_case2b = "Diagnostic Reports"  

            case2d = "report_name should take2_case2"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(report_types_case2b) + ".", extra = main)),)  

        if case2c == "report_name should take_case2":
            case2d = "doctor name should take_case2"
            reportName2a = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),)


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case2e
        global reportName2b 
        global reportDoctor2a

        case2e          = "shakskklm"
        reportName2b    = "isisvasal"
        reportDoctor2a  = "isjvjds9k"
        
        if case2d == "report_name should take2_case2":
            case2e = "doctor name should take2_case2"
            reportName2b = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),)

        if case2d == "doctor name should take_case2":
            case2e = "report summary should take_case2"
            reportDoctor2a = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add report summary?", extra = main)),)


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 2: upload my medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 
        
        global case2f
        global reportDoctor2b

        case2f          = "ssisiivv"
        reportDoctor2b  = "isvsiaal"

        if case2e == "doctor name should take2_case2":
            case2f = "report summary should take2_case2"
            reportDoctor2b = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add report summary?", extra = main)),)

        if case2e == "report summary should take_case2":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case2f = "report summary add korbe_case2"
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
                        save_health_record_1(userId, reportName2a, summary, report_types_case2a, reportDoctor2a, namett, ids2a, urls2a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case2a) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")
                    else:
                        summary = ""
                        save_health_record_1(userId, reportName2a, summary, report_types_case2a, reportDoctor2a, namet, ids2a, urls2a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case2a) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")
                else:
                    summary = ""
                    save_health_record_1(userId, reportName2a, summary, report_types_case2a, reportDoctor2a, patient_name[0], ids2a, urls2a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case2a) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 2: upload my medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

        global case2g
        case2g = "sivjijsi"
        
        if case2f == "report summary should take2_case2":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case2g = "report summary add korbe2_case2"
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
                        save_health_record_2(userId, reportName2b, summary, report_types_case2b, reportDoctor2b, namett, ids2a, urls2a, ids2b, urls2b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case2b) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing") 
                    else:
                        summary = ""
                        save_health_record_2(userId, reportName2b, summary, report_types_case2b, reportDoctor2b, namet, ids2a, urls2a, ids2b, urls2b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case2b) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")
                else:
                    summary = ""
                    save_health_record_2(userId, reportName2b, summary, report_types_case2b, reportDoctor2b, patient_name[0], ids2a, urls2a, ids2b, urls2b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case2b) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing") 

        if case2f == "report summary add korbe_case2":

            summarys = step_context.result
            selff = ["myself", "my", "i", "me"]
            if patient_name[0].lower() in selff:
                namet = check_name(userId, token)
                if namet == "not found":
                    namett = "User"
                    save_health_record_1(userId, reportName2a, summarys, report_types_case2a, reportDoctor2a, namett, ids2a, urls2a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case2a) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")
                else:
                    save_health_record_1(userId, reportName2a, summarys, report_types_case2a, reportDoctor2a, namet, ids2a, urls2a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case2a) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing") 
            else:
                save_health_record_1(userId, reportName2a, summarys, report_types_case2a, reportDoctor2a, patient_name[0], ids2a, urls2a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case2a) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()



    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 2: upload my medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

        if case2g == "report summary add korbe2_case2":

            summarys = step_context.result
            selff = ["myself", "my", "i", "me"]

            if patient_name[0].lower() in selff:
                namet = check_name(userId, token)
                if namet == "not found":
                    namett = "User"
                    save_health_record_2(userId, reportName2b, summarys, report_types_case2b, reportDoctor2b, namett, ids2a, urls2a, ids2b, urls2b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case2b) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")
                else:
                    save_health_record_2(userId, reportName2b, summarys, report_types_case2b, reportDoctor2b, namet, ids2a, urls2a, ids2b, urls2b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case2b) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")
            else:
                save_health_record_2(userId, reportName2b, summarys, report_types_case2b, reportDoctor2b, patient_name[0], ids2a, urls2a, ids2b, urls2b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case2b) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.end_dialog()