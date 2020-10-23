from github import Github, RateLimitExceededException
import time
import json

def save_in_file(filename,data):
    with open(filename,mode="r") as f:
        try: 
            prev_data = json.load(f) 
        except:
            prev_data = []
        data = prev_data + data
      
    with open(filename,mode="w") as f:
        f.write(json.dumps(data))
        
# github access token
g = Github("3fb8c2b912625949580df590b3deaa15b8bceee7")
repo = g.get_repo("microsoft/vscode")
issues = repo.get_issues(labels = ["feature-request"],state = "closed")
count = 0
data = []
filename = 'data_closed_with_comments.json'
for issue in issues:
    count += 1
    try:
        data.append({
            "title": issue.title,
            "description": issue.body,
            "createdAt": issue.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "state": issue.state,
            "number": issue.number,
            "comments": [comment.body for comment in issue.get_comments()]
        })
    except RateLimitExceededException as RE:
        save_in_file(filename,data)
        data.clear()
        print("up to rate limit , sleep for 1h")
        time.sleep(3600)
    
    if count % 100 == 0:
        print('{} issues got'.format(count))

save_in_file(filename,data)

print("total:{}".format(count))