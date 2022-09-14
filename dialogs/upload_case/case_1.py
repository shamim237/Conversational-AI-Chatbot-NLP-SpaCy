import gspread
from user_info import check_name
from prompt.date_prompt import DatePrompt
from prompt.time_prompt import TimePrompt
from nlp_model.predict import predict_class
from prompt.email_prompt import EmailPrompt
from botbuilder.core import MessageFactory
from nlp_model.record_predict import predict_record
from dialogs.attachment_prompt import AttachmentPrompt
from health_record import save_health_record_1, save_health_record_2
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import TextPrompt, NumberPrompt, ChoicePrompt, ConfirmPrompt,PromptOptions



class caseOneRecordDialog(ComponentDialog):
    def __init__(self, dialog_id: str = None):
        super(caseOneRecordDialog, self).__init__(dialog_id or caseOneRecordDialog.__name__)

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
                    self.tenth_step,


                ],
            )
        )

        self.initial_dialog_id = "WFDialog"


    async def first_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global userId
        global token
        global wks
        global pharmacyId

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

        global report_type

        classes         = []
        report_type     = []



        for x in pred.keys():
            if x == "REPORT_TYPE":
                types = pred[x]
                report_type.append(types)
                classes.append(x)


        await step_context.context.send_activity(
            MessageFactory.text("Sure. Please upload the document."))            
        prompt_options = PromptOptions(
            prompt=MessageFactory.text(
                "Tap \U0001F4CE to upload"),)
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
                MessageFactory.text("The file is uploaded successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)  


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
                

        global case1c
        global report_types

        report_types = "vklmvmls"
        case1c       = "ksvkiw0s"


        respo = predict_class(step_context.result)
        
        if respo == "positive":
            case1c = "add more attachments"
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Please attach more files if you would like to upload them."),
                retry_prompt=MessageFactory.text(
                    "The attachment must be a jpeg/png/pdf files."),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
        
        else:
            pres    = ["prescriptions", "prescription"]
            med     = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia     = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

            if report_type[0].lower() in pres:
                report_types = "Prescriptions"
            if report_type[0].lower() in med:
                report_types = "Medical Claims"
            if report_type[0].lower() in dia:
                report_types = "Diagnostic Reports"  

            case1c = "patient_name should take"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is this " + str(report_types) + " for?")),)    


    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


        global case1d 
        global ids1b
        global urls1b
        global report_types1
        global reportPatient1a

        case1d          = "vshhshss" 
        ids1b           = "kafnnkad"
        urls1b          = "smvsvovs"
        report_types1   = "aninaini"
        reportPatient1a = "skkvioss"

        if case1c == "add more attachments":
            
            image = step_context.context.activity.additional_properties

            for i in image.keys():
                if i == "attachmentUrl":
                    urls1b = image[i]
                if i == "attachmentId":
                    ids1b = image[i]        

            pres    = ["prescriptions", "prescription"]
            med     = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia     = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

            if report_type[0].lower() in pres:
                report_types1 = "Prescriptions"
            if report_type[0].lower() in med:
                report_types1 = "Medical Claims"
            if report_type[0].lower() in dia:
                report_types1 = "Diagnostic Reports"  

            case1d = "patient_name should take2"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is this " + str(report_types1) + " for?")),)  


        if case1c == "patient_name should take":
            reportPatient1a = step_context.result
            pred = predict_class(step_context.result)
            if pred == "don't know":
                case1d = "patient_name should again take"    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("It's the patient name. You can find it on the " + str(report_types))),)

            else: 
                case1d  = "doctor name should take"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)


    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1e 
        global reportDoctor1a 
        global reportPatient1b
        global reportPatient1a1

        case1e           = "mvbmlbls"
        reportPatient1b  = "kbkbkbls"
        reportPatient1a1 = "smvomvss"
        reportDoctor1a   = "jkvnnvsn"


        if case1d == "patient_name should take2":
            
            pred = predict_class(step_context.result)
            if pred == "don't know":
                case1e = "patient_name should again take2"    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("It's the patient name. You can find it on the " + str(report_types1))),)

            else: 
                case1e  = "doctor name should take3"
                reportPatient1b = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)


        if case1d == "patient_name should again take":

            case1e  = "doctor name should take2"
            reportPatient1a1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)

        if case1d == "doctor name should take":

            case1e  = "report name name should take"
            reportDoctor1a = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(report_types) + ".")),)


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1f
        global reportName1a
        global reportDoctor1a1
        global reportPatient1b1
        global reportDoctor1b
        
        reportPatient1b1 = "invsivninv"
        reportDoctor1b   = "jhsndjniii"
        reportName1a     = "nncvvnivni"
        reportDoctor1a1  = "js jv j di"
        case1f           = "simnivposs"

        if case1e == "patient_name should again take2":

            case1f  = "doctor name should take4"
            reportPatient1b1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)

        if case1e  == "doctor name should take3":

            case1f  = "report name name should take2"
            reportDoctor1b = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(report_types1) + ".")),)

        if case1e  == "doctor name should take2":

            case1f  = "report name name should take3"
            reportDoctor1a1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(report_types) + ".")),)

        if case1e == "report name name should take":
            
            case1f = "summary should take"
            reportName1a = step_context.result

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?")),)


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global case1g
        global reportName1b
        global reportName1a1
        global reportDoctor1b1

        case1g          = "svnosnvbon"
        reportName1b    = "ksinvsivni"
        reportName1a1   = "sivnivnisn"
        reportDoctor1b1 = "kvsmavopns"

        if case1f == "doctor name should take4":

            case1g  = "report name name should take4"
            reportDoctor1b1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Please enter the name of the report. You can find it on the " + str(report_types1) + ".")),)


        if case1f == "report name name should take2":

            case1g = "summary should take2"
            reportName1b = step_context.result

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?")),)

        if case1f == "report name name should take3":

            case1g = "summary should take3"
            reportName1a1 = step_context.result

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?")),)

        if case1f == "summary should take":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case1g = "add summary"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the reeport summary.")),)

            else:
                reportSummary = ""
                save_health_record_1(userId, reportName1a, reportSummary, report_types, reportDoctor1a, reportPatient1a, ids1a, urls1a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
                return await step_context.end_dialog()  


    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global case1h 
        global reportName1b1

        case1h        = "ksvsnsnw"
        reportName1b1 = "isnvisnd"

        if case1g == "report name name should take4":

            case1h = "summary should take4"
            reportName1b1 = step_context.result

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?")),)            

        if case1g == "summary should take2":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case1h = "add summary2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the report summary.")),)

            else:
                reportSummary = ""
                save_health_record_2(userId, reportName1b, reportSummary, report_types1, reportDoctor1b, reportPatient1b, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
                return await step_context.end_dialog()                


        if case1g == "summary should take3":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case1h = "add summary3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the reeport summary.")),)

            else:
                reportSummary = ""
                save_health_record_1(userId, reportName1a1, reportSummary, report_types, reportDoctor1a1, reportPatient1a1, ids1a, urls1a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
                return await step_context.end_dialog()                

        if case1g == "add summary":

            reportSummary = step_context.result
            save_health_record_1(userId, reportName1a, reportSummary, report_types, reportDoctor1a, reportPatient1a, ids1a, urls1a, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
            return await step_context.end_dialog()      


    async def ninth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global case1i
        case1i = "sonvnosnv"

        if case1h == "summary should take4":
            respo = predict_class(step_context.result)

            if respo == "positive":
                case1i = "add summary4"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the reeport summary.")),)

            else:
                reportSummary = ""
                save_health_record_2(userId, reportName1b1, reportSummary, report_types1, reportDoctor1b1, reportPatient1b1, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
                return await step_context.end_dialog()   


        if case1h == "add summary2":
            reportSummary = step_context.result
            save_health_record_2(userId, reportName1b, reportSummary, report_types1, reportDoctor1b, reportPatient1b, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
            return await step_context.end_dialog()             

        
        if case1h == "add summary3":
            reportSummary = step_context.result
            save_health_record_1(userId, reportName1a1, reportSummary, report_types, reportDoctor1a1, reportPatient1a1, ids1a, urls1a, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
            return await step_context.end_dialog() 


    async def tenth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if case1i == "add summary4":
            reportSummary = step_context.result
            save_health_record_2(userId, reportName1b1, reportSummary, report_types1, reportDoctor1b1, reportPatient1b1, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
            return await step_context.end_dialog() 