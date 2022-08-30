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

        global upload1

        upload1         = "ksmgskm"

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
##########################################################################################################################################################################################
#########################################################################################################################################################################################################################        
        # upload my mom's blood sugar report

        # if "PATIENT_NAME" in classes and "REPORT_NAME" in classes and "REPORT_TYPE" not in classes:
            
        #     my = ["my", "My", "MY", "I", "me", "myself"]

        #     if patient_name[0] in my:
        #         user_name = check_name(userId, token)

        #         if user_name == "not found":
        #             upload1 = "take name from user"
        #             return await step_context.prompt(
        #                 TextPrompt.__name__,
        #                 PromptOptions(
        #                     prompt=MessageFactory.text("I haven't found your name in the server. Can you please enter your name?")),)
        #         else:
        #             patient_name1 = user_name
        #             wks.update_acell("G1", patient_name[0])
        #             wks.update_acell("G2", patient_name1)
        #             upload1 = "upload attachments"
        #             prompt_options = PromptOptions(
        #                 prompt=MessageFactory.text(
        #                     "You can take a snap or upload an image or PDF file. Please choose the document source."),)
        #             return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

        #     else:
        #         upload1 = "upload attachments1"
        #         prompt_options = PromptOptions(
        #             prompt=MessageFactory.text(
        #                 "You can take a snap or upload an image or PDF file. Please choose the document source."),)
        #         return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        # global case2
        # global patient_name101

        # patient_name101 = "uacacus"
        # case2           = "sjsnvjs"


        # if "PATIENT_NAME" in classes and "REPORT_NAME" in classes and "REPORT_TYPE" in classes:
            
        #     my = ["my", "My", "MY", "I", "me", "myself"]

        #     if patient_name[0] in my:
        #         user_name = check_name(userId, token)

        #         if user_name == "not found":
        #             case2 = "take name from user"
        #             return await step_context.prompt(
        #                 TextPrompt.__name__,
        #                 PromptOptions(
        #                     prompt=MessageFactory.text("I haven't found your name in the server. Can you please enter your name?")),)
        #         else:
        #             patient_name101 = user_name
        #             case2 = "upload attachments"
        #             prompt_options = PromptOptions(
        #                 prompt=MessageFactory.text(
        #                     "You can take a snap or upload an image or PDF file. Please choose the document source."),)
        #             return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)

        #     else:
        #         case2 = "upload attachments1"
        #         prompt_options = PromptOptions(
        #             prompt=MessageFactory.text(
        #                 "You can take a snap or upload an image or PDF file. Please choose the document source."),)
        #         return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)


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

            ids1a = list(image.values())[0]
            urls1a = list(image.values())[1]

            if image is not None: 
                case1b = "want to add more or not"
                await step_context.context.send_activity(
                    MessageFactory.text("The files are uploaded successfully."))
                return await step_context.prompt(
                    TextPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)            


#######################################################################################################################################################################################

        # global upload2
        # global urls1
        # global ids1
        # global patient_name12

        # patient_name12  = "smsdidvnnvi"
        # upload2         = "smnvosnaaaa"
        # urls1           = "url of imag"
        # ids1            = "id of image"

        # if upload1 == "take name from user":
        #     patient_name12 = step_context.result
        #     upload2 = "upload attachments2"
        #     prompt_options = PromptOptions(
        #         prompt=MessageFactory.text(
        #             "You can take a snap or upload an image or PDF file. Please choose the document source."),)
        #     return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
        
        # if upload1 == "upload attachments" or upload1 == "upload attachments1":
            
        #     image = step_context.context.activity.additional_properties

        #     ids1 = list(image.values())[0]
        #     urls1 = list(image.values())[1]

        #     if image is not None: 
        #         upload2 = "want to add more or not"
        #         await step_context.context.send_activity(
        #             MessageFactory.text("The files are uploaded successfully."))
        #         return await step_context.prompt(
        #             TextPrompt.__name__,
        #             PromptOptions(
        #                 prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)

###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        # global case2i
        # global urls1i
        # global ids1i
        # global patient_name12i

        # patient_name12i  = "smsdidvnnvi"
        # urls1i          = "url of imag"
        # ids1i            = "id of image"
        # case2i = "ajfnsifv"

        # if case2 == "take name from user":
        #     patient_name12i = step_context.result
        #     case2i = "upload attachments2"
        #     prompt_options = PromptOptions(
        #         prompt=MessageFactory.text(
        #             "You can take a snap or upload an image or PDF file. Please choose the document source."),)
        #     return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
        

        # if case2 == "upload attachments" or case2 == "upload attachments1":
        #     image = step_context.context.activity.additional_properties

        #     ids1i = list(image.values())[0]
        #     urls1i = list(image.values())[1]

        #     if image is not None: 
        #         case2i = "want to add more or not"
        #         await step_context.context.send_activity(
        #             MessageFactory.text("The files are uploaded successfully."))
        #         return await step_context.prompt(
        #             TextPrompt.__name__,
        #             PromptOptions(
        #                 prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)



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




