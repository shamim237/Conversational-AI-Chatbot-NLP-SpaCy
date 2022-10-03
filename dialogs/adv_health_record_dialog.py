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
from dialogs.upload_case.case_2 import caseTwoRecordDialog
from dialogs.upload_case.case_1 import caseOneRecordDialog
from dialogs.upload_case.case_7 import caseSevenRecordDialog

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
        self.add_dialog(caseOneRecordDialog(caseOneRecordDialog.__name__))
        self.add_dialog(caseTwoRecordDialog(caseTwoRecordDialog.__name__))
        self.add_dialog(caseSevenRecordDialog(caseSevenRecordDialog.__name__))
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

        userId = step_context.context.activity.from_property.id
        pharmacyId = step_context.context.activity.from_property.name
        token = step_context.context.activity.from_property.role 

        ac = gspread.service_account("chatbot-logger-985638d4a780.json")
        sh = ac.open("chatbot_logger")
        wks = sh.worksheet("Sheet1")

        main = step_context.context.activity.text
        wks.update_acell("A7", str(main))

        pred = predict_record(main)

        try:
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
        

        if "PATIENT_NAME" not in classes and "REPORT_NAME" not in classes and "REPORT_TYPE" in classes and "DIAGNOSTIC" not in classes:

            return await step_context.begin_dialog(caseOneRecordDialog.__name__)


#########################################################################################################################################################################################################################
##################################################################### Case 2: upload my medical claims #####################################################################################################################
#########################################################################################################################################################################################################################  

        if "PATIENT_NAME" in classes and "REPORT_NAME" not in classes and "REPORT_TYPE" in classes and "DIAGNOSTIC" not in classes:

            return await step_context.begin_dialog(caseTwoRecordDialog.__name__)

#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################        

        global case3a 
        case3a = "ksvnsvn"

        if "PATIENT_NAME" not in classes and "REPORT_NAME" in classes and "REPORT_TYPE" in classes and "DIAGNOSTIC" not in classes:

            case3a = "upload attachments_case3"
            await step_context.context.send_activity(
                MessageFactory.text("Sure. Please upload the document.", extra = main))            
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Tap \U0001F4CE to upload", extra = main),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 


        global case4a
        case4a = "ksvnsvn"

        if "PATIENT_NAME" in classes and "REPORT_NAME" in classes and "REPORT_TYPE" in classes and "DIAGNOSTIC" not in classes:
            wks.update_acell("A19", "Entered health record4")
            case4a = "upload attachments_case4"
            await step_context.context.send_activity(MessageFactory.text(f"Sure. Please upload the document.", extra = main))            
            prompt_options = PromptOptions(prompt=MessageFactory.text(f"Tap \U0001F4CE to upload", extra = main))
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


#########################################################################################################################################################################################################################
##################################################################### Case 5: upload malaria test report #####################################################################################################################
######################################################################################################################################################################################################################### 

        global case5a
        case5a = "ksvnsvn"

        if "PATIENT_NAME" not in classes and "REPORT_NAME" not in classes and "REPORT_TYPE" not in classes and "DIAGNOSTIC" in classes:
            wks.update_acell("A19", "Entered health record5")
            case5a = "upload attachments_case5"
            await step_context.context.send_activity(
                MessageFactory.text("Sure. Please upload the document.", extra = main))            
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Tap \U0001F4CE to upload", extra = main),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


#########################################################################################################################################################################################################################
##################################################################### Case 6: upload my malaria test report #####################################################################################################################
######################################################################################################################################################################################################################### 

        global case6a
        case6a = "ksvnsvn"

        if "PATIENT_NAME" in classes and "REPORT_NAME" not in classes and "REPORT_TYPE" not in classes and "DIAGNOSTIC" in classes:
            wks.update_acell("A19", "Entered health record6")
            wks.update_acell("A20", str(classes))
            wks.update_acell("A21", str(main))
            case6a = "upload attachments_case6"
            await step_context.context.send_activity(
                MessageFactory.text("Sure. Please upload the document.", extra = main))            
            prompt_options = PromptOptions(
                prompt=MessageFactory.text(
                    "Tap \U0001F4CE to upload", extra = main),)
            return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

