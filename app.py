import sys
from USC_DB_Wrapper.db import DB, Scores, Charts
from tkinter import *
from tkinter.ttk import *
from datetime import datetime

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


def app():
    if(cb_level.get() == '' or cb_grade.get() == ''):
        return
    print('[', datetime.today(), '] Submit clicked : Updating values for', cb_level.get(), cb_grade.get())

    # initialize DB connection with 'maps.db'
    db = DB()

    '''
    # Deprecated: CLI implementation
    if len(sys.argv) < 3:
        print("Please compile with a level and grade. i.e. $ python app.py [level] [grade]")
        exit(1)

    charts = Scores.get_top_score_of_chart_by_level(sys.argv[1])
    new_list = []
    count = {'S': 0, 'AAA+': 0, 'AAA': 0, 'AA+': 0, 'AA': 0}

    if len(charts) == 0:
        print('Invalid chart level. Please use 1 to 20.')
        exit(1)
    '''

    charts = Scores.get_top_score_of_chart_by_level(cb_level.get())
    new_list = []
    count = {'S': 0, 'AAA+': 0, 'AAA': 0, 'AA+': 0, 'AA': 0}

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
    if cb_grade.get() == 'S':
        total = count['S']
    elif cb_grade.get() == 'AAA+':
        total = count['S'] + count['AAA+']
    elif cb_grade.get() == 'AAA':
        total = count['S'] + count['AAA+'] + count['AAA']
    elif cb_grade.get() == 'AA+':
        total = count['S'] + count['AAA+'] + count['AAA'] + count['AA+']
    elif cb_grade.get() == 'AA':
        total = count['S'] + count['AAA+'] + count['AAA'] + count['AA+'] + count['AA']

    # write progress into text file
    f = open("text/" + cb_level.get() + cb_grade.get() + ".txt", "w")
    f.write(str(cb_level.get()) + " " + str(cb_grade.get()) + ": " + str(total) + "/" + str(len(new_list)))
    f.close()

    # Uncomment to debug
    #debug()

    # last line. close db connection
    del db
    
    label_update['text'] = 'Update complete. ' + cb_level.get() + cb_grade.get() + '.txt'


if __name__ == '__main__':
    root = Tk()
    root.title('USCProgressTracker')
    w = 300
    h = 150

    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    level_list = [17, 18, 19, 20]
    grade_list = ['S', 'AAA+', 'AAA', 'AA+', 'AA']

    Label(root, text='Level:').grid(row=0, column=0)
    cb_level = Combobox(root, state='readonly', values=level_list)
    cb_level.grid(row=0, column=1)

    Label(root, text='Grade:').grid(row=1, column=0)
    cb_grade = Combobox(root, state='readonly', values=grade_list)
    cb_grade.grid(row=1, column=1)

    Button(root, text='Submit', command=app).grid(row=2, column=1)
    Button(root, text='Quit', command=root.quit).grid(row=3, column=1)

    label_update = Label(root, text='')
    label_update.grid(row=4, column=1)

    root.mainloop()
