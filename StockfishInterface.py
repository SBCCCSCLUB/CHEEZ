import subprocess
import time

engine = subprocess.Popen(
    'stockfish_10_x64.exe',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)


def put(command):
    print('\nyou:\n\t' + command)
    engine.stdin.write(command + '\n')


def get():
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    # engine.stdin.write('isready\r\n')
    print('\nengine:')
    print(engine.stdout.readlines())
    engine.stdin.write('isready\r\n')

    #     if text == 'readyok':
    #         break
    #     if text !='':
    #         print('\t'+text)
    # # for line in engine.stdout:
    # #     print(line)


skill_level = 20

get()
put('uci')
get()
put('setoption name Hash value 128')
get()
put("setoption name Skill Level value " + str(skill_level))  # 0-20
get()
put('ucinewgame')
get()
put('position startpos moves e2e4 e7e5 f2f4')
get()
put('go infinite')
time.sleep(3)
get()
put('stop')
get()
put('quit')