################################################################################################################################################
        # global upload3
        # global ids11
        # global urls11

        # ids11   = "id of the attachs"
        # urls11  = "url of the attach"
        # upload3 = "vnizvivssssssssss"


        # if upload2 == "upload attachments2":
        #     image = step_context.context.activity.additional_properties

        #     ids11 = list(image.values())[0]
        #     urls11 = list(image.values())[1]

        #     if image is not None: 
        #         upload3 = "want to add more or not2"
        #         await step_context.context.send_activity(
        #             MessageFactory.text("The files are uploaded successfully."))
        #         return await step_context.prompt(
        #             TextPrompt.__name__,
        #             PromptOptions(
        #                 prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)


        # if upload2 == "want to add more or not":
        #     yesno = predict_class(step_context.result)
            
        #     if yesno == "positive":
        #         upload3 = "add more/choose options"
        #         prompt_options = PromptOptions(
        #             prompt=MessageFactory.text(
        #                 "Please attach more files you would like to uplaod"),
        #             retry_prompt=MessageFactory.text(
        #                 "The attachment must be a jpeg/png/pdf files."),)
        #         return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
        #     else:
        #         upload3 = "choose options"
        #         listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
        #         return await step_context.prompt((ChoicePrompt.__name__),
        #             PromptOptions(prompt=MessageFactory.text("Okay. What best describes the report?"),choices=listofchoice))                    


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################
        # global ids11i
        # global urls11i
        # global case2ia

        # ids11i  = "smikvw"
        # urls11i = "sviivn"
        # case2ia = "smvvms"

        # if case2i == "upload attachments2":
        #     image = step_context.context.activity.additional_properties

        #     ids11i = list(image.values())[0]
        #     urls11i = list(image.values())[1]

        #     if image is not None: 
        #         case2ia = "want to add more or not2"
        #         await step_context.context.send_activity(
        #             MessageFactory.text("The files are uploaded successfully."))
        #         return await step_context.prompt(
        #             TextPrompt.__name__,
        #             PromptOptions(
        #                 prompt=MessageFactory.text("You can add more images to this report. Would you like to add more?")),)


        # if case2i == "want to add more or not":
        #     yesno = predict_class(step_context.result)
            
        #     if yesno == "positive":
        #         case2ia = "add more/choose options"
        #         prompt_options = PromptOptions(
        #             prompt=MessageFactory.text(
        #                 "Please attach more files you would like to uplaod"),
        #             retry_prompt=MessageFactory.text(
        #                 "The attachment must be a jpeg/png/pdf files."),)
        #         return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
        #     else:
        #         case2ia = "choose options"
        #         return await step_context.prompt(
        #             TextPrompt.__name__,
        #             PromptOptions(
        #                 prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)          




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

            ids1b = list(image.values())[0]
            urls1b = list(image.values())[1]            

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




#################################################################################################################################################################################
        # global urls2
        # global ids2
        # global upload4
        # global reportType1

        # reportType1     = "jncdcncsssss"
        # upload4         = "nothing much"
        # urls2           = "url of image"
        # ids2            = "id of images"


        # if upload3 == "want to add more or not2":
        #     yesno = predict_class(step_context.result)
            
        #     if yesno == "positive":
        #         upload4 = "add more/choose options2"
        #         prompt_options = PromptOptions(
        #             prompt=MessageFactory.text(
        #                 "Please attach more files you would like to uplaod"),
        #             retry_prompt=MessageFactory.text(
        #                 "The attachment must be a jpeg/png/pdf files."),)
        #         return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
        #     else:
        #         upload4 = "choose options2"
        #         listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
        #         return await step_context.prompt((ChoicePrompt.__name__),
        #             PromptOptions(prompt=MessageFactory.text("Okay. What best describes the report?"),choices=listofchoice))  

        # if upload3 == "add more/choose options":
        #     upload4 = "options choosing"
        #     image = step_context.context.activity.additional_properties

        #     ids2 = list(image.values())[0]
        #     urls2 = list(image.values())[1]

        #     listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
        #     return await step_context.prompt((ChoicePrompt.__name__),
        #         PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))

        # if upload3 == "choose options":
        #     upload4 = "doctor name"
        #     reportType1 = step_context.result.value
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)          