#########################################################################################################################################################################################################################
##################################################################### Case 7: upload my health record #####################################################################################################################
######################################################################################################################################################################################################################### 

        if "PATIENT_NAME" in classes and "REPORT_NAME" not in classes and "REPORT_TYPE" not in classes and "DIAGNOSTIC" not in classes:
            return await step_context.begin_dialog(caseSevenRecordDialog.__name__)



    async def scnd_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################
        
        global case3b
        global urls3a
        global ids3a

        case3b = "ksvskvn"
        urls3a = "ajnajnc"
        ids3a  = "smnkzxk"

        if case3a == "upload attachments_case3" or case5a == "upload attachments_case5":      

            image = step_context.context.activity.additional_properties

            check = list(image.values())[0]
            if len(check) <= 10:
                ids3a = list(image.values())[0]
                urls3a = list(image.values())[1]
            else:
                ids3a = list(image.values())[1]
                urls3a = list(image.values())[0]  

            if image is not None: 
                case3b = "want to add more or not_case3"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?", extra = main)),)      

#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 
        
        global case4b
        global urls4a
        global ids4a

        case4b = "ksvskvn"
        urls4a = "ajnajnc"
        ids4a  = "smnkzxk"

        if case4a == "upload attachments_case4" or case6a == "upload attachments_case6":
            
            image = step_context.context.activity.additional_properties

            check = list(image.values())[0]
            if len(check) <= 10:
                ids4a = list(image.values())[0]
                urls4a = list(image.values())[1]
            else:
                ids4a = list(image.values())[1]
                urls4a = list(image.values())[0]  

            if image is not None: 
                case4b = "want to add more or not_case4"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully.", extra = main))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?", extra = main)),)   



    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 


#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################
        
        global case3c
        global report_types_case3

        report_types_case3  = "vklmvmls"
        case3c              = "ksvkiw0s"
        
        if case3b == "want to add more or not_case3": 

            respoa = predict_class(step_context.result)

            if respoa == "positive":
                case3c = "add more attachments_case3"
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

                if case3a == "upload attachments_case3":
                    if report_type[0].lower() in pres:
                        report_types_case3 = "Prescriptions"
                    if report_type[0].lower() in med:
                        report_types_case3 = "Medical Claims"
                    if report_type[0].lower() in dia:
                        report_types_case3 = "Diagnostic Reports" 
                else:
                    pass

                if case3a == "upload attachments_case3": 
                    case3c = "patient_name should take_case3"
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Who is this " + str(report_types_case3) + " for?", extra = main)),) 
                if case5a == "upload attachments_case5":
                    case3c = "patient_name should take_case3"
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Who is this diagnostic reports for?", extra = main)),) 

#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 

        global case4c
        global report_types_case4

        report_types_case4  = "vklmvmls"
        case4c              = "ksvkiw0s"
 

        if case4b == "want to add more or not_case4":

            pres = ["prescriptions", "prescription"]
            med = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

            if case4a == "upload attachments_case4":

                if report_type[0].lower() in pres:
                    report_types_case4 = "Prescriptions"
                if report_type[0].lower() in med:
                    report_types_case4 = "Medical Claims"
                if report_type[0].lower() in dia:
                    report_types_case4 = "Diagnostic Reports"
            else:
                pass 

            respox = predict_class(step_context.result)
            
            if respox == "positive":
                case4c = "add more attachments_case4"
                prompt_options = PromptOptions(
                    prompt=MessageFactory.text(
                        "Please attach more files you would like to uplaod", extra = main),
                    retry_prompt=MessageFactory.text(
                        "The attachment must be a jpeg/png/pdf files.", extra = main),)
                return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
            else:
                case4c = "doctor_name should take_case4"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who's the doctor you've consulted with?", extra = main)),)      




    async def fourth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult: 

