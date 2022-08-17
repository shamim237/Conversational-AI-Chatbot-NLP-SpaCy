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
from health_record import save_health_record_1, save_health_record_2, save_health_record_3, save_health_record_4, save_health_record_5
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

        ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
        sh = ac.open("logs_checker")
        wks = sh.worksheet("Sheet1")

        try:
            wks.update_acell("B5", str(step_context.context.activity))
        except:
            pass               
                
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(
                "You can take a snap or upload an image or PDF file. Please choose the document source."),
            # retry_prompt=MessageFactory.text(
            #     "The attachment must be a jpeg/png/pdf files."),
            )
        return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

    async def upload2_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global email
        global urls1
        global ids1
        global upload2
        global userId

        urls1 = "url1 of image"
        ids1 = "id1 of image"
        upload2 = "smnvosn"

        ac = gspread.service_account("sheetlogger-357104-9747ccb595f6.json")
        sh = ac.open("logs_checker")
        wks = sh.worksheet("Sheet1")   

        userId = step_context.context.activity.from_property.id
        email = check_email(userId, token)

        image = step_context.context.activity.additional_properties

        try:
            wks.update_acell("A6", str(type(image)))
            wks.update_acell("B6", str(image))
        except:
            pass

        ids1 = list(image.values())[0]
        urls1 = list(image.values())[1]


        try:
            wks.update_acell("B7", " ".join(urls1))
            wks.update_acell("B8", " ".join(ids1))
        except:
            pass

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
        global add_more
        
        upload3 = "vnizviv"


        yesno = predict_class(step_context.result)

        if upload2 == "want to add more or not":
            print("entered14")
            if yesno == "positive":
                add_more = "add more"
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

        reportType1 = "shell"
        upload4 = "nothing much"
        urls2 = "url of image"
        ids2 = "id of image"

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

            ids2 = list(image.values())[0]
            urls2 = list(image.values())[1]

            listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
            return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))

    async def upload5_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload5
        global reportPatient1
        global reportType2

        upload5 = "step5"
        reportPatient1 = "patient!!!"
        reportType2 = "type of report"

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

        upload6 = "step6"
        reportDoctor1 = "vsmmvm"
        reportPatient13 = "patientfskms9"
        reportPatient2 = "acfafskms9"

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

        upload7 = "zknvlzknv"
        reportDoctor13 = ";vxsvvsopm"
        reportName1 =  "vsiopvnsp0vnpjn"
        reportPatient21 = "vpkgvw00w"
        reportDoctor2 = "fwofw0jf0w"


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
            upload7 == "reportname--"
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


        upload8 = "csomvsv"
        reportName12 = "vfwkowf"
        reportName13 = "WFWKFM WPM FOPM"
        reportName2 = "vsinvionvb"
        reportDoctor21 = "vmmsinvnmvjm"

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
            # if len(urls1) == 1:
            print(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1, urls1)
            save_health_record_1(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1, urls1, pharmacyId, token)
            # if len(urls1) == 2:
            #     print(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1])
            #     save_health_record_2(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], pharmacyId, token)
            # if len(urls1) == 3:
            #     print(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2])
            #     save_health_record_3(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], pharmacyId, token)
            # if len(urls1) == 4:
            #     print(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3])
            #     save_health_record_4(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], pharmacyId, token)
            # if len(urls1) == 5:
            #     print(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids1[4], urls1[4])
            #     save_health_record_5(patientId, reportName1, reportSummary1, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids1[4], urls1[4], pharmacyId, token)               
            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

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

        upload9 = "sninovnnvb"
        reportName21 = "smnv  k ovn"

        if upload8 == "reportsummary2":

            patientId = userId
            reportSummary12 = step_context.result
            # if len(urls1) == 1:
            print(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1, urls1)
            save_health_record_1(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1, urls1, pharmacyId, token)
            # if len(urls1) == 2:
            #     print(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1])
            #     save_health_record_2(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], pharmacyId, token)
            # if len(urls1) == 3:
            #     print(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2])
            #     save_health_record_3(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], pharmacyId, token)
            # if len(urls1) == 4:
            #     print(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3])
            #     save_health_record_4(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], pharmacyId, token)
            # if len(urls1) == 5:
            #     print(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids1[4], urls1[4])
            #     save_health_record_5(patientId, reportName12, reportSummary12, reportType1, reportDoctor1, reportPatient1, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids1[4], urls1[4], pharmacyId, token)  
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)


        if upload8 == "reportsummary13":

            patientId = userId
            reportSummary13 = step_context.result
            # if len(urls1) == 1:
            print(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1, urls1)
            save_health_record_1(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1, urls1, pharmacyId, token)
            # if len(urls1) == 2:
            #     print(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1])
            #     save_health_record_2(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1], pharmacyId, token)
            # if len(urls1) == 3:
            #     print(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2])
            #     save_health_record_3(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], pharmacyId, token)
            # if len(urls1) == 4:
            #     print(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3])
            #     save_health_record_4(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], pharmacyId, token)
            # if len(urls1) == 5:
            #     print(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids1[4], urls1[4])
            #     save_health_record_5(patientId, reportName13, reportSummary13, reportType1, reportDoctor13, reportPatient13, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids1[4], urls1[4], pharmacyId, token)  
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)

        if upload8 == "reportsummary--":
            patientId = userId
            reportSummary2 = step_context.result            
            if add_more == "add more":
                # if len(urls1) == 1 and len(urls2) == 1:
                print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1, urls1, ids2, urls2)
                save_health_record_2(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1, urls1, ids2, urls2, pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 2:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_3(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 1:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0])
                #     save_health_record_3(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 2:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_4(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 1:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0])
                #     save_health_record_4(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 2:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 3:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 3:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_4(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 3:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 1:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 2:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)    
                # if len(urls1) == 4 and len(urls2) == 3:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 4:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], ids2[3], urls2[3])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], ids2[3], urls2[3], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 4:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 4:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 4:
                #     print(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName2, reportSummary2, reportType2, reportDoctor2, reportPatient2, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)

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

    async def uploa10_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload10
        global reportName22

        upload10 = "wsmvspmsvbmp0mv"
        reportName22 = "asmvpsmvm"

        if upload9 == "reportsummary-2-":
            patientId = userId
            reportSummary21 = step_context.result
            if add_more == "add more":
                # if len(urls1) == 1 and len(urls2) == 1:
                print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1, urls1, ids2, urls2)
                save_health_record_2(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1, urls1, ids2, urls2, pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 2:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_3(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 1:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0])
                #     save_health_record_3(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 2:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_4(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 1:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0])
                #     save_health_record_4(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 2:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 3:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 3:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_4(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 3:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 1:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 2:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)    
                # if len(urls1) == 4 and len(urls2) == 3:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 4:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], ids2[3], urls2[3])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], ids2[3], urls2[3], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 4:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 4:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 4:
                #     print(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName21, reportSummary21, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)

        if upload9 == "reportname again-2-":
            upload10 = "reportsummary-21-"
            reportName22 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

    async def upload11_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if upload10 == "reportsummary-21-":
            patientId = userId
            reportSummary22 = step_context.result
            if add_more == "add more":
                # if len(urls1) == 1 and len(urls2) == 1:
                print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1, urls1, ids2, urls2)
                save_health_record_2(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1, urls1, ids2, urls2, pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 2:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_3(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 1:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0])
                #     save_health_record_3(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 2:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_4(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 1:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0])
                #     save_health_record_4(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 2:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 3:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 3:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_4(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 3:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 1:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 2:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)    
                # if len(urls1) == 4 and len(urls2) == 3:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
                # if len(urls1) == 1 and len(urls2) == 4:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], ids2[3], urls2[3])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], ids2[3], urls2[3], pharmacyId, token)
                # if len(urls1) == 2 and len(urls2) == 4:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids2[0], urls2[0], ids2[1], urls2[1], ids2[2], urls2[2], pharmacyId, token)
                # if len(urls1) == 3 and len(urls2) == 4:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids2[0], urls2[0], ids2[1], urls2[1], pharmacyId, token)
                # if len(urls1) == 4 and len(urls2) == 4:
                #     print(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0])
                #     save_health_record_5(patientId, reportName22, reportSummary22, reportType2, reportDoctor21, reportPatient21, ids1[0], urls1[0], ids1[1], urls1[1], ids1[2], urls1[2], ids1[3], urls1[3], ids2[0], urls2[0], pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)                    

    # @staticmethod
    
    # async def picture_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        
    #     ac = gspread.service_account("sppech-to-text-351109-41a4f352dd45.json")
    #     sh = ac.open("userId")
    #     wks = sh.worksheet("Sheet1") 

    #     if not prompt_context.recognized.succeeded:
    #         await prompt_context.context.send_activity(
    #             "No attachments received. Proceeding without a picture...")
    #         # We can return true from a validator function even if recognized.succeeded is false.
    #         return True

    #     attachments = prompt_context.recognized.value
    #     for i in attachments:
    #         print(i.content_type)
    #         wks.update_acell("A1", i.content_type)
    #     valid_images = [
    #         attachment
    #         for attachment in attachments
    #         if attachment.content_type in ["image/jpeg", "image/png", "image/jpg", "application/pdf"]]

    #     for attachment in attachments:
    #         response = urllib.request.urlopen(attachment.content_url)
    #         headers = response.info()

    #         if headers["content-type"] == "application/json":
    #             data = bytes(json.load(response)["data"])
    #         else:
    #             data = response.read()

    #         local_filename = os.path.join(os.getcwd(), attachment.name)
    #         with open(local_filename, "wb") as out_file:
    #             out_file.write(data)

    #     prompt_context.recognized.value = valid_images
    #     return len(valid_images) > 0