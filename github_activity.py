import requests
from bs4 import BeautifulSoup

levels = [
    "beginner",
    "intermediate",
    "advanced"
]
issue_types = [
    "code+review",
    "question",
    "solution+request",
    "solution",
]
member = dict()


def add_member(github_id):
    member[github_id] = dict()
    for issue_type in issue_types:
        member[github_id][issue_type] = 0
    member[github_id]["feedback"] = 0



def get_feedbacks(week, author, address):
    req = requests.get(address)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    raw_data = soup.select("div.timeline-comment-header.clearfix.d-block.d-sm-flex > h3")[1:]
    for data in raw_data:
        date = data.find("relative-time").get("datetime")
        parsed = data.find_all("a")
        user = parsed[1].get_text()
        # print("   ", (date, user), "(author)" if author == user else "")
        if not author == user:
            if not user in member:
                add_member(user)
            member[user]["feedback"] += 1



def get_issues(week, level, issue):
    address = "https://github.com/UNIST-Almight/ps-study-2021-fall/issues?"\
              "q=label%3A%22{}%22+label%3A%22{}%22+label%3A%22week+{}%22+"\
              .format(level, issue, week)
    # print()
    print("checking:", ("week+%s"%week, level, issue))
    # print()
    req = requests.get(address)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    raw_data = soup.select("div.flex-auto.min-width-0.p-2.pr-3.pr-md-2")
    for data in raw_data:
        date = data.find("relative-time").get("datetime")
        parsed = data.find_all("a")
        issue_address = parsed[0].get('href')
        author = parsed[-1].get_text()
        # print((date, author))
        if not author in member:
            add_member(author)
        member[author][issue] += 1
        if issue == issue_types[0]:
            print("    Issue: {}".format(issue_address))
            get_feedbacks(week, author, "https://github.com{}".format(issue_address))
    print()
    

################################
## test code
################################

week = int(input("Week #:"))
for level in levels:
    for issue in issue_types:
        get_issues(week, level, issue)

print()
for m in member:
    print('Github ID: %15s'%(m), member[m])