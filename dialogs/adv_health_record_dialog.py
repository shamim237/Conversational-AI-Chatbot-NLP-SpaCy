from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.choices import Choice
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt,PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from dialogs.attachment_prompt import AttachmentPrompt
from nlp_model.record_predict import predict_record
from nlp_model.predict import predict_class
from health_record import save_health_record_1, save_health_record_2
import gspread


class AdvHealthRecordDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(AdvHealthRecordDialog, self).__init__(dialog_id or AdvHealthRecordDialog.__name__)

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



                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId
        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        main = wks.acell("H22").value
        wks.update_acell("H1", main)

        pred = predict_record(main)

        try:
            wks.update_acell("H2", main)
            wks.update_acell("H3", str(pred))
        except:
            pass
        
        global patient_name
        global report_name
        global report_type


        classes         = []
        patient_name    = []
        report_name     = []
        report_type     = []

        for x in pred.keys():
            if x == "PATIENT_NAME":
                name = pred[x]
                patient_name.append(name)
                classes.append(x)
            if x == "REPORT_NAME":
                report = pred[x]
                report_name.append(report)
                classes.append(x)
            if x == "REPORT_TYPE":
                types = pred[x]
                report_type .append(types)
                classes.append(x)

        global case1i 
        case1i = "ksksksk"

        
        # upload my mom's blood sugar report
        if "PATIENT_NAME" in classes and "REPORT_NAME" in classes and "REPORT_TYPE" not in classes:
            case1i = "image upload"
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "You can take a snap or upload an image or PDF file. Please choose the document source."),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global upload2
        global urls1
        global ids1
        upload2 = "smnvosn"
        urls1 = "url of image"
        ids1 = "id of image"

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        if case1i == "image upload":

            image = step_context.context.activity.additional_properties

            try:
                wks.update_acell("D6", str(type(image)))
                wks.update_acell("E6", str(image))
            except:
                pass

            ids1 = list(image.values())[0]
            urls1 = list(image.values())[1]

            if image is not None:
                upload2 = "want to add more or not"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global upload3        
        upload3 = "vnizviv"

        yesno = predict_class(step_context.result)

        if upload2 == "want to add more or not":
            if yesno == "positive":
                upload3 = "add more/choose options"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "Please attach more files you would like to uplaod"),
                    retry_prompt=MessageFactory.text(
                        "The attachment must be a jpeg/png/pdf files."),)

                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
            else:
                upload3 = "choose options"
                listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
                return await step_context.prompt((ChoicePrompt.__name__),
                    PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))

    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global urls2
        global ids2
        global upload4
        global reportType

        reportType = "shell"
        upload4 = "nothing much"
        urls2 = "url of image"
        ids2 = "id of image"

        if upload3 == "choose options":
            upload4 = "doctor name"
            reportType = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)          

        if upload3 == "add more/choose options":
            upload4 = "options choosing"
            image = step_context.context.activity.additional_properties

            ids2 = list(image.values())[0]
            urls2 = list(image.values())[1]

            listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
            return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload5
        global reportType2
        global doctor

        doctor = "sklvnsvn"
        upload5 = "step5"
        reportType2 = "type of report"

        if upload4 == "doctor name":
            upload5 = "report summary"  
            doctor = step_context.result  
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload4 == "options choosing":
            upload5 = "doctor name2"
            reportType2 = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)    

    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload6
        global doctori
        doctori = 'ksnsm'
        upload6 = "snkln"

        if upload5 == "report summary":
            patientId = userId
            reportSummary = step_context.result

            save_health_record_1(patientId, report_name[0], reportSummary, reportType, doctor, patient_name[0], ids1, urls1, pharmacyId, token)               
            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

        if upload5 == "doctor name2":
            upload6 = "report summary"  
            doctori = step_context.result  
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if upload6 == "report summary":
            patientId = userId
            reportSummary = step_context.result

            save_health_record_2(patientId, report_name[0], reportSummary, reportType2, doctori, patient_name[0], ids1, urls1, ids2, urls2, pharmacyId, token)              
            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 