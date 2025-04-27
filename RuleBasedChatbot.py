# Rule-based Chatbot
import random
import os
import re

error_messages = ["I'm not sure how to respond to that.", "Could you please clarify?"]

class Candidate:
    def __init__(self, name):
        self.name = name
        self.degree = []
        self.institution = None
        self.experience = None
        self.certifications = []
    
    def getStrList(self, l):
        if len(l) == 1: return l[0]
        if len(l) == 2: return l[0] + " and " + l[1]
        str_ = ""
        for i in range(len(l)):
            if(i == len(l) - 1):
                str_ += 'and ' + l[i]
            else: str_ += l[i] + ", "
        return str_

def greeting(greetings_list):
    random_greeting = random.randint(0, len(greetings_list)-1)
    print(greetings_list[random_greeting])

def getResume():
    print("Please share your resume (path to local file).")
    while(True):
        try:
            path_resume = input()
            resume = open(path_resume, 'r')
            _, ext = os.path.splitext(path_resume)
            if(ext != '.txt'): print("Sorry, I can only parse text files. Please share a .txt file as your resume.")
            else: return resume
        except FileNotFoundError:
            print("Oh no! I could not find this file. Please share the path to your locally stored resume file.")
        except Exception as e:
            print("Sorry, an unexpected error {e} occured. Please share the path to your locally stored resume file.")

def parseResume(file, institutions_rank_mapping):
    # assumptions about resume file for parser: 
    #   assume 1st line of resume is always a full name
    #   assume institution in a seperate line by itself
    #   assume experience is only mentioned once 

    degrees = {'B.S.', 'M.Sc.', 'B.Tech', 'MBA', 'Ph.D.', 'BS', 'MSc', 'PhD'}
    certifications = {'AWS Certified', 'PMP', 'Google Cloud Certified'}

    lines = file.readlines()
    candidate = Candidate(lines[0].strip('\n'))

    for i in range(1, len(lines)):
        line = lines[i].strip('\n')
        if(not candidate.institution and line in institutions_rank_mapping.keys()):
            candidate.institution = line
        else:
            if(not candidate.experience):
                match = re.findall('\d+\+? years?', line)
                if len(match) > 0: candidate.experience = match[0]
            for degree in degrees:
                if degree in line:
                    candidate.degree.append(degree)
            for certification in certifications:
                if certification in line:
                    candidate.certifications.append(certification)

    return candidate

def chatbot(greetings_list, institutions_rank_mapping):
    greeting(greetings_list)
    resume_file = getResume()
    candidate = parseResume(resume_file, institutions_rank_mapping)
    
    print("Thanks! Do you have any questions about the candidate?")
    while(True):
        message = input()
        if(message == "bye"): 
            print("Have a nice day!")
            return
        elif("years of experience" in message or "experience" in message):
            print(f"{candidate.name} has {candidate.experience} of experience.")
        elif("degree" in message or "degrees" in message):
            print(f"{candidate.name} has a {candidate.getStrList(candidate.degree)} degree.")
        elif("certification" in message or "certifications" in message or "certified" in message):
            print(f"{candidate.name} has the following certifications listed: {candidate.getStrList(candidate.certifications)}")
        elif("institution" in message):
            print(f"{candidate.name} studied at {candidate.institution} ranked at {institutions_rank_mapping[candidate.institution][0]} and is described as \"{institutions_rank_mapping[candidate.institution][1]}\"")
        else:
            print(error_messages[random.randint(0, len(error_messages)-1)])

if __name__ == '__main__':
    # List of greetings randomly selected by chatbot
    greetings_list = ["Hi! I am a chatbot designed to answer questions about your resume.",
                    "Hello! I am a chatbot. Excited to help you with your resume!",
                    "Hello! I am a resume parser."]

    institutions_rank_mapping = {'University of California, Irvine': [30, 'Top 10 public schools'],
                                 'University of California, Berkeley': [17, 'Top public university']}

    chatbot(greetings_list, institutions_rank_mapping)