###########################################################################################################################################################################################################################
######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
###########################################################################################################################################################################################################################

        # global case2ib
        # global ids2i
        # global urls2i
        # global doctor1i

        # case2ib     = "snvsvnnv"
        # ids2i       = "svisvnis"
        # urls2i      = "kvikvmvm"
        # doctor1i    = "kvkmmkas"


        # if case2ia == "want to add more or not2":
        #     yesno = predict_class(step_context.result)
            
        #     if yesno == "positive":
        #         case2ib = "add more/choose options2"
        #         prompt_options = PromptOptions(
        #             prompt=MessageFactory.text(
        #                 "Please attach more files you would like to uplaod"),
        #             retry_prompt=MessageFactory.text(
        #                 "The attachment must be a jpeg/png/pdf files."),)
        #         return await step_context.prompt(AttachmentPrompt.__name__, prompt_options)
            
        #     else:
        #         case2ib = "choose options2"
        #         return await step_context.prompt(
        #             TextPrompt.__name__,
        #             PromptOptions(
        #                 prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)  

        # if case2ia == "add more/choose options":
        #     case2ib = "options choosing"
        #     image = step_context.context.activity.additional_properties

        #     ids2i = list(image.values())[0]
        #     urls2i = list(image.values())[1]

        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)  

        # if case2ia == "choose options":
        #     case2ib = "doctor name"
        #     doctor1i = step_context.result
        #     return await step_context.prompt(
        #         TextPrompt.__name__,
        #         PromptOptions(
        #             prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)    




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


#############################################################################################################################################################################################################

#         global upload5
#         global ids22
#         global urls22
#         global reportType2
#         global reportType21
#         global doctor1


#         ids22           = "kskdkkdk"
#         urls22          = "svnsvkss"
#         doctor1          = "sklvnsvn"
#         upload5         = "step5sdd"
#         reportType2     = "type ofa"
#         reportType21    = "knknskvn"


#         if upload4 == "add more/choose options2":
#             upload5 = "options choosing2"
#             image = step_context.context.activity.additional_properties

#             ids22 = list(image.values())[0]
#             urls22 = list(image.values())[1]

#             listofchoice = [Choice("Prescriptions"),Choice("Diagonstic Reports"), Choice("Medical Claims")]
#             return await step_context.prompt((ChoicePrompt.__name__),
#                 PromptOptions(prompt=MessageFactory.text("Okay! What best describes the report?"),choices=listofchoice))


#         if upload4 == "choose options2":
#             upload5 = "doctor name2"
#             reportType21 = step_context.result.value
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("Who is the doctor you've consulted with?")),) 

#         if upload4 == "options choosing":
#             upload5 = "doctor name22"
#             reportType2 = step_context.result.value
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)               
                    
#         if upload4 == "doctor name":
#             upload5 = "report summary"  
#             doctor1 = step_context.result  
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)


# ###########################################################################################################################################################################################################################
# ######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
# ###########################################################################################################################################################################################################################

#         global case2ic
#         global ids22i
#         global urls22i
#         global doctor21i
#         global doctor2i

#         case2ic     = "aclacl"
#         ids22i      = "svmlsv"
#         urls22i     = "msvlos"
#         doctor21i   = "slvlls"
#         doctor2i    = "lmclcl"


#         if case2ib == "add more/choose options2":
#             case2ic = "options choosing2"
#             image = step_context.context.activity.additional_properties

#             ids22i  = list(image.values())[0]
#             urls22i = list(image.values())[1]

#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)  


#         if case2ib == "choose options2":
#             case2ic = "doctor name2"
#             doctor21i = step_context.result
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

#         if case2ib == "options choosing":
#             case2ic = "doctor name22"
#             doctor2i = step_context.result
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)          
                    
#         if case2ib == "doctor name":

#             patientId = userId
#             reportSummary = step_context.result

#             if case2 == "upload attachments":

#                 ac = gspread.service_account("chatbot-logger-985638d4a780.json")
#                 sh = ac.open("chatbot_logger")
#                 wks = sh.worksheet("Sheet1")
#                 wks.update_acell("G3", patient_name1)

#                 pres = ["prescriptions", "prescription"]
#                 med = ["medical claimss", "medical claims", "medical claim"]
#                 dia = ["diagnostic reports", "diagnostic report"]

