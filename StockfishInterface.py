import subprocess
import time


class StockfishInterface:
    def __init__(self, skill_level=20):
        # define the engine
        self.engine = subprocess.Popen(
            'stockfish_10_x64.exe',
            universal_newlines=True,
            bufsize=1,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        # set position string
        self.position = "position startpos moves"
        # start the engine
        self.get()
        self.put('uci')
        self.get()
        self.put('setoption name Hash value 128')
        self.get()
        self.put("setoption name Skill Level value " + str(skill_level))  # 0-20
        self.get()
        self.put('ucinewgame')
        self.get()

    def put(self, command):
        print('\nyou:\n\t' + command)
        self.engine.stdin.write(command + '\n')

    def get(self):
        # using the 'isready' command (engine has to answer 'readyok')
        # to indicate current last line of stdout
        self.engine.stdin.write('isready\n')
        return_string = ""
        print('\nengine:')
        while True:
            text = self.engine.stdout.readline().strip()
            if text == 'readyok':
                break
            if text != '':
                print('\t' + text)
                return_string += text
        return

    def move(self, uci_string):
        self.position += " " + uci_string
        self.put(self.position)
        self.get()
        self.put('go movetime 1000')
        time.sleep(1)
        self.get()
        # self.put('stop')
        # self.get()

    def fen_start(self, fen_string):
        self.position = "position fen " + fen_string
