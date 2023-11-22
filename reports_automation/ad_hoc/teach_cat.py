import pandas as pd
import utilities.file_utilities as file_utilities
json_file = [
    {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614421",
                    "seq_no": "1614421",
                    "q_text": "The students can use the portal as a playground to make mistakes.",
                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614421",
                    "choice_id": "1",
                    "choice_text": "TRUE",
                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614421",
                    "choice_id": "2",
                    "choice_text": "FALSE",
                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614422",
                    "seq_no": "1614422",
                    "q_text": "The student can record or write their responses in Tamizh.",
                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614422",
                    "choice_id": "1",
                    "choice_text": "TRUE",
                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614422",
                    "choice_id": "2",
                    "choice_text": "FALSE",
                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614423",
                    "seq_no": "1614423",
                    "q_text": "If the student strength is more than the no. of computers students can be made to use the lab in batches on alternate weeks",
                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614423",
                    "choice_id": "1",
                    "choice_text": "TRUE",
                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614423",
                    "choice_id": "2",
                    "choice_text": "FALSE",
                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614424",
                    "seq_no": "1614424",
                    "q_text": "What were the major objectives of the Pilot Programme? A) To identify ground level Infrastructure and Technical challenges. B)To identify the factors impacting Student's engagement.C)To recognise the language level of students.D)To ensure headset delivery to all HS and HSS",
                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614424",
                    "choice_id": "1",
                    "choice_text": "Only A",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614424",
                    "choice_id": "2",
                    "choice_text": "Both A and B",

                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614424",
                    "choice_id": "3",
                    "choice_text": "Both C and D",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614424",
                    "choice_id": "4",
                    "choice_text": "All of the above",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614425",
                    "seq_no": "1614425",
                    "q_text": "Is it mandatory for students to login to the portal?",

                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614425",
                    "choice_id": "1",
                    "choice_text": "Yes",

                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614425",
                    "choice_id": "2",
                    "choice_text": "No",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614426",
                    "seq_no": "1614426",
                    "q_text": "What can teachers do in case they are unaware of their students' EMIS ID/password? A)Ask the class teacher to give the student their EMIS IDs and password.B)Go to the school login and find out students' EMIS IDs.C)Ask HM for the ID/password.D)Call 14417",

                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614426",
                    "choice_id": "1",
                    "choice_text": "Only A",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614426",
                    "choice_id": "2",
                    "choice_text": "Both A and B",

                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614426",
                    "choice_id": "3",
                    "choice_text": "A, B and C",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614426",
                    "choice_id": "4",
                    "choice_text": "All of the above",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614427",
                    "seq_no": "1614427",
                    "q_text": "What are the mandatory items to be checked before conducting Language lab periods?A)Headsets to be installed in lab ( 2 headsets per computer).B)Allotted language lab periods in timetable to be stuck in the Hi Tech lab.C)Posters given in the training module must be printed and displayed in the Hi Tech lab.D)Session Plan provided in the module to be read by teachers ",

                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614427",
                    "choice_id": "1",
                    "choice_text": "Only A",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614427",
                    "choice_id": "2",
                    "choice_text": "Both A and B",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614427",
                    "choice_id": "3",
                    "choice_text": "A, B and C",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614427",
                    "choice_id": "4",
                    "choice_text": "All of the above",

                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614428",
                    "seq_no": "1614428",
                    "q_text": "What are teachers to do in case of any grievances during lab period? A)View poster on troubleshooting.B)View FAQ section in Mozhigal Website.C)Call 14417.D)Contact HM/Hi Tech Lab In Charge",

                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614428",
                    "choice_id": "1",
                    "choice_text": "Only A",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614428",
                    "choice_id": "2",
                    "choice_text": "Both A and B",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614428",
                    "choice_id": "3",
                    "choice_text": "A, B and C",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614428",
                    "choice_id": "4",
                    "choice_text": "All of the above",

                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614429",
                    "seq_no": "1614429",
                    "q_text": "The students cannot record multiple times. They should get it right the first time.",

                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614429",
                    "choice_id": "1",
                    "choice_text": "TRUE",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614429",
                    "choice_id": "2",
                    "choice_text": "FALSE",

                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                }
            ]
        },
        {
            "qset_id": "30257",
            "quest": [
                {
                    "q_id": "1614430",
                    "seq_no": "1614430",
                    "q_text": "In the beginning of each module the teacher should ask the student to go through the help videos and learn how to engage with it.",

                    "subjectss": "others",
                    "subject": "other"
                }
            ],
            "choice": [
                {
                    "q_id": "1614430",
                    "choice_id": "1",
                    "choice_text": "TRUE",

                    "choice_correct_yn": "1",
                    "choice_weight": "1.00"
                },
                {
                    "q_id": "1614430",
                    "choice_id": "2",
                    "choice_text": "FALSE",

                    "choice_correct_yn": "0",
                    "choice_weight": "1.00"
                }
            ]
        }
]
df = pd.json_normalize(json_file)
print(df.head(2))
#df.to_excel(r'C:\Users\TAMILL\Data Reporting\reports\generated\Nov_23\18_Nov\TPD_quiz_data\quiz_qstn.xlsx',index=False)
