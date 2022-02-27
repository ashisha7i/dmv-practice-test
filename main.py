import wget
import json
from webbrowser import get
import requests
from bs4 import BeautifulSoup
import uuid

json_arr = []
question_num = 1
downloaded_images = {"test"}

def get_question_text(question_row):
    question_div = question_row.find("div", class_="question")
    question_div_h3 = question_div.find("h3")
    question_text = question_div_h3.text
    question_text = question_text[question_text.index(".")+1:].strip()
    return question_text

def get_answer_options(question_row):
    options = []
    answer_pick_holder = question_row.find("div", class_="answer-pick-holder")
    option_labels = answer_pick_holder.find_all("label", class_="form-check-label")
    for option_label in option_labels:
        option_span = option_label.find("span")
        option_text = option_span.text
        options.append(option_text)
    return options

def get_correct_option(question_row):
    return question_row["data-value"]

def get_question_image(question_row):
    question_image = question_row.find("img")
    return question_image["src"] if question_image else ""

def get_questions_for_page(examNum, pageNum):
    URL = "https://www.dmv-written-test.com/california/practice-test-" +  str(examNum) +".html?page=" + str(pageNum)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    questions_holder = soup.find("div", id="questions-holder")

    question_rows = questions_holder.find_all("div", class_="question-row")
    
    options = ["A","B","C"]
    
    for question_row in question_rows:
        question_obj = {}
        question_obj["id"] = str(uuid.uuid4())
        question_obj["serial_num"] = str(globals()['question_num'])
        globals()["question_num"] = globals()["question_num"] + 1
        question_obj["question_text"] = get_question_text(question_row)

        question_image = get_question_image(question_row)
        question_obj["has_image"] = len(question_image) > 0
        if question_image:
            question_obj["image_src"] = question_image
            if question_image not in globals()["downloaded_images"]:
                globals()["downloaded_images"].add(question_image)
                wget.download(question_image, out="images")


        question_obj["options"] = []
        answers_arr = get_answer_options(question_row)
        for idx, ans in enumerate(answers_arr):
            answer_obj = { "option": options[idx], "option_text": ans }
            question_obj["options"].append(answer_obj)
        
        question_obj["correct_option"] = get_correct_option(question_row)
        json_arr.append(question_obj)

    return json_arr
    
for exam in range(1,25):
    for page in range(1,8):
        print(f"Exam {exam} / Page {page}")
        questions_arr = get_questions_for_page(exam, page)
        json_file = open("exam1.json", "w")
        json_file.write(json.dumps(questions_arr, indent=2))
        json_file.close()
print("Done")
    