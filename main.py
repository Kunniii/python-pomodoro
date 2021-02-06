from win10toast import ToastNotifier
from time import sleep
import sys, getopt

def usage():
    a = '''
        Pomodoro in Commandline
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
    iconPath = './tomato.ico'
    if not time or not repeat or not shortBreak or not longBreak or not cycle:
        print('Something were wrong!\nMake sure not thing is less than or equal 0!!')
        sleep(1)
        usage()

    text = f'''\n\n         New Pomodoro\n    time        :   {time/60}  min\n    repeat      :   {repeat}   times\n    short-break :   {shortBreak/60}   min\n    long-break  :   {longBreak/60}  min\n    cycle       :   {cycle}   cycles'''
    print(text)
    a = 1
    for i in range(cycle):
        print(f"Starting cycle {i+1}")
        noti.show_toast("Pomodoro", f"Start cycle of: {i+1}", duration=25, icon_path=iconPath)
        sleep(time-25)
        if a != repeat:
            noti.show_toast("Pomodoro", "It's time to take a short break", duration=25, icon_path=iconPath)
            sleep(shortBreak-25)
        else:
            noti.show_toast("Pomodoro",f"You have finished {repeat} Pomodoros\nIt's time for a long break!!!", duration=25, icon_path=iconPath)
            sleep(longBreak-25)
            a = 0
        a += 1


def main():
    time = 30*60
    repeat = 5
    shortBreak = 5*60
    longBreak = 15*60
    cycle = 3
    if not(sys.argv[1:]):
        usage()
        print("Do you want to use default settings? Y/N ", end='')
        n=input()
        if n.lower() == 'y':
            pass
        else:
            print('Enter time: ', end='')
            time=int(input())*60
            print('Enter repeat time: ', end='')
            repeat=int(input())
            print('Enter short break time: ', end='')
            shortBreak=int(input())*60
            print('Enter long break time: ', end='')
            longBreak=int(input())*60
            print('Enter cycle: ', end='')
            cycle=int(input())
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
        except:
            usage()
    startPomodoro(time, repeat, shortBreak, longBreak, cycle)

if __name__ == "__main__":
    main()
