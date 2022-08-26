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
from user_info import check_name


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

        global patient_name1 
        global upload1

        upload1         = "ksmgskm"
        patient_name1   = "sksksks" 

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

        wks.update_acell("F1", patient_name[0])
        # upload my mom's blood sugar report

        if "PATIENT_NAME" in classes and "REPORT_NAME" in classes and "REPORT_TYPE" not in classes:
            
            my = ["my", "My", "MY", "I", "me", "myself"]

            if patient_name[0] in my:
                user_name = check_name(userId, token)

                if user_name == "not found":
                    upload1 = "take name from user"
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("I haven't found your name in the server. Can you please enter your name?")),)
                else:
                    patient_name1 = user_name
                    wks.update_acell("G1", patient_name[0])
                    wks.update_acell("G2", patient_name1)
                    upload1 = "upload attachments"
                    prompt_options = PromptOptions(
                        prompt=MessageFactory.text(
                            "You can take a snap or upload an image or PDF file. Please choose the document source."),)
                    return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

            else:
                upload1 = "upload attachments1"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "You can take a snap or upload an image or PDF file. Please choose the document source."),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        global case2
        global patient_name101

        patient_name101 = "uacacus"
        case2           = "sjsnvjs"


        if "PATIENT_NAME" in classes and "REPORT_NAME" in classes and "REPORT_TYPE" in classes:
            
            my = ["my", "My", "MY", "I", "me", "myself"]

            if patient_name[0] in my:
                user_name = check_name(userId, token)

                if user_name == "not found":
                    case2 = "take name from user"
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("I haven't found your name in the server. Can you please enter your name?")),)
                else:
                    patient_name101 = user_name
                    case2 = "upload attachments"
                    prompt_options = PromptOptions(
                        prompt=MessageFactory.text(
                            "You can take a snap or upload an image or PDF file. Please choose the document source."),)
                    return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

            else:
                case2 = "upload attachments1"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "You can take a snap or upload an image or PDF file. Please choose the document source."),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        
        global upload2
        global urls1
        global ids1
        global patient_name12

        patient_name12  = "smsdidvnnvi"
        upload2         = "smnvosnaaaa"
        urls1           = "url of imag"
        ids1            = "id of image"

        if upload1 == "take name from user":
            patient_name12 = step_context.result
            upload2 = "upload attachments2"
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "You can take a snap or upload an image or PDF file. Please choose the document source."),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
        
        if upload1 == "upload attachments" or upload1 == "upload attachments1":
            
            image = step_context.context.activity.additional_properties

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

