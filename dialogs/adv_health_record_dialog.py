from botbuilder.core import MessageFactory
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext, ComponentDialog
from botbuilder.dialogs.prompts import PromptOptions, TextPrompt, NumberPrompt
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
                    self.ninth_step,
                    self.tenth_step,

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
        global diagnostic

        classes         = []
        patient_name    = []
        report_name     = []
        report_type     = []
        diagnostic      = []


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
                report_type.append(types)
                classes.append(x)
            if x == "DIAGNOSTIC":
                diag = pred[x]
                diagnostic.append(diag)
                classes.append(x)


#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
#########################################################################################################################################################################################################################        
        
        global case1a 
        case1a = "ksvnsvn"

        if "PATIENT_NAME" not in classes and "REPORT_NAME" not in classes and "REPORT_TYPE" in classes and "DIAGNOSTIC" not in classes:

            case1a = "upload attachments"
            await step_context.context.send_activity(
                MessageFactory.text("Sure. Please upload the document."))            
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Tap \U0001F4CE to upload"),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 


        global case4a
        case4a = "ksvnsvn"

        if "PATIENT_NAME" in classes and "REPORT_NAME" in classes and "REPORT_TYPE" in classes and "DIAGNOSTIC" not in classes:

            case4a = "upload attachments_case4"
            await step_context.context.send_activity(
                MessageFactory.text("Sure. Please upload the document."))            
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Tap \U0001F4CE to upload"),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)



    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 
        
        global case1b
        global urls1a
        global ids1a

        case1b = "ksvskvn"
        urls1a = "ajnajnc"
        ids1a  = "smnkzxk"


        if case1a == "upload attachments":

            image = step_context.context.activity.additional_properties

            ids1a = list(image.values())[1]
            urls1a = list(image.values())[0]

            if image is not None: 
                case1b = "want to add more or not"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)            

#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 
        global case4b
        global urls4a
        global ids4a

        case4b = "ksvskvn"
        urls4a = "ajnajnc"
        ids4a  = "smnkzxk"

        if case4a == "upload attachments_case4":
            
            image = step_context.context.activity.additional_properties

            ids4a = list(image.values())[1]
            urls4a = list(image.values())[0]

            if image is not None: 
                case4b = "want to add more or not_case4"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)    


    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 


#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 
        global case1c
        global report_types

        report_types = "vklmvmls"
        case1c       = "ksvkiw0s"

        if case1b == "want to add more or not":

            respo = predict_class(step_context.result)
            
            if respo == "positive":
                case1c = "add more attachments"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "Please attach more files you would like to uplaod"),
                    retry_prompt=MessageFactory.text(
                        "The attachment must be a jpeg/png/pdf files."),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
            else:
                pres = ["prescriptions", "prescription"]
                med = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
                dia = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

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


#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 

        global case4c
        global report_types_case4

        report_types_case4 = "vklmvmls"
        case1c       = "ksvkiw0s"
 

        if case4b == "want to add more or not_case4":

            pres = ["prescriptions", "prescription"]
            med = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

            if report_type[0].lower() in pres:
                report_types_case4 = "Prescriptions"
            if report_type[0].lower() in med:
                report_types_case4 = "Medical Claims"
            if report_type[0].lower() in dia:
                report_types_case4 = "Diagnostic Reports" 

            respo = predict_class(step_context.result)
            
            if respo == "positive":
                case4c = "add more attachments_case4"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "Please attach more files you would like to uplaod"),
                    retry_prompt=MessageFactory.text(
                        "The attachment must be a jpeg/png/pdf files."),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
            else:
                case4c = "doctor_name should take_case4"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who's the doctor you've consulted with?")),)      




    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 


#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 
        
        global case1d 
        global ids1b
        global urls1b
        global report_types1
        global reportPatient1a

        case1d          = "vk klv s" 
        ids1b           = "kafnnkad"
        urls1b          = "smvsvovs"
        report_types1   = "aninaini"
        reportPatient1a = "skkvioss"

        if case1c == "add more attachments":
            
            image = step_context.context.activity.additional_properties

            ids1b = list(image.values())[1]
            urls1b = list(image.values())[0]            

            pres = ["prescriptions", "prescription"]
            med = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

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

            pred = predict_class(step_context.result)
            if pred == "don't know":
                case1d = "patient_name should again take"    
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("It's the patient name. You can find it on the " + str(report_types))),)

            else: 
                case1d  = "doctor name should take"
                reportPatient1a = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)


#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 
        
        global case4d 
        global ids4b
        global urls4b
        global reportDoctor4a
        
        case4d          = "vkfklvfs" 
        ids4b           = "kafnnkad"
        urls4b          = "smvsvovs"
        reportDoctor4a  = "skvsivis"
        
        if case4c == "add more attachments_case4":        

            image = step_context.context.activity.additional_properties

            ids4b = list(image.values())[1]
            urls4b = list(image.values())[0]            

            case4d = "doctor_name should take2_case4"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who's the doctor you've consulted with?")),)  

        if case4c == "doctor_name should take_case4":

            reportDoctor4a = step_context.result
            case4d = "report summarry should take_case4"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?")),)  



    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")
        wks.update_acell("E9", case1d)

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