#                 wks.update_acell("K1", report_name[0])
#                 wks.update_acell("K2", reportSummary)
#                 wks.update_acell("K4", doctor1i)
#                 wks.update_acell("K5", patient_name101)
#                 wks.update_acell("K6", ids1i)
#                 wks.update_acell("K7", urls1i)

#                 if report_type[0] in pres:
#                     report_types = "Prescriptions"
#                     wks.update_acell("K3", report_types)
#                     save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name101, ids1i, urls1i, pharmacyId, token) 
#                 if report_type[0] in med:
#                     report_types = "Medical Claims"
#                     save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name101, ids1i, urls1i, pharmacyId, token) 
#                 if report_type[0] in dia:
#                     report_types = "Diagnostic Reports"
#                     save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name101, ids1i, urls1i, pharmacyId, token) 
                

#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

#             if case2 == "upload attachments1":

#                 pres = ["prescriptions", "prescription"]
#                 med = ["medical claimss", "medical claims", "medical claim"]
#                 dia = ["diagnostic reports", "diagnostic report"]
                
#                 if report_type[0] in pres:
#                     report_types = "Prescriptions"
#                     save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name[0], ids1, urls1, pharmacyId, token) 
#                 if report_type[0] in med:
#                     report_types = "Medical Claims"
#                     save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name[0], ids1, urls1, pharmacyId, token) 
#                 if report_type[0] in dia:
#                     report_types = "Diagnostic Reports"
#                     save_health_record_1(patientId, report_name[0], reportSummary, report_types, doctor1i, patient_name[0], ids1, urls1, pharmacyId, token) 

                              
                
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 




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



########################################################################################################################################################################################################








#         global upload6
#         global doctor2
#         global doctor21
#         global reportType22

#         reportType22    = "ssmkssolwe"
#         doctor2         = "siksnsgegr"
#         doctor21        = "kisvmsvmff"
#         upload6         = "snklnfbtgr"


#         if upload5 == "options choosing2":
#             upload6 = "doctor name2"
#             reportType22 = step_context.result.value
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("Who is the doctor you've consulted with?")),)     

#         if upload5 == "doctor name2":
#             upload6 = "report summary2"  
#             doctor21 = step_context.result  
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

#         if upload5 == "doctor name22":
#             upload6 = "report summary"  
#             doctor2 = step_context.result  
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

#         if upload5 == "report summary":
#             patientId = userId
#             reportSummary = step_context.result

#             if upload1 == "upload attachments":

#                 ac = gspread.service_account("chatbot-logger-985638d4a780.json")
#                 sh = ac.open("chatbot_logger")
#                 wks = sh.worksheet("Sheet1")
#                 wks.update_acell("G3", patient_name1)


#                 save_health_record_1(patientId, report_name[0], reportSummary, reportType1, doctor1, patient_name1, ids1, urls1, pharmacyId, token)               
                
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

#             if upload1 == "upload attachments1":

#                 save_health_record_1(patientId, report_name[0], reportSummary, reportType1, doctor1, patient_name[0], ids1, urls1, pharmacyId, token)               
                
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 



# ###########################################################################################################################################################################################################################
# ######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
# ###########################################################################################################################################################################################################################

#         global case2id
#         global doctor22i

#         case2id     = "sknskvn"
#         doctor22i   = "skvksvd"

#         if case2ic == "options choosing2":
#             case2id = "summary2"
#             doctor22i = step_context.result
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)     

#         if case2ic == "doctor name2":
            
#             patientId = userId
#             reportSummary = step_context.result

#             pres = ["prescriptions", "prescription"]
#             med = ["medical claimss", "medical claims", "medical claim"]
#             dia = ["diagnostic reports", "diagnostic report"]

#             if report_type[0] in pres:
#                 report_types = "Prescriptions"
#                 save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor21i, patient_name12i, ids11i, urls11i, pharmacyId, token) 
#             if report_type[0] in med:
#                 report_types = "Medical Claims"
#                 save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor21i, patient_name12i, ids11i, urls11i, pharmacyId, token) 
#             if report_type[0] in dia:
#                 report_types = "Diagnostic Reports"
#                 save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor21i, patient_name12i, ids11i, urls11i, pharmacyId, token) 

                         
            
#             await step_context.context.send_activity(
#                 MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 

#         if case2ic == "doctor name22":
            
#             patientId = userId
#             reportSummary = step_context.result

#             if case2 == "upload attachments":

#                 pres = ["prescriptions", "prescription"]
#                 med = ["medical claimss", "medical claims", "medical claim"]
#                 dia = ["diagnostic reports", "diagnostic report"]