###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        global case2i
        global urls1i
        global ids1i
        global patient_name12i

        patient_name12i  = "smsdidvnnvi"
        urls1i          = "url of imag"
        ids1i            = "id of image"
        case2i = "ajfnsifv"

        if case2 == "take name from user":
            patient_name12i = step_context.result
            case2i = "upload attachments2"
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "You can take a snap or upload an image or PDF file. Please choose the document source."),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
        

        if case2 == "upload attachments" or case2 == "upload attachments1":
            image = step_context.context.activity.additional_properties

            ids1i = list(image.values())[0]
            urls1i = list(image.values())[1]

            if image is not None: 
                case2i = "want to add more or not"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)



    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global upload3
        global ids11
        global urls11

        ids11   = "id of the attachs"
        urls11  = "url of the attach"
        upload3 = "vnizvivssssssssss"


        if upload2 == "upload attachments2":
            image = step_context.context.activity.additional_properties

            ids11 = list(image.values())[0]
            urls11 = list(image.values())[1]

            if image is not None: 
                upload3 = "want to add more or not2"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)


        if upload2 == "want to add more or not":
            yesno = predict_class(step_context.result)
            
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
                    PromptOptions(prompt=MessageFactory.text("Okay. What best describes the report?"),choices=listofchoice))                    


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################
        global ids11i
        global urls11i
        global case2ia

        ids11i  = "smikvw"
        urls11i = "sviivn"
        case2ia = "smvvms"

        if case2i == "upload attachments2":
            image = step_context.context.activity.additional_properties

            ids11i = list(image.values())[0]
            urls11i = list(image.values())[1]

            if image is not None: 
                case2ia = "want to add more or not2"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)


        if case2i == "want to add more or not":
            yesno = predict_class(step_context.result)
            
            if yesno == "positive":
                case2ia = "add more/choose options"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "Please attach more files you would like to uplaod"),
                    retry_prompt=MessageFactory.text(
                        "The attachment must be a jpeg/png/pdf files."),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
            else:
                case2ia = "choose options"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)          




    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

        global urls2
        global ids2
        global upload4
        global reportType1

        reportType1     = "jncdcncsssss"
        upload4         = "nothing much"
        urls2           = "url of image"
        ids2            = "id of images"


        if upload3 == "want to add more or not2":
            yesno = predict_class(step_context.result)
            
            if yesno == "positive":
                upload4 = "add more/choose options2"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "Please attach more files you would like to uplaod"),
                    retry_prompt=MessageFactory.text(
                        "The attachment must be a jpeg/png/pdf files."),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
            else:
                upload4 = "choose options2"
                listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
                return await step_context.prompt((ChoicePrompt.__name__),
                    PromptOptions(prompt=MessageFactory.text("Okay. What best describes the report?"),choices=listofchoice))  

        if upload3 == "add more/choose options":
            upload4 = "options choosing"
            image = step_context.context.activity.additional_properties

            ids2 = list(image.values())[0]
            urls2 = list(image.values())[1]

            listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
            return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))

        if upload3 == "choose options":
            upload4 = "doctor name"
            reportType1 = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)          


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        global case2ib
        global ids2i
        global urls2i
        global doctor1i

        case2ib     = "snvsvnnv"
        ids2i       = "svisvnis"
        urls2i      = "kvikvmvm"
        doctor1i    = "kvkmmkas"


        if case2ia == "want to add more or not2":
            yesno = predict_class(step_context.result)
            
            if yesno == "positive":
                case2ib = "add more/choose options2"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "Please attach more files you would like to uplaod"),
                    retry_prompt=MessageFactory.text(
                        "The attachment must be a jpeg/png/pdf files."),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
            else:
                case2ib = "choose options2"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)  

        if case2ia == "add more/choose options":
            case2ib = "options choosing"
            image = step_context.context.activity.additional_properties

            ids2i = list(image.values())[0]
            urls2i = list(image.values())[1]

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)  

        if case2ia == "choose options":
            case2ib = "doctor name"
            doctor1i = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)    




    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload5
        global ids22
        global urls22
        global reportType2
        global reportType21
        global doctor1


        ids22           = "kskdkkdk"
        urls22          = "svnsvkss"
        doctor1          = "sklvnsvn"
        upload5         = "step5sdd"
        reportType2     = "type ofa"
        reportType21    = "knknskvn"


        if upload4 == "add more/choose options2":
            upload5 = "options choosing2"
            image = step_context.context.activity.additional_properties

            ids22 = list(image.values())[0]
            urls22 = list(image.values())[1]

            listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
            return await step_context.prompt((ChoicePrompt.__name__),
                PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))


        if upload4 == "choose options2":
            upload5 = "doctor name2"
            reportType21 = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),) 

        if upload4 == "options choosing":
            upload5 = "doctor name22"
            reportType2 = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)               
                    
        if upload4 == "doctor name":
            upload5 = "report summary"  
            doctor1 = step_context.result  
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        global case2ic
        global ids22i
        global urls22i
        global doctor21i
        global doctor2i

        case2ic     = "aclacl"
        ids22i      = "svmlsv"
        urls22i     = "msvlos"
        doctor21i   = "slvlls"
        doctor2i    = "lmclcl"


        if case2ib == "add more/choose options2":
            case2ic = "options choosing2"
            image = step_context.context.activity.additional_properties

            ids22i  = list(image.values())[0]
            urls22i = list(image.values())[1]

            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)  


        if case2ib == "choose options2":
            case2ic = "doctor name2"
            doctor21i = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if case2ib == "options choosing":
            case2ic = "doctor name22"
            doctor2i = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)          
                    
        if case2ib == "doctor name":

            patientId = userId
            reportSummary = step_context.result

            if case2 == "upload attachments":

                ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                sh = ac.open("chatbot_logger")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("G3", patient_name1)

                pres = ["prescriptions", "prescription"]
                med = ["medical claimss", "medical claims", "medical claim"]
                dia = ["diagnostic reports", "diagnostic report"]

                wks.update_acell("K1", report_name[0])
                wks.update_acell("K2", reportSummary)
                wks.update_acell("K4", doctor1i)
                wks.update_acell("K5", patient_name101)
                wks.update_acell("K6", ids1i)
                wks.update_acell("K7", urls1i)

                if report_type[0] in pres:
                    report_types = "Prescriptions"
                    wks.update_acell("K3", report_types)
                    save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name101, ids1i, urls1i, pharmacyId, token) 
                if report_type[0] in med:
                    report_types = "Medical Claims"
                    save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name101, ids1i, urls1i, pharmacyId, token) 
                if report_type[0] in dia:
                    report_types = "Diagnostic Reports"
                    save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name101, ids1i, urls1i, pharmacyId, token) 
                

                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

            if case2 == "upload attachments1":

                pres = ["prescriptions", "prescription"]
                med = ["medical claimss", "medical claims", "medical claim"]
                dia = ["diagnostic reports", "diagnostic report"]
                
                if report_type[0] in pres:
                    report_types = "Prescriptions"
                    save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name[0], ids1, urls1, pharmacyId, token) 
                if report_type[0] in med:
                    report_types = "Medical Claims"
                    save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name[0], ids1, urls1, pharmacyId, token) 
                if report_type[0] in dia:
                    report_types = "Diagnostic Reports"
                    save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name[0], ids1, urls1, pharmacyId, token) 

                              
                
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 




    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload6
        global doctor2
        global doctor21
        global reportType22

        reportType22    = "ssmkssolwe"
        doctor2         = "siksnsgegr"
        doctor21        = "kisvmsvmff"
        upload6         = "snklnfbtgr"


        if upload5 == "options choosing2":
            upload6 = "doctor name2"
            reportType22 = step_context.result.value
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)     

        if upload5 == "doctor name2":
            upload6 = "report summary2"  
            doctor21 = step_context.result  
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload5 == "doctor name22":
            upload6 = "report summary"  
            doctor2 = step_context.result  
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload5 == "report summary":
            patientId = userId
            reportSummary = step_context.result

            if upload1 == "upload attachments":

                ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                sh = ac.open("chatbot_logger")
                wks = sh.worksheet("Sheet1")
                wks.update_acell("G3", patient_name1)


                save_health_record_1(patientId, report_name[0], reportSummary, reportType1, doctor1, patient_name1, ids1, urls1, pharmacyId, token)               
                
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

            if upload1 == "upload attachments1":

                save_health_record_1(patientId, report_name[0], reportSummary, reportType1, doctor1, patient_name[0], ids1, urls1, pharmacyId, token)               
                
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 