#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 

        global case4e
        global reportDoctor4b

        case4e          = "ksnvsns"
        reportDoctor4b  = "iafv8h8"
        

        if case4d == "doctor_name should take2_case4":

            reportDoctor4b = step_context.result
            case4e = "report summarry should take_case44"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?")),) 

        if case4d == "report summarry should take_case4":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case4e = "add summary_case4"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the reeport summary.")),)

            else:
                reportSummary = ""
                myself = ["my", "myself", "i", "me"]
                
                if patient_name[0].lower() in myself:
                    user_name = check_name(userId, token)
                    if user_name == "not found":
                        case4e = "name nite hbe_case4"
                        await step_context.context.send_activity(
                            MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server."))
                        return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                prompt=MessageFactory.text("Please enter your name-")),)
                    else:
                        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
                        sh = ac.open("chatbot_logger")
                        wks = sh.worksheet("Sheet1")

                        try:
                            wks.update_acell("L1", userId)
                            wks.update_acell("L2", report_name[0])
                            wks.update_acell("L3", reportSummary)
                            wks.update_acell("L4", report_types_case4)
                            wks.update_acell("L5", reportDoctor4a)
                            wks.update_acell("L6", user_name)
                            wks.update_acell("L7", ids4a)
                            wks.update_acell("L8", urls4a)
                            wks.update_acell("L9", pharmacyId)
                            wks.update_acell("L10", token)
                        except:
                            pass

                        save_health_record_1(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4a, user_name, ids4a, urls4a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                        return await step_context.end_dialog()   

                else:
                    save_health_record_1(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4a, patient_name[0], ids4a, urls4a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                    return await step_context.end_dialog()  



    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 
        
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



#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 
        global case4f
        global summary4a
        case4f      = "issivhi8"
        summary4a   = "uasbubua"

        if case4e == "report summarry should take_case44":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case4f = "add summary_case44"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the reeport summary.")),)

            else:
                reportSummary = ""
                myself = ["my", "myself", "i", "me"]
                
                if patient_name[0].lower() in myself:
                    user_name = check_name(userId, token)
                    if user_name == "not found":
                        case4f = "name nite hbe_case44"
                        await step_context.context.send_activity(
                            MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server."))
                        return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                prompt=MessageFactory.text("Please enter your name-")),)
                    else:
                        save_health_record_2(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4b, user_name, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                        return await step_context.end_dialog()   

                else:
                    save_health_record_2(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4b, patient_name[0], ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                    return await step_context.end_dialog()  

        if case4e == "add summary_case4":
            
            summary4a = step_context.result

            myself = ["my", "myself", "i", "me"]
            
            if patient_name[0].lower() in myself:
                user_name = check_name(userId, token)
                if user_name == "not found":
                    case4f = "name nite hbe_case4a"
                    await step_context.context.send_activity(
                        MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server."))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Please enter your name-")),)
                else:
                    save_health_record_1(userId, report_name[0], summary4a, report_types_case4, reportDoctor4a, user_name, ids4a, urls4a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                    return await step_context.end_dialog()   

            else:
                save_health_record_1(userId, report_name[0], summary4a, report_types_case4, reportDoctor4a, patient_name[0], ids4a, urls4a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                return await step_context.end_dialog() 

        
        if case4e == "name nite hbe_case4":
            summary = ""
            patt_name = step_context.result
            save_health_record_1(userId, report_name[0], summary, report_types_case4, reportDoctor4a, patt_name, ids4a, urls4a, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
            return await step_context.end_dialog()               

        


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:


#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

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


#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 
        
        global case4g
        global summary4b

        case4g      = "snncvuisn"
        summary4b   = "isvisnvdd"
        
        if case4f == "add summary_case44":

            summary4b = step_context.result

            myself = ["my", "myself", "i", "me"]
            
            if patient_name[0].lower() in myself:
                user_name = check_name(userId, token)
                if user_name == "not found":
                    case4g = "name nite hbe_case4s"
                    await step_context.context.send_activity(
                        MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server."))
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Please enter your name-")),)
                else:
                    save_health_record_2(userId, report_name[0], summary4b, report_types_case4, reportDoctor4b, user_name, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                    return await step_context.end_dialog()   
  

            else:
                save_health_record_2(userId, report_name[0], summary4b, report_types_case4, reportDoctor4b, patient_name[0], ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
                return await step_context.end_dialog()   


        if case4f == "name nite hbe_case44":
            summary = ""
            names = step_context.result
            save_health_record_2(userId, report_name[0], summary, report_types_case4, reportDoctor4b, names, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
            return await step_context.end_dialog()   

        if case4f == "name nite hbe_case4a":
            names = step_context.result
            save_health_record_1(userId, report_name[0], summary4a, report_types_case4, reportDoctor4a, names, ids4a, urls4a, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
            return await step_context.end_dialog()              


    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

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
                        prompt=MessageFactory.text("Please share the reeport summary.")),)

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


#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 

        if case4g == "name nite hbe_case4s":
            names = step_context.result
            save_health_record_2(userId, report_name[0], summary4b, report_types_case4, reportDoctor4b, names, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully."))
            return await step_context.end_dialog()  



    async def ninth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

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

#########################################################################################################################################################################################################################
##################################################################### Case 1: upload medical claims #####################################################################################################################
######################################################################################################################################################################################################################### 

        if case1i == "add summary4":

            reportSummary = step_context.result
            save_health_record_2(userId, reportName1b1, reportSummary, report_types1, reportDoctor1b1, reportPatient1b1, ids1a, urls1a, ids1b, urls1b, pharmacyId, token)
            await step_context.context.send_activity(
                MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully."))
            return await step_context.end_dialog()  