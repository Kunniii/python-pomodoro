from win10toast import ToastNotifier
from time import sleep
import sys, getopt
from getpass import getuser
from os import path
from datetime import timedelta

def progressBar (iteration, total, prefix = '', suffix = ''):
    length = 50
    fill = '█'
    printEnd = "\r"
    percent = ("{0:.2f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '.' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print(f'{prefix} |{bar}| {percent}% {suffix} {chr(3)}')

def showProgressBar(sec):
    for i in range(0, sec+1):
        sleep(1)
        progressBar(i, sec, '    Progress', "Completed | " + str(timedelta(seconds=sec-i)) + " left")

def usage():
    a = '''
        Pomodoro in Command line
-h --help           Show this help dialog
-t --time           The time for one Pomodoro
-r --repeat         The repeat time for one long break
-s --short-break    Short break time after one Pomodoro
-l --long-break     Long break time after -r times
-c --cycle          Cyles for Pomodoro

By defaut:
    time        :   30  min
    repeat      :   5   times
    short-break :   5   min
    long-break  :   15  min
    cycle       :   3   cycle'''

    print(a)

def startPomodoro(time, repeat, shortBreak, longBreak, cycle):
    noti = ToastNotifier()
    toastDuration = 10
    iconPath = f'C:\\Users\\{getuser()}\\tomato.ico'
    if not path.isfile(iconPath):
        iconPath=None
    print(f'''\n\n         New Pomodoro\n    time        :   {time//60}   min\n    repeat      :   {repeat}   times\n    short-break :   {shortBreak//60}   min\n    long-break  :   {longBreak//60}   min\n    cycle       :   {cycle}   cycles\n''')
    for i in range(cycle):
        print(f"\nStarting cycle {i+1}")
        noti.show_toast("Pomodoro", f"Starting cycle {i+1}", duration=toastDuration, icon_path=iconPath, threaded=1)
        for j in range(repeat):
            print(f'    Pomodoro {j+1}')
            showProgressBar(time)
            noti.show_toast("Pomodoro", "It's time to take a short break", duration=toastDuration, icon_path=iconPath, threaded=1)
            print(f"    Short Break")
            showProgressBar(shortBreak)
        noti.show_toast("Pomodoro",f"You have finished {repeat} Pomodoros\nIt's time for a long break!!!", duration=toastDuration, icon_path=iconPath, threaded=1)
        print(f"    Long Break")
        showProgressBar(longBreak)

def getInput():
    print('Enter time (minute)              :   ', end='')
    time=int(input())*60
    print('Enter repeat time                :   ', end='')
    repeat=int(input())
    print('Enter short break time (minute)  :   ', end='')
    shortBreak=int(input())*60
    print('Enter long break time (minute)   :   ', end='')
    longBreak=int(input())*60
    print('Enter cycle                      :   ', end='')
    cycle=int(input())

    return time, repeat, shortBreak, longBreak, cycle

def main():
    time = 30*60
    repeat = 5
    shortBreak = 5*60
    longBreak = 15*60
    cycle = 3
    isInputOK = 0
    if not(sys.argv[1:]):
        usage()
        print("\nDo you want to use default settings? Yes/No ", end='')
        n=input()
        
        while n.lower() not in ('y', 'yes') and n.lower() not in ('n', 'no'):
            print("Yes/No ", end='')
            n=input()
        if n.lower() in ('yes', 'y'):
            pass
        elif n.lower() in ('no', 'n'):
            time, repeat, shortBreak, longBreak, cycle = getInput()
        isInputOK = 1
    else:
        try:
            opt, val = getopt.getopt(sys.argv[1:], "h:t:r:s:l:c:", ("help", "time", "repeat", "short-break", "long-break", "cycle"))
            for o, v in opt:
                if o in ('-h', '--help'):
                    usage()
                if o in ('-t', '--time'):
                    time = int(v)*60
                if o in ('-r', '--repeat'):
                    repeat = int(v)
                if o in ('-s', '--short-break'):
                    shortBreak = int(v)*60
                if o in ('-l', '--long-break'):
                    longBreak = int(v)*60
                if o in ('-c', '--cycle'):
                    cycle = int(v)
            isInputOK = 1
        except:
            usage()
            isInputOK = 0
    
    if not time or not repeat or not shortBreak or not longBreak or not cycle:
        print('\nSomething were wrong!\nMake sure not thing is less than or equal 0!!\n')
        sleep(1)
        print('See the usage below')
        sleep(1.5)
        usage()
        isInputOK = 0
    
    if isInputOK:
        startPomodoro(time, repeat, shortBreak, longBreak, cycle)

if __name__ == "__main__":
    main()
