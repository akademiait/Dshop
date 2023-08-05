# Dshop developed by Akademia IT

## Rules of engagement
Good reading on working with code changes and pull request is https://google.github.io/eng-practices/. It contains both views - change author and reviewer.

### Rules

1. Do not commit directly to `master` or `dev`. Both branches are protected.
2. Use pull request to add your work. Make pull request to `dev` branch.
   - After creating pull request use "reviewers" option on far right of the screen to request review from "akademiait/dshop" team, or you can request review from certain team member directly by mentioning their name.
      ![image](https://github.com/akademiait/Dshop/assets/989256/a5886335-b537-4a23-8655-1bcaba5c67ae)
   - One of the team members (or multiple) will perform code review and approve the pull request or requst changes.
   - If changes are requested, all comments have to be in constructive and friendly manner, as shown in https://google.github.io/eng-practices/review/reviewer/comments.html
   - It's a good thing to comment on the good parts of code with "Nice work" or something similar. 
3. Code quality and automated tests will be run and required to pass before pull request can be merged. 
4. At least one approval by other team member is required before pull request can be merged.
5. After pull request is approved and code quality + tests are passed, pull request is merged by the author.
6. It is author responsibility to watch over pull request, bump if there is no code review done, fix issues and merge pull request.

#### How to Set up

Clone repository to specific folder (ex. Dshop):
```
git clone https://github.com/akademiait/Dshop.git
```
You need to have installed Poetry package. If you don't have, please install using this command:
```
pip install poetry
```
Navigate to Dshop folder by command:
```
cd Dshop
```
Set poetry global option, to use project folder as place to hold Virtual environment (recommended):
```
poetry config virtualenvs.in-project true
```
Install virtual environment, using current dependencies:
```
poetry install
```
Copy file env-template to .env file using command:
```
# linux/mac
cp env-template .env

# windows
copy env-template .env
```
Start poetry virtual environment
```
poetry shell
```

Update local .env file as needed


Run project:
```
# linux/mac
./manage.py shell

# windows
python manage.py runserver
```

Open web browser and navigate to localhost address:  http://127.0.0.1:8000/ 