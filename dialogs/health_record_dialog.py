from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs.choices import Choice
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt,PromptOptions
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from prompt.email_prompt import EmailPrompt
from dialogs.attachment_prompt import AttachmentPrompt
from user_info import check_email
from nlp_model.predict import predict_class
from health_record import save_health_record_1, save_health_record_2
import gspread


class HealthRecordDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(HealthRecordDialog, self).__init__(dialog_id or HealthRecordDialog.__name__)

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
                    self.upload_step,
                    self.upload2_step,
                    self.upload3_step,
                    self.upload4_step,
                    self.upload5_step,
                    self.upload6_step,
                    self.upload7_step,
                    self.upload8_step,
                    self.upload9_step,
                    self.upload10_step,
                    self.upload11_step,

                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def upload_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global pharmacyId

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
             
                
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(
                "You can take a snap or upload an image or PDF file. Please choose the document source."),)
        return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


    async def upload2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global urls1
        global ids1
        global upload2
        global userId

        urls1   = "url1 of imag"
        ids1    = "id1 of image"
        upload2 = "smnvosnsssss"

        userId = step_context.context.activity.from_property.id
        image = step_context.context.activity.additional_properties

        check = list(image.values())[0]
        
        if len(check) <= 10:
            ids1    = list(image.values())[0]
            urls1   = list(image.values())[1]
        else:
            ids1    = list(image.values())[1]
            urls1   = list(image.values())[0]  


        if image is not None:
            upload2 = "want to add more or not"
            await step_context.context.send_activity(
                MessageFactory.text("The files are uploaded successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)   



    async def upload3_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global upload3
        
        upload3 = "vnizviv"


        yesno = predict_class(step_context.result)

        if upload2 == "want to add more or not":
            print("entered14")
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


    async def upload4_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global urls2
        global ids2
        global upload4
        global reportType1

        reportType1 = "shellsssssss"
        upload4     = "nothing much"
        urls2       = "url of image"
        ids2        = "id of images"

        if upload3 == "choose options":
            upload4 = "kar report"
            reportType1 = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the report for? Please enter the patient name- ")),)          

        if upload3 == "add more/choose options":
            upload4 = "options choosing"
            image = step_context.context.activity.additional_properties

            check = list(image.values())[0]
            
            if len(check) <= 10:
                ids2    = list(image.values())[0]
                urls2   = list(image.values())[1]
            else:
                ids2    = list(image.values())[1]
                urls2   = list(image.values())[0] 

            listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
            return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))

    async def upload5_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload5
        global reportPatient1
        global reportType2

        upload5         = "step5aaaa"
        reportPatient1  = "patientaa"
        reportType2     = "typaaaaat"

        if upload4 == "kar report":
            pred = predict_class(step_context.result)
            if pred == "don't know":
                upload5 = "patient_name12"    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("It's the patient name. You can find it on the " + str(reportType1))),)

            else: 
                upload5 = "doctor name"
                reportPatient1 = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)

        if upload4 == "options choosing":
            upload5 = "patient name"
            reportType2 = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the report for? Please enter the patient name- ")),)


    async def upload6_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload6
        global reportDoctor1
        global reportPatient13
        global reportPatient2

        upload6         = "step6sss"
        reportDoctor1   = "vsmmvmss"
        reportPatient13 = "patientf"
        reportPatient2  = "acfafskm"

        if upload5 == "patient_name12":
            upload6 = "doc name13"
            reportPatient13 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you have consulted with?")),) 

        if upload5 == "doctor name":
            upload6 = "reportname"
            reportDoctor1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Enter a name to your report. It can be 'Blood Sugar Level report' or 'Malaria Report' etc.\n\nYou can also find it on the report.")),)

        if upload5 == "patient name":
            pred = predict_class(step_context.result)
            if pred == "don't know":
                upload6 = "patient_name"    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("It's the patient name. You can find it on the " + str(reportType2))),)

            else: 
                upload6 = "doctor name"
                reportPatient2 = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)


    async def upload7_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload7
        global reportDoctor13
        global reportName1
        global reportPatient21
        global reportDoctor2

        upload7         = "zknvlzknv"
        reportDoctor13  = "vxsvvsopm"
        reportName1     = "vsiopvnsa"
        reportPatient21 = "vpkgvw00w"
        reportDoctor2   = "fwofw0jf0"


        if upload6 == "doc name13":
            upload7 = "report name13"
            reportDoctor13 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Enter a name to your report. It can be 'Blood Sugar Level report' or 'Malaria Report' etc.\n\nYou can also find it on the report.")),)

        if upload6 == "reportname":
            pred = predict_class(step_context.result)
            if pred == "don't know":
                upload7 = "reportname again"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text('You can find it on the top of your report. It can be "Typhoid report" or "CBP" etc.')),)
            else:
                upload7 = "reportsummary"
                reportName1 = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload6 == "patient_name":
            upload7 = "doctor name nibo"
            reportPatient21 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)

        if upload6 == "doctor name":
            upload7 = "reportname--"
            reportDoctor2 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Enter a name to your report. It can be 'Blood Sugar Level report' or 'Malaria Report' etc.\n\nYou can also find it on the report.")),) 

    async def upload8_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload8
        global reportName12
        global reportName13
        global reportName2
        global reportDoctor21
 
        upload8         = "csomvsvww"
        reportName12    = "vfwkowfww"
        reportName13    = "aqsdfffff"
        reportName2     = "vsinvionv"
        reportDoctor21  = "vmmsinvnm"

        if upload7 == "report name13":
            pred = predict_class(step_context.result)
            if pred == "don't know":
                upload8 = "reportname again"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text('You can find it on the top of your report. It can be "Typhoid report" or "CBP" etc.')),)
            else:
                upload8 = "reportsummary13"
                reportName13 = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload7 == "reportname again":
            upload8 = "reportsummary2"
            reportName12 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload7 == "reportsummary":
            patientId = userId
            reportSummary1 = step_context.result
            save_health_record_1(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1, urls1, pharmacyId, token)            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()

        if upload7 == "reportname--":  
            pred = predict_class(step_context.result)
            if pred == "don't know":
                upload8 = "reportname again--"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text('You can find it on the top of your report. It can be "Typhoid report" or "CBP" etc.')),)
            else:
                upload8 = "reportsummary--"
                reportName2 = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload7 == "doctor name nibo":
            upload8 = "reportname nibo"
            reportDoctor21 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Enter a name to your report. It can be 'Blood Sugar Level report' or 'Malaria Report' etc.\n\nYou can also find it on the report.")),)


    async def upload9_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload9
        global reportName21
        global reportName212
        global reportName131

        upload9         = "snbxzcck"
        reportName21    = "smnvxzik"
        reportName212   = "smgdgdfg"
        reportName131   = "smnziziz"


        if upload8 == "reportname again--":
            upload9 = "reportsummary--test"
            reportName212 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)


        if upload8 == "reportsummary2":

            patientId = userId
            reportSummary12 = step_context.result
            save_health_record_1(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1, urls1, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()


        if upload8 == "reportsummary13":

            patientId = userId
            reportSummary13 = step_context.result
            save_health_record_1(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1, urls1, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()

        if upload8 == "reportsummary--":
            patientId = userId
            reportSummary2 = step_context.result            
            save_health_record_2(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1, urls1, ids2, urls2, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()


        if upload8 == "reportname nibo":
            pred = predict_class(step_context.result)
            if pred == "don't know":
                upload9 = "reportname again-2-"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text('You can find it on the top of your report. It can be "Typhoid report" or "CBP" etc.')),)
            else:
                upload9 = "reportsummary-2-"
                reportName21 = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)


        if upload8 == "reportname again":
            upload9 = "reportsummary132"
            reportName131 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)



    async def upload10_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload10
        global reportName22

        upload10 = "wsmvspmsvbmp0mv"
        reportName22 = "asmvpsmvm"

        if upload9 == "reportsummary-2-":
            patientId = userId
            reportSummary21 = step_context.result
            save_health_record_2(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1, urls1, ids2, urls2, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()


        if upload9 == "reportname again-2-":
            upload10 = "reportsummary-21-"
            reportName22 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)


        if upload9 == "reportsummary--test":
            patientId = userId
            reportSummary212 = step_context.result
            save_health_record_2(patientId, reportName212, reportSummary212, reportType2, reportDoctor2, reportPatient2, ids1, urls1, ids2, urls2, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()

        if upload9 == "reportsummary132":
            patientId = userId
            reportSummary131 = step_context.result
            print(patientId, reportName131, reportSummary131, reportType1, reportDoctor13, reportPatient13, ids1, urls1)
            save_health_record_1(patientId, reportName131, reportSummary131, reportType1, reportDoctor13, reportPatient13, ids1, urls1, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()


    async def upload11_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if upload10 == "reportsummary-21-":
            patientId = userId
            reportSummary22 = step_context.result
            save_health_record_2(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1, urls1, ids2, urls2, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            await step_context.context.send_activity(
                MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app."))                
            return await step_context.end_dialog()
                