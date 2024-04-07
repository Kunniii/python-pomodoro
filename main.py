import getopt
import platform
import sys
from datetime import timedelta
from os import get_terminal_size, path, system
from time import localtime, sleep, strftime

from notifypy import Notify

fill = "█"
time = 60 * 60
repeat = 5
shortBreak = 5 * 60
longBreak = 15 * 60
cycle = 3
isInputOK = 0


def clearConsole():
    if platform.system() == "Windows":
        system("cls")
    else:
        system("clear")


def progressBar(iteration, total, prefix="", suffix="", pomodoro=0, cycle=0):
    global fill
    clearConsole()
    timeNow = strftime("%H:%M", localtime())
    length = int(int(get_terminal_size()[0]) - 80)
    percent = ("{0:.2f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + " " * (length - filledLength)
    toPrint = f"\n\n\tPomodoro {pomodoro} - Cycle {cycle}\n\t\t{timeNow} | {prefix} |{bar}| {percent}% {suffix}"
    print(toPrint)
    if iteration == total:
        print(toPrint + " " + chr(3))


def showProgressBar(sec, pomodoro, cycle):
    for i in range(0, sec + 1):
        sleep(1)
        progressBar(
            i,
            sec,
            "Running",
            "Completed | " + str(timedelta(seconds=sec - i)) + " left",
            pomodoro, 
            cycle
        )


def usage():
    a = """
Pomodoro in Command line
-h --help           Show this help dialog
-t --time           The time for one Pomodoro
-r --repeat         The repeat time for one long break
-s --short-break    Short break time after one Pomodoro
-l --long-break     Long break time after -r times
-c --cycle          Cycles for Pomodoro
-f --fill           Progressbar filling
-y --yes            Accept default time settings

By default:
    time        :   60  min
    repeat      :   5   times
    short-break :   5   min
    long-break  :   15  min
    cycle       :   3   cycle
    filling     :   █
"""

    print(a)


def startPomodoro(time, repeat, shortBreak, longBreak, cycle, fill):
    iconPath = path.abspath("./tomato.ico")
    if not path.isfile(iconPath):
        iconPath = None
    print("\n\n\t\tNew Pomodoro")
    print(f"\ttime        :   {time//60}   min")
    print(f"\trepeat      :   {repeat}   times")
    print(f"\tshort-break :   {shortBreak//60}   min")
    print(f"\tlong-break  :   {longBreak//60}   min")
    print(f"\tcycle       :   {cycle}   cycles")
    print(f"\n\n>> Starting in 3 senconds...")
    sleep(3)
    notify = Notify(
        default_notification_audio=path.abspath("./bell.wav"),
    )
    notify.application_name = "Pomodoro"
    notify.icon = iconPath
    notify.title = "Pomodoro starts"

    for i in range(cycle):
        print(f"\nStarting cycle {i+1}")
        notify.message = f"Starting cycle {i+1}"
        for j in range(repeat - 1):
            notify.send(block=False)
            showProgressBar(time, j+1, i+1)

            notify.title = "Pomodoro short break"
            notify.message = "It's time to take a short break"
            notify.send(block=False)

            showProgressBar(shortBreak, "Short break", i+1)
        showProgressBar(time)

        notify.title = "Pomodoro long break"
        notify.message = (
            f"You have finished {repeat} Pomodoros\nIt's time for a long break!!!"
        )
        notify.send(block=False)

        showProgressBar(longBreak, "Long break", i+1)


def getInput():
    global time, repeat, shortBreak, longBreak, cycle, fill

    print("Enter time (minute)              :   ", end="")
    time = int(input()) * 60
    print("Enter repeat time                :   ", end="")
    repeat = int(input())
    print("Enter short break time (minute)  :   ", end="")
    shortBreak = int(input()) * 60
    print("Enter long break time (minute)   :   ", end="")
    longBreak = int(input()) * 60
    print("Enter cycle                      :   ", end="")
    cycle = int(input())
    print("Enter filling style              :   ", end="")
    fill = input()


def main():
    global time, repeat, shortBreak, longBreak, cycle, fill

    if not (sys.argv[1:]):
        usage()
        print("\nDo you want to use default settings? Yes/No ", end="")
        n = input()

        while n.lower() not in ("y", "yes") and n.lower() not in ("n", "no"):
            print("Yes/No ", end="")
            n = input()
        if n.lower() in ("yes", "y"):
            pass
        elif n.lower() in ("no", "n"):
            getInput()
        isInputOK = 1
    else:
        try:
            opt, val = getopt.getopt(
                sys.argv[1:],
                "y:h:t:r:s:l:c:f:",
                (
                    "yes",
                    "help",
                    "time",
                    "repeat",
                    "short-break",
                    "long-break",
                    "cycle",
                    "fill",
                ),
            )
            for o, v in opt:
                if o in ("-y", "yes"):
                    break
                if o in ("-h", "--help"):
                    usage()
                if o in ("-t", "--time"):
                    time = int(v) * 60
                if o in ("-r", "--repeat"):
                    repeat = int(v)
                if o in ("-s", "--short-break"):
                    shortBreak = int(v) * 60
                if o in ("-l", "--long-break"):
                    longBreak = int(v) * 60
                if o in ("-c", "--cycle"):
                    cycle = int(v)
                if o in ("-f", "--fill"):
                    fill = v[0]
            isInputOK = 1
        except Exception:
            isInputOK = 0

        if not time or not repeat or not shortBreak or not longBreak or not cycle:
            print(
                "\nSomething were wrong!\nMake sure not thing is less than or equal 0!!\n"
            )
            sleep(1)
            print("See the usage below")
            sleep(1.5)
            isInputOK = 0

    if isInputOK:
        clearConsole()
        startPomodoro(time, repeat, shortBreak, longBreak, cycle, fill)
    else:
        usage()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nHave a good day!!\n\n")
