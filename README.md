# Password-Hacker-4-5
Hyperskill Password Hacker 4/5
The difference with the stage 5/5 is that you change if statement with catching exception with:
start = datetime.now()
....
finish = datetime.now()
difference = (finish - start).total_seconds()
if difference >= 0.1:
...