#                 if report_type[0] in pres:
#                     report_types = "Prescriptions"
#                     save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name101, ids1i, urls1i, ids2i, urls2i, pharmacyId, token) 
#                 if report_type[0] in med:
#                     report_types = "Medical Claims"
#                     save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name101, ids1i, urls1i, ids2i, urls2i, pharmacyId, token) 
#                 if report_type[0] in dia:
#                     report_types = "Diagnostic Reports"
#                     save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name101, ids1i, urls1i, ids2i, urls2i, pharmacyId, token) 

                             
                
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)

#             if case2 == "upload attachments1":

#                 pres = ["prescriptions", "prescription"]
#                 med = ["medical claimss", "medical claims", "medical claim"]
#                 dia = ["diagnostic reports", "diagnostic report"]

#                 if report_type[0] in pres:
#                     report_types = "Prescriptions"
#                     save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name[0], ids1i, urls1i, ids2i, urls2i, pharmacyId, token)  
#                 if report_type[0] in med:
#                     report_types = "Medical Claims"
#                     save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name[0], ids1i, urls1i, ids2i, urls2i, pharmacyId, token)
#                 if report_type[0] in dia:
#                     report_types = "Diagnostic Reports"
#                     save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor2i, patient_name[0], ids1i, urls1i, ids2i, urls2i, pharmacyId, token)

                            
                
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)  



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


#################################################################################################################################################################################################################



#         global upload7 
#         global doctor211

#         upload7     = "smnviksvf"
#         doctor211    = "skvmsvmed"

#         if upload6 == "doctor name2":
#             upload7 = "report summary21"  
#             doctor211 = step_context.result  
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can add a short summary of the report for reference. Please write a short summary-")),)

#         if upload6 == "report summary2":
#             patientId = userId
#             reportSummary = step_context.result

#             save_health_record_2(patientId, report_name[0], reportSummary, reportType21, doctor21, patient_name1, ids1, urls1, pharmacyId, token)              
            
#             await step_context.context.send_activity(
#                 MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 


#         if upload6 == "report summary":
#             patientId = userId
#             reportSummary = step_context.result

#             if upload1 == "upload attachments":

#                 save_health_record_2(patientId, report_name[0], reportSummary, reportType2, doctor2, patient_name1, ids1, urls1, ids2, urls2, pharmacyId, token)              
                
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)

#             if upload1 == "upload attachments1":

#                 save_health_record_2(patientId, report_name[0], reportSummary, reportType2, doctor2, patient_name[0], ids1, urls1, ids2, urls2, pharmacyId, token)              
                
#                 await step_context.context.send_activity(
#                     MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#                 return await step_context.prompt(
#                     TextPrompt.__name__,
#                     PromptOptions(
#                         prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),)  


# ###########################################################################################################################################################################################################################
# ######################################################## Case 2- upload my spouse diagnostic report for Aldosterone Test ##################################################################################################
# ###########################################################################################################################################################################################################################


#         if case2id == "summary2":

#             patientId = userId
#             reportSummary = step_context.result

#             pres = ["prescriptions", "prescription"]
#             med = ["medical claimss", "medical claims", "medical claim"]
#             dia = ["diagnostic reports", "diagnostic report"]

#             if report_type[0] in pres:
#                 report_types = "Prescriptions"
#                 save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor22i, patient_name12i, ids11i, urls11i, ids22i, urls22i, pharmacyId, token)  
#             if report_type[0] in med:
#                 report_types = "Medical Claims"
#                 save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor22i, patient_name12i, ids11i, urls11i, ids22i, urls22i, pharmacyId, token)  
#             if report_type[0] in dia:
#                 report_types = "Diagnostic Reports"
#                 save_health_record_2(patientId, report_name[0], reportSummary, report_types, doctor22i, patient_name12i, ids11i, urls11i, ids22i, urls22i, pharmacyId, token)  

                        
            
#             await step_context.context.send_activity(
#                 MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 





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


###############################################################################################################################################################################################################

#         if upload7 == "report summary21":

#             patientId = userId
#             reportSummary = step_context.result

#             save_health_record_2(patientId, report_name[0], reportSummary, reportType22, doctor211, patient_name12, ids11, urls11, ids22, urls22, pharmacyId, token)              
            
#             await step_context.context.send_activity(
#                 MessageFactory.text(f"Thank You! Your report has been saved successfully."))
#             return await step_context.prompt(
#                 TextPrompt.__name__,
#                 PromptOptions(
#                     prompt=MessageFactory.text("You can now access all of your reports from health records section of your Jarvis app.")),) 


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