#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################

        global case3d 
        global ids3b
        global urls3b
        global report_types_case3b
        global reportPatient3a

        case3d                  = "vk klv s" 
        ids3b                   = "kafnnkad"
        urls3b                  = "smvsvovs"
        report_types_case3b     = "aninaini"
        reportPatient3a         = "skkvioss"

        if case3c == "add more attachments_case3":

            image = step_context.context.activity.additional_properties

            check = list(image.values())[0]
            if len(check) <= 10:
                ids3b = list(image.values())[0]
                urls3b = list(image.values())[1]
            else:
                ids3b = list(image.values())[1]
                urls3b = list(image.values())[0]           

            pres    = ["prescriptions", "prescription"]
            med     = ["medical claims", "medical claim", "insurance claims", "insurance claim", "insurance"]
            dia     = ["diagnostic reports", "diagnostic report", "lab reports", "lab report"]

            if case3a == "upload attachments_case3":

                if report_type[0].lower() in pres:
                    report_types_case3b  = "Prescriptions"
                if report_type[0].lower() in med:
                    report_types_case3b  = "Medical Claims"
                if report_type[0].lower() in dia:
                    report_types_case3b  = "Diagnostic Reports" 
            else:
                pass 

            if case3a == "upload attachments_case3":
                case3d = "patient_name should take2_case3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is this " + str(report_types_case3b) + " for?", extra = main)),)

            if case5a == "upload attachments_case5":
                case3d = "patient_name should take2_case3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is this diagnostic reports for?", extra = main)),)


        if case3c == "patient_name should take_case3": 

            preds = predict_class(step_context.result)

            if preds == "don't know":
                if case3a == "upload attachments_case3":
                    case3d = "patient_name should again take_case3"    
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("It's the patient name. You can find it on the " + str(report_types_case3))),)
                if case5a == "upload attachments_case5":
                    case3d = "patient_name should again take_case3"    
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("It's the patient name. You can find it on the diagnostic reports.", extra = main)),)

            else: 
                case3d = "doctor name should take_case3"
                reportPatient3a = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),) 


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

            check = list(image.values())[0]
            if len(check) <= 10:
                ids4b = list(image.values())[0]
                urls4b = list(image.values())[1]
            else:
                ids4b = list(image.values())[1]
                urls4b = list(image.values())[0]          

            case4d = "doctor_name should take2_case4"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who's the doctor you've consulted with?", extra = main)),) 
        
        if case4c == "doctor_name should take_case4":

            reportDoctor4a = step_context.result
            case4d = "report summarry should take_case4"
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add a report summary?", extra = main)),)  




    async def fifth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################

        global case3e 
        global reportDoctor3a 
        global reportPatient3b
        global reportPatient3a1

        case3e           = "mvbmlbls"
        reportPatient3b  = "kbkbkbls"
        reportPatient3a1 = "smvomvss"
        reportDoctor3a   = "jkvnnvsn"

        if case3d == "patient_name should take2_case3":

            pred = predict_class(step_context.result)
            if pred == "don't know":

                if case3a == "upload attachments_case3":
                    case3e = "patient_name should again take2_case3"    
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("It's the patient name. You can find it on the " + str(report_types_case3b) + ".", extra = main)))

                if case5a == "upload attachments_case5":
                    case3e = "patient_name should again take2_case3"    
                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("It's the patient name. You can find it on the diagnostic reports.", extra = main)),)

            else: 
                case3e  = "doctor name should take2_case3"
                reportPatient3b = step_context.result
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),) 


        if case3d == "patient_name should again take_case3":

            case3e  = "doctor name should take2a_case3"
            reportPatient3a1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),)

        if case3d == "doctor name should take_case3":

            case3e  = "report summary should take_case3"
            reportDoctor3a = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add report summary?", extra = main)),)

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
                    prompt=MessageFactory.text("Would you like to add a report summary?", extra = main)),) 

        if case4d == "report summarry should take_case4":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case4e = "add summary_case4"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the reeport summary.", extra = main)),)

            else:
                reportSummary = ""
                myself = ["my", "myself", "i", "me"]
                
                if patient_name[0].lower() in myself:
                    user_name = check_name(userId, token)
                    if user_name == "not found":
                        case4e = "name nite hbe_case4"
                        if case4a == "upload attachments_case4":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server.", extra = main))
                        else:
                            report_types = "Diagnostic Reports"
                            await step_context.context.send_activity(
                                MessageFactory.text(f"I need your name to upload your " + str(report_types) + ". But I haven't find your name in the server.", extra = main))
                        return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                prompt=MessageFactory.text("Please enter your name-", extra = main)),)
                    else:
                        if case4a == "upload attachments_case4":

                            save_health_record_1(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4a, user_name, ids4a, urls4a, pharmacyId, token)
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                            await step_context.context.send_activity(
                                MessageFactory.text("end dialog", extra = main))
                            return await step_context.replace_dialog("passing") 

                        if case6a == "upload attachments_case6": 

                            report_names = diagnostic[0]
                            report_types = "Diagnostic Reports"

                            save_health_record_1(userId, report_names, reportSummary, report_types, reportDoctor4a, user_name, ids4a, urls4a, pharmacyId, token)
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully.", extra = main))
                            await step_context.context.send_activity(
                                MessageFactory.text("end dialog", extra = main))
                            return await step_context.replace_dialog("passing")

                else:
                    if case4a == "upload attachments_case4":

                        save_health_record_1(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4a, patient_name[0], ids4a, urls4a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")

                    if case6a == "upload attachments_case6": 

                        report_names = diagnostic[0]
                        report_types = "Diagnostic Reports"

                        save_health_record_1(userId, report_names, reportSummary, report_types, reportDoctor4a, patient_name[0], ids4a, urls4a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing") 


    async def sixth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################

        global case3f
        global reportPatient3b1
        global reportDoctor3b
        global reportDoctor3a1

        case3f              = "osvosvosops"
        reportPatient3b1    = "acvj9avni9n"
        reportDoctor3b      = "oasovcosass"
        reportDoctor3a1     = "9ja9vcsa9vj"

        if case3e == "patient_name should again take2_case3":    

            case3f = "doctor name should take4_case3"
            reportPatient3b1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Who is the doctor you've consulted with?", extra = main)),)

        if case3e == "doctor name should take2_case3":

            case3f = "report summary should take2_case3"
            reportDoctor3b = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add report summary?", extra = main)),)

        if case3e == "doctor name should take2a_case3":

            case3f = "report name name should take3_case3"
            reportDoctor3a1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add report summary?", extra = main)),)

        
        if case3e == "report summary should take_case3":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case3f = "summary add korbe_case3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the report summary.", extra = main)),)

            else:
                if case3a == "upload attachments_case3":
                    summary = ""
                    save_health_record_1(userId, report_name[0], summary, report_types_case3, reportDoctor3a, reportPatient3a, ids3a, urls3a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case3) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")

                if case5a == "upload attachments_case5": 
                    summary = ""
                    report_namest = diagnostic[0]
                    report_typet = "Diagnostic Reports"
                    save_health_record_1(userId, report_namest, summary, report_typet, reportDoctor3a, reportPatient3a, ids3a, urls3a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")

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
                        prompt=MessageFactory.text("Please share the report summary.", extra = main)),)

            else:
                reportSummary = ""
                myself = ["my", "myself", "i", "me"]
                
                if patient_name[0].lower() in myself:
                    user_name = check_name(userId, token)
                    if user_name == "not found":
                        case4f = "name nite hbe_case44"

                        if case4a == "upload attachments_case4":
                            await step_context.context.send_activity(
                                MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server.", extra = main))
                        else:
                            report_types = "Diagnostic Reports"
                            await step_context.context.send_activity(
                                MessageFactory.text(f"I need your name to upload your " + str(report_types) + ". But I haven't find your name in the server.", extra = main))  

                        return await step_context.prompt(
                            TextPrompt.__name__,
                            PromptOptions(
                                prompt=MessageFactory.text("Please enter your name-", extra = main)),)
                    else:
                        if case4a == "upload attachments_case4":

                            save_health_record_2(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4b, user_name, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                            await step_context.context.send_activity(
                                MessageFactory.text("end dialog", extra = main))
                            return await step_context.replace_dialog("passing")

                        if case4a == "upload attachments_case6":

                            report_names = diagnostic[0]
                            report_typef = "Diagnostic Reports"

                            save_health_record_2(userId, report_names, reportSummary, report_typef, reportDoctor4b, user_name, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                            await step_context.context.send_activity(
                                MessageFactory.text("end dialog", extra = main))
                            return await step_context.replace_dialog("passing")                             

                else:
                    if case4a == "upload attachments_case4":

                        save_health_record_2(userId, report_name[0], reportSummary, report_types_case4, reportDoctor4b, patient_name[0], ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")

                    if case4a == "upload attachments_case6":

                            report_names = diagnostic[0]
                            report_typef = "Diagnostic Reports" 

                            save_health_record_2(userId, report_names, reportSummary, report_typef, reportDoctor4b,  patient_name[0], ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                            await step_context.context.send_activity(
                                MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                            await step_context.context.send_activity(
                                MessageFactory.text("end dialog", extra = main))
                            return await step_context.replace_dialog("passing")                             

        if case4e == "add summary_case4":
            
            summary4a = step_context.result

            myself = ["my", "myself", "i", "me"]
            
            if patient_name[0].lower() in myself:
                user_name = check_name(userId, token)
                if user_name == "not found":
                    case4f = "name nite hbe_case4a"

                    if case4a == "upload attachments_case4":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server.", extra = main))
                    else:
                        report_types = "Diagnostic Reports"
                        await step_context.context.send_activity(
                            MessageFactory.text(f"I need your name to upload your " + str(report_types) + ". But I haven't find your name in the server.", extra = main))

                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Please enter your name-", extra = main)),)
                else:
                    
                    if case4a == "upload attachments_case4":
                        save_health_record_1(userId, report_name[0], summary4a, report_types_case4, reportDoctor4a, user_name, ids4a, urls4a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing") 
                    
                    if case4a == "upload attachments_case6":

                        report_names = diagnostic[0]
                        report_typef = "Diagnostic Reports"                    
                        save_health_record_1(userId, report_names, summary4a, report_typef, reportDoctor4a, user_name, ids4a, urls4a, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")

            else:
                if case4a == "upload attachments_case4":

                    save_health_record_1(userId, report_name[0], summary4a, report_types_case4, reportDoctor4a, patient_name[0], ids4a, urls4a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing") 

                if case4a == "upload attachments_case6":

                    report_names = diagnostic[0]
                    report_typef = "Diagnostic Reports" 
                    save_health_record_1(userId, report_names, summary4a, report_typef, reportDoctor4a, patient_name[0], ids4a, urls4a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing") 

        
        if case4e == "name nite hbe_case4":

            summary = ""
            patt_name = step_context.result
            if case4a == "upload attachments_case4":
                save_health_record_1(userId, report_name[0], summary, report_types_case4, reportDoctor4a, patt_name, ids4a, urls4a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")
            if case4a == "upload attachments_case6":               
                report_names = diagnostic[0]
                report_typef = "Diagnostic Reports" 
                save_health_record_1(userId, report_names, summary, report_typef, reportDoctor4a, patt_name, ids4a, urls4a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")       


    async def seventh_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
 
#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################
        
        global case3g
        global reportDoctor3b1

        case3g              = "knsvkvs"
        reportDoctor3b1     = "ksmskmo"

        if case3f == "doctor name should take4_case3":

            case3g = "report summary should take22_case3"
            reportDoctor3b1 = step_context.result
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("Would you like to add report summary?", extra = main)),)

        if case3f == "report summary should take2_case3":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case3g = "summary add korbe1_case3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the report summary.", extra = main)),)

            else:
                if case3a == "upload attachments_case3": 
                    summary = ""
                    save_health_record_2(userId, report_name[0], summary, report_types_case3b, reportDoctor3b, reportPatient3b, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case3b) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing") 

                if case5a == "upload attachments_case5":
                    report_namet = diagnostic[0]
                    report_typet = "Diagnostic Reports" 
                    summary = ""
                    save_health_record_2(userId, report_namet, summary, report_typet, reportDoctor3b, reportPatient3b, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing") 


        if case3f == "report name name should take3_case3":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case3g = "summary add korbe2_case3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the report summary.", extra = main)),)

            else:
                if case3a == "upload attachments_case3":
                    summary = ""
                    save_health_record_1(userId, report_name[0], summary, report_types_case3, reportDoctor3a1, reportPatient3a1, ids3a, urls3a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case3) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")

                if case5a == "upload attachments_case5":
                    summary = ""
                    report_namet = diagnostic[0]
                    report_typet = "Diagnostic Reports" 
                    save_health_record_1(userId, report_namet, summary, report_typet, reportDoctor3a1, reportPatient3a1, ids3a, urls3a, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")                     


        if case3f == "summary add korbe_case3":  

            summary = step_context.result
            if case3a == "upload attachments_case3":
                save_health_record_1(userId, report_name[0], summary, report_types_case3, reportDoctor3a, reportPatient3a, ids3a, urls3a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case3) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing") 

            if case5a == "upload attachments_case5":
                report_namet = diagnostic[0]
                report_typet = "Diagnostic Reports" 
                save_health_record_1(userId, report_namet, summary, report_typet, reportDoctor3a, reportPatient3a, ids3a, urls3a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")                      



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
                    if case4a == "upload attachments_case4":
                        await step_context.context.send_activity(
                            MessageFactory.text(f"I need your name to upload your " + str(report_types_case4) + ". But I haven't find your name in the server.", extra = main))
                    else:
                        report_types = "Diagnostic Reports"
                        await step_context.context.send_activity(
                            MessageFactory.text(f"I need your name to upload your " + str(report_types) + ". But I haven't find your name in the server.", extra = main))

                    return await step_context.prompt(
                        TextPrompt.__name__,
                        PromptOptions(
                            prompt=MessageFactory.text("Please enter your name-", extra = main)),)
                else:
                    if case4a == "upload attachments_case4":
                        save_health_record_2(userId, report_name[0], summary4b, report_types_case4, reportDoctor4b, user_name, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")
                    if case4a == "upload attachments_case6":               
                        report_names = diagnostic[0]
                        report_typef = "Diagnostic Reports" 
                        save_health_record_2(userId, report_names, summary4b, report_typef, reportDoctor4b, user_name, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                        await step_context.context.send_activity(
                            MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                        await step_context.context.send_activity(
                            MessageFactory.text("end dialog", extra = main))
                        return await step_context.replace_dialog("passing")
                      
            else:
                if case4a == "upload attachments_case4":
                    save_health_record_2(userId, report_name[0], summary4b, report_types_case4, reportDoctor4b, patient_name[0], ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")   

                if case4a == "upload attachments_case6":               
                    report_names = diagnostic[0]
                    report_typef = "Diagnostic Reports" 
                    save_health_record_2(userId, report_names, summary4b, report_typef, reportDoctor4b, patient_name[0], ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")



        if case4f == "name nite hbe_case44":
            summary = ""
            names = step_context.result
            if case4a == "upload attachments_case4":
                save_health_record_2(userId, report_name[0], summary, report_types_case4, reportDoctor4b, names, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")
            if case4a == "upload attachments_case6":               
                report_names = diagnostic[0]
                report_typef = "Diagnostic Reports" 
                save_health_record_2(userId, report_names, summary, report_typef, reportDoctor4b, names, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")             

        if case4f == "name nite hbe_case4a":
            names = step_context.result
            if case4a == "upload attachments_case4":
                save_health_record_1(userId, report_name[0], summary4a, report_types_case4, reportDoctor4a, names, ids4a, urls4a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")              
            if case4a == "upload attachments_case6":               
                report_names = diagnostic[0]
                report_typef = "Diagnostic Reports"
                save_health_record_1(userId, report_names, summary4a, report_typef, reportDoctor4a, names, ids4a, urls4a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")    
                

    async def eighth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################

        global case3h 
        case3h = "akaaso"

        if case3g == "report summary should take22_case3":

            respo = predict_class(step_context.result)

            if respo == "positive":
                case3h = "summary add korbe3_case3"
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("Please share the report summary.", extra = main)),)

            else:
                if case3a == "upload attachments_case3":
                    summary = ""
                    save_health_record_2(userId, report_name[0], summary, report_types_case3b, reportDoctor3b1, reportPatient3b1, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_types_case3b) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing") 

                if case5a == "upload attachments_case5":
                    report_namet = diagnostic[0]
                    report_typet = "Diagnostic Reports" 
                    summary = ""
                    save_health_record_2(userId, report_namet, summary, report_typet, reportDoctor3b1, reportPatient3b1, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                    await step_context.context.send_activity(
                        MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                    await step_context.context.send_activity(
                        MessageFactory.text("end dialog", extra = main))
                    return await step_context.replace_dialog("passing")


        if case3g == "summary add korbe1_case3":

            summary = step_context.result
            if case3a == "upload attachments_case3":
                save_health_record_2(userId, report_name[0], summary, report_types_case3b, reportDoctor3b, reportPatient3b, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case3b) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")
            
            if case5a == "upload attachments_case5":
                report_namet = diagnostic[0]
                report_typet = "Diagnostic Reports" 
                save_health_record_2(userId, report_namet, summary, report_typet, reportDoctor3b, reportPatient3b, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")

        
        if case3g == "summary add korbe2_case3":

            summary = step_context.result
            if case3a == "upload attachments_case3":
                save_health_record_1(userId, report_name[0], summary, report_types_case3, reportDoctor3a1, reportPatient3a1, ids3a, urls3a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case3) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing") 
            
            if case5a == "upload attachments_case5":
                report_namet = diagnostic[0]
                report_typet = "Diagnostic Reports" 
                save_health_record_1(userId, report_namet, summary, report_typet, reportDoctor3a1, reportPatient3a1, ids3a, urls3a, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")

#########################################################################################################################################################################################################################
##################################################################### Case 4: upload my prescriptions for covid test report #####################################################################################################################
######################################################################################################################################################################################################################### 

        if case4g == "name nite hbe_case4s":
            names = step_context.result

            if case4a == "upload attachments_case4":
                save_health_record_2(userId, report_name[0], summary4b, report_types_case4, reportDoctor4b, names, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case4) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing") 

            if case4a == "upload attachments_case6":               
                report_names = diagnostic[0]
                report_typef = "Diagnostic Reports"
                save_health_record_2(userId, report_names, summary4b, report_typef, reportDoctor4b, names, ids4a, urls4a, ids4b, urls4b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typef) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")  


    async def ninth_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:

#########################################################################################################################################################################################################################
##################################################################### Case 3: upload diagnostic report for dengue fever test #####################################################################################################################
#########################################################################################################################################################################################################################

        if case3h == "summary add korbe3_case3": 
            summary = step_context.result
            
            if case3a == "upload attachments_case3":
                save_health_record_2(userId, report_name[0], summary, report_types_case3b, reportDoctor3b1, reportPatient3b1, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_types_case3b) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing") 

            if case5a == "upload attachments_case5":
                report_namet = diagnostic[0]
                report_typet = "Diagnostic Reports"                 
                save_health_record_2(userId, report_namet, summary, report_typet, reportDoctor3b1, reportPatient3b1, ids3a, urls3a, ids3b, urls3b, pharmacyId, token)
                await step_context.context.send_activity(
                    MessageFactory.text(f"Your " + str(report_typet) + " has been uploaded successfully.", extra = main))
                await step_context.context.send_activity(
                    MessageFactory.text("end dialog", extra = main))
                return await step_context.replace_dialog("passing")


 