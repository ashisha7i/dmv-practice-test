import json
import requests
from bs4 import BeautifulSoup



URL = "https://www.dmv-written-test.com/california/practice-test-1.html?page=1"

page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="questions-main-content-holder")

question_rows = results.find_all("div", class_="question-row")

json_arr = []
json_obj = {}

for row in question_rows:
    questions = row.find_all("div", class_="question")
    for question in questions:
        question_text = question.find("h3")
        question_text_str = question_text.text
        json_obj["question"] = question_text_str[question_text_str.index(".")+1:].strip()
        answers = []
        idx = 1
        for ans in row.find_all("label", class_="form-check-label"):
            ans_obj = {}
            ans_obj["index"] = str(idx)
            ans_obj["text"] = ans.find("span").text
            answers.append(ans_obj)
            idx = idx + 1
        json_obj["answers"] = answers
    for explanation in row.find_all("div", class_="explanation-row"):
        full_explanation = explanation.find("div", class_="full-explanation")
        json_obj["explanation"] = full_explanation.find("summary").text.strip()
        json_obj["correct_answer"] ="TBD"
        json_arr.append(json_obj)

print(json.dumps(json_arr))