###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        global case2id
        global doctor22i

        case2id     = "sknskvn"
        doctor22i   = "skvksvd"

        if case2ic == "options choosing2":
            case2id = "summary2"
            doctor22i = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)     

        if case2ic == "doctor name2":
            
            patientId = userId
            reportSummary = step_context.result

            pres = ["prescriptions", "prescription"]
            med = ["medical claimss", "medical claims", "medical claim"]
            dia = ["diagnostic reports", "diagnostic report"]

            if report_type[0] in pres:
                report_types = "Prescriptions"
                save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor21i, patient_name12i, ids11i, urls11i, pharmacyId, token) 
            if report_type[0] in med:
                report_types = "Medical Claims"
                save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor21i, patient_name12i, ids11i, urls11i, pharmacyId, token) 
            if report_type[0] in dia:
                report_types = "Diagnostic Reports"
                save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor21i, patient_name12i, ids11i, urls11i, pharmacyId, token) 

                         
            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

        if case2ic == "doctor name22":
            
            patientId = userId
            reportSummary = step_context.result

            if case2 == "upload attachments":

                pres = ["prescriptions", "prescription"]
                med = ["medical claimss", "medical claims", "medical claim"]
                dia = ["diagnostic reports", "diagnostic report"]

                if report_type[0] in pres:
                    report_types = "Prescriptions"
                    save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name101, ids1i, urls1i, ids2i, urls2i, pharmacyId, token) 
                if report_type[0] in med:
                    report_types = "Medical Claims"
                    save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name101, ids1i, urls1i, ids2i, urls2i, pharmacyId, token) 
                if report_type[0] in dia:
                    report_types = "Diagnostic Reports"
                    save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name101, ids1i, urls1i, ids2i, urls2i, pharmacyId, token) 

                             
                
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)

            if case2 == "upload attachments1":

                pres = ["prescriptions", "prescription"]
                med = ["medical claimss", "medical claims", "medical claim"]
                dia = ["diagnostic reports", "diagnostic report"]

                if report_type[0] in pres:
                    report_types = "Prescriptions"
                    save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name[0], ids1i, urls1i, ids2i, urls2i, pharmacyId, token)  
                if report_type[0] in med:
                    report_types = "Medical Claims"
                    save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name[0], ids1i, urls1i, ids2i, urls2i, pharmacyId, token)
                if report_type[0] in dia:
                    report_types = "Diagnostic Reports"
                    save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name[0], ids1i, urls1i, ids2i, urls2i, pharmacyId, token)

                            
                
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)  



    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        global upload7 
        global doctor211

        upload7     = "smnviksvf"
        doctor211    = "skvmsvmed"

        if upload6 == "doctor name2":
            upload7 = "report summary21"  
            doctor211 = step_context.result  
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

        if upload6 == "report summary2":
            patientId = userId
            reportSummary = step_context.result

            save_health_record_2(patientId, report_name[0], reportSummary, reportType21, doctor21, patient_name1, ids1, urls1, pharmacyId, token)              
            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 


        if upload6 == "report summary":
            patientId = userId
            reportSummary = step_context.result

            if upload1 == "upload attachments":

                save_health_record_2(patientId, report_name[0], reportSummary, reportType2, doctor2, patient_name1, ids1, urls1, ids2, urls2, pharmacyId, token)              
                
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)

            if upload1 == "upload attachments1":

                save_health_record_2(patientId, report_name[0], reportSummary, reportType2, doctor2, patient_name[0], ids1, urls1, ids2, urls2, pharmacyId, token)              
                
                await step_context.context.send_activity(
                    MessageFactory.text(f"Thank You! Your report has been saved successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)  


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################


        if case2id == "summary2":

            patientId = userId
            reportSummary = step_context.result

            pres = ["prescriptions", "prescription"]
            med = ["medical claimss", "medical claims", "medical claim"]
            dia = ["diagnostic reports", "diagnostic report"]

            if report_type[0] in pres:
                report_types = "Prescriptions"
                save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor22i, patient_name12i, ids11i, urls11i, ids22i, urls22i, pharmacyId, token)  
            if report_type[0] in med:
                report_types = "Medical Claims"
                save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor22i, patient_name12i, ids11i, urls11i, ids22i, urls22i, pharmacyId, token)  
            if report_type[0] in dia:
                report_types = "Diagnostic Reports"
                save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor22i, patient_name12i, ids11i, urls11i, ids22i, urls22i, pharmacyId, token)  

                        
            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 





    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

        if upload7 == "report summary21":

            patientId = userId
            reportSummary = step_context.result

            save_health_record_2(patientId, report_name[0], reportSummary, reportType22, doctor211, patient_name12, ids11, urls11, ids22, urls22, pharmacyId, token)              
            
            await step_context.context.send_activity(
                MessageFactory.text(f"Thank You! Your report has been saved successfully."))
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 