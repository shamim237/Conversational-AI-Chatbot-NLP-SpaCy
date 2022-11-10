# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# from datetime import datetime

# def date_validate(date):

#     try:

#         today = datetime.now()
#         today = datetime.strftime(today, "%Y-%m-%d")   
#         today = datetime.strptime(today, "%Y-%m-%d").date()

#         raw = Recognizers.recognize_datetime(date, culture = Culture.English) 
#         dates = []     
#         for i in raw:
#             raw = i.resolution
#             dd = raw['values']
#             # print(dd)
#             for j in dd:
#                 tim = j['value']  
#                 dates.append(tim) 
#         f_date = []
#         for i in dates:
#             datey = datetime.strptime(i, "%Y-%m-%d").date()
#             if datey >= today:
#                 datey = datetime.strftime(datey, "%Y-%m-%d")
#                 f_date.append(datey)
#             else:
#                 return None
#     except:
#         return None

#     return f_date

# ss = date_validate("not tell you")
# print(ss)

# print(datess)

# datek = ",".join(datess)

# print(datek)

# import recognizers_suite as Recognizers
# from recognizers_suite import Culture
# from datetime import datetime



# ss = time_validate("at 11pm")
# print(ss)

# from transformers import pipeline, set_seed
# generator = pipeline('text-generation', model='gpt2')
# set_seed(42)
# generator("Hello, I'm a language model,", max_length=30, num_return_sequences=5)
# from datasets import load_dataset

# dataset = load_dataset("facebook/blenderbot-400M-distill")

# dd = dataset['train']['utterances']


# with open("data.txt", "w") as file:
#     file.write(str(dd))
#     file.close

# print(dd)

# from datasets import load_dataset
# from transformers import AutoTokenizer, TFAutoModelForSeq2SeqLM, TFBlenderbotForConditionalGeneration
# import tensorflow
# import numpy as np
# from tensorflow.keras.optimizers import Adam

# dataset = load_dataset("glue", "cola")
# dataset = dataset["train"]

# # with open("dataf.txt", "r") as dataf:
# #     data = dataf.read()

# tokenizer = AutoTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
# model = TFAutoModelForSeq2SeqLM.from_pretrained("facebook/blenderbot-400M-distill")



# tokenized_data = tokenizer(dataset["sentence"], return_tensors="np", padding=True)

# labels = np.array(dataset["label"]) 

# # dataf = np.array(tokenized_data)

# model.compile(optimizer=Adam(3e-5), loss = "None")

# model.fit(tokenized_data, labels)


# import re

# with open("data.txt", "r") as data:
#     data = data.read()
#     data = re.sub(r"\]\,", r"\n", data)
#     data = re.sub(r"\'\,", r"\n", data)
#     data = re.sub(r"\[", r"", data)
#     data = re.sub(r"\]", r"", data)
#     data = re.sub(r"(\n)\s", r"\1", data)
#     data = re.sub(r"\'(patient)", r"\1", data)
#     data = re.sub(r"\"(patient)", r"\1", data)
#     data = re.sub(r"\'(doctor)", r"\1", data)
#     data = re.sub(r"\"(doctor)", r"\1", data)
#     data = re.sub(r"\'(\n)", r"\1", data) #, doctor:
#     data = re.sub(r"\"(\n)", r"\1", data)
#     data = re.sub(r"\,\s(doctor)", r"\n\1", data)

# with open("dataf.txt", "w") as dataf:
#     dataf.write(data)
#     dataf.close()
