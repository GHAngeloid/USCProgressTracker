import sys
from USC_DB_Wrapper.db import DB, Scores, Charts

def debug():
    for item in new_list:
        print(item)
    print("S ranks:", count['S'], "/",len(new_list))
    print("AAA+ ranks:", count['AAA+'], "/",len(new_list))
    print("AAA ranks:", count['AAA'], "/",len(new_list))
    print("AA+ ranks:", count['AA+'], "/",len(new_list))
    print("AA ranks:", count['AA'], "/",len(new_list))
    print("A+ ranks:", count['A+'], "/",len(new_list))
    print("A ranks:", count['A'], "/",len(new_list))


# initialize DB connection with 'maps.db'
db = DB()

if len(sys.argv) < 3:
    print("Please compile with a level and grade. i.e. $ python app.py [level] [grade]")
    exit(1)

charts = Scores.get_top_score_of_chart_by_level(sys.argv[1])
new_list = []
count = {'S': 0, 'AAA+': 0, 'AAA': 0, 'AA+': 0, 'AA': 0}

if len(charts) == 0:
    print('Invalid chart level. Please use 1 to 20.')
    exit(1)

for entry in charts:
    grade = None
    if entry['miss'] == 0:
        grade = 'UC'
    elif entry['score'] is not None:
        if entry['score'] >= 9900000:
            count['S'] += 1
            grade = 'S'
        elif entry['score'] >= 9800000:
            count['AAA+'] += 1
            grade = 'AAA+'
        elif entry['score'] >= 9700000:
            count['AAA'] += 1
            grade = 'AAA'
        elif entry['score'] >= 9500000:
            count['AA+'] += 1
            grade = 'AA+'
        elif entry['score'] >= 9300000:
            count['AA'] += 1
            grade = 'AA'
        elif entry['score'] >= 9000000:
            grade = 'A+'
        elif entry['score'] >= 8700000:
            grade = 'A'
        elif entry['score'] >= 8000000:
            grade = 'B'
        elif entry['score'] >= 7000000:
            grade = 'C'
        else:
            grade = 'D'
    new_list.append({'artist':entry['artist'], 'title':entry['title'], 'level':entry['level'], 'score':entry['score'], 'grade':grade})

# if not exact
total = 0
if sys.argv[2] == 'S':
    total = count['S']
elif sys.argv[2] == 'AAA+':
    total = count['S'] + count['AAA+']
elif sys.argv[2] == 'AAA':
    total = count['S'] + count['AAA+'] + count['AAA']
elif sys.argv[2] == 'AA+':
    total = count['S'] + count['AAA+'] + count['AAA'] + count['AA+']
elif sys.argv[2] == 'AA':
    total = count['S'] + count['AAA+'] + count['AAA'] + count['AA+'] + count['AA']

# write progress into text file
f = open("text/" + sys.argv[1] + sys.argv[2] + ".txt", "w")
f.write(str(sys.argv[1]) + " " + str(sys.argv[2]) + ": " + str(total) + "/" + str(len(new_list)))
f.close()

# Uncomment to debug
#debug()

# last line. close db connection
del db
