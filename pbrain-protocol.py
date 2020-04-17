#!/usr/bin/env python3

import sys
import random
import copy
import multiprocessing
import time

goban = []
defense = True

class Game:
    def __init__(self):
        self.info = {
            "timeout_turn": 0,
            "timeout_match": 0,
            "max_memory": 0,
            "time_left": 0,
            "game_type": 0,
            "rule": 0,
            "evaluate": 0,
            "folder": ""
        }

    def print_board(self):
        for line in goban:
            for i in range(len(line)):
                print("------", end='')
            print()
            print("|", end='')
            for c in line:
                print("  " + c + "  |", end='')
            print()


    # =========================================================================== A.I ==========================================================================

    def playing_zone(self, tmp):
        list = []
        for i in range(len(tmp)):
            for j in range(len(tmp)):
                if tmp[i][j] == ' ' and (
                        (i < len(tmp) - 1 and tmp[i + 1][j] != ' ') or
                        (j < len(tmp) - 1 and tmp[i][j + 1] != ' ') or
                        (i >= 1 and tmp[i - 1][j] != ' ') or
                        (j >= 1 and tmp[i][j - 1] != ' ') or
                        (i < len(tmp) - 1 and j < len(tmp) - 1 and tmp[i + 1][j + 1] != ' ') or
                        (i >= 1  and j < len(tmp) - 1 and tmp[i - 1][j + 1] != ' ') or
                        (i < len(tmp) - 1 and j >= 1 and tmp[i + 1][j - 1] != ' ') or
                        (j >= 1 and i >= 1 and tmp[i - 1][j - 1] != ' ')):
                    list.append([i, j])
        return list

    def is_five(self, line):
        return "ooooo" in line

    def is_five_adv(self, line):
        return "xxxxx" in line

    def is_open_four(self, line):
        return " oooo " in line

    def is_open_four_adv(self, line):
        return " xxxx " in line

    def is_four(self, line):
        d = {
            " oooox",
            "xoooo ",
            "x oooox",
            "xo ooox",
            "xoo oox",
            "xooo ox",
            "xoooo x",
        }
        return any(x in line for x in d)

    def is_four_adv(self, line):
        d = {
            " xxxxo",
            "oxxxx ",
            "o xxxxo",
            "ox xxxo",
            "oxx xxo",
            "oxxx xo",
            "oxxxx o",
        }
        return any(x in line for x in d)

    def is_open_three(self, line):
        d = {
            "  ooo x",
            "  ooo  ",
            "  ooo ",
            " ooo  ",
            "x ooo  ",
            " oo o ",
            " o oo ",
        }
        return any(x in line for x in d)

    def is_open_three_adv(self, line):
        d = {
            "  xxx o",
            "  xxx  ",
            "  xxx ",
            " xxx  ",
            "o xxx  ",
            " xx x ",
            " x xx ",
        }
        return any(x in line for x in d)

    def is_three(self, line):
        d = {
            " ooox",
            "xooo ",
            "x ooo x",
            "xo oo ",
            "xoo o ",
            " o oox",
            " oo ox",
        }
        return any(x in line for x in d)

    def is_three_adv(self, line):
        d = {
            " xxxo",
            "oxxx ",
            "o xxx o",
            "ox xx ",
            "oxx x ",
            " x xxo",
            " xx xo",
        }
        return any(x in line for x in d)

    def is_open_two(self, line):
        d = {
            "  oo  ",
            "  o o  ",
            " o  o ",
        }
        return any(x in line for x in d)

    def is_open_two_adv(self, line):
        d = {
            "  xx  ",
            "  x x  ",
            " x  x ",
        }
        return any(x in line for x in d)

    def create_all_line(self, tmp):
        tab = []
        for line in tmp:
            tab.append(line)

        for i in range(len(tmp)):
            tab.append([item[i] for item in tmp])

        for j in range(len(tmp) - 4):
            diag = []
            for i in range(len(tmp) - j):
                diag.append(tmp[i + j][i])
            tab.append(diag)
        for j in range(1, len(tmp) - 4):
            diag = []
            for i in range(len(tmp) - j):
                diag.append(tmp[i][i + j])
            tab.append(diag)

        k = len(tmp) - 1
        for j in range(0, len(tmp) - 4):
            diag = []
            for i in range(len(tmp) - j):
                diag.append(tmp[i][k - i])
            k -= 1
            tab.append(diag)
        k = len(tmp) - 1
        for j in range(1, len(tmp) - 4):
            diag = []
            for i in range(len(tmp) - j):
                diag.append(tmp[k - i][i + j])
            tab.append(diag)

        return tab

    def attack(self):
        return

    def calc_adv_score(self, tmp, pos):
        score = 0
        temp = copy.deepcopy(tmp)
        temp[pos[0]][pos[1]] = 'x'
        lines = self.create_all_line(temp)
        for lin in lines:
            line = ''.join(lin)
            if self.is_five_adv(line):
                score += 1000000000
            if self.is_open_four_adv(line):
                score += 100000
            if self.is_four_adv(line):
                score += 30000
            if self.is_open_three_adv(line):
                score += 3000
            if self.is_three_adv(line):
                score += 250
            if self.is_open_two_adv(line):
                score += 100
        return score

    def calc_score(self, pos):
        score = 0
        othree = 0
        temp = copy.deepcopy(goban)
        temp[pos[0]][pos[1]] = 'o'
        score_adv = []
        zone = self.playing_zone(temp)
        for pos in zone:
            score_adv.append(self.calc_adv_score(temp, pos))
        lines = self.create_all_line(temp)
        for lin in lines:
            line = ''.join(lin)
            if self.is_five(line):
                score += 100000000000000
            if self.is_open_four(line):
                score += 50000
            if self.is_four(line):
                score += 250
            if self.is_open_three(line):
                othree += 1
                score += 175
            if self.is_three(line):
                score += 100
            if self.is_open_two(line):
                score += 125
        if othree >= 2:
            score += 20000
        return score - max(score_adv)

    def AI(self):
        timeout = time.time() + 4.8
        score = []
        zone = self.playing_zone(goban)
        # process_nb = len(zone)
        # pool = multiprocessing.Pool(processes=process_nb)
        # res = [pool.apply_async(self.calc_score, (pos,)) for pos in zone]
        # score = [result.get() for result in res]
        # score.append([result.get() for result in res])
        for pos in zone:
          score.append(self.calc_score(pos))
          if time.time() > timeout:
              break
        # print(score)
        # print(zone)
        x = score.index(max(score))
        return "{:d},{:d}".format(zone[x][0],zone[x][1])


    # =========================================================================== A.I ==========================================================================


    def handle_start(self, args):
        if len(args) != 1 or not args[0].isdigit() or int(args[0]) < 5:
            print("ERROR", flush=True)
        else:
            global goban
            goban = []
            for i in range(int(args[0])):
                line = [' ' for j in range(int(args[0]))]
                goban.append(line)
            print("OK", flush=True)

    def handle_restart(self, args):
        arg = [str(len(goban))]
        self.handle_start(arg)

    def handle_turn(self, args):
        if len(args) == 1:
            arg = args[0].split(',')
            if len(arg) != 2 or not arg[0].isdigit() or not arg[1].isdigit():
                print("ERROR", flush=True)
            else:
                goban[int(arg[0])][int(arg[1])] = 'x'
                pos = self.AI()
                print(pos, flush=True)
                pos = pos.rstrip().split(',')
                goban[int(pos[0])][int(pos[1])] = 'o'
        else:
            print("ERROR", flush=True)

    def handle_begin(self, _args):
        global defense
        defense = False
        x = len(goban) // 2
        goban[x][x] = 'o'
        print(str(len(goban) // 2) + "," + str(len(goban) // 2), flush=True)

    def handle_board(self, args):
        global goban
        size = len(goban)
        goban = []
        for i in range(size):
            line = [' ' for j in range(size)]
            goban.append(line)
        while True:
            line = input()
            if line == "DONE":
                pos = self.AI()
                print(pos, flush=True)
                pos = pos.rstrip().split(',')
                goban[int(pos[0])][int(pos[1])] = 'o'
                return
            args = line.split(',')
            if args[2] == "1":
                goban[int(args[0])][int(args[1])] = 'x'
            else:
                goban[int(args[0])][int(args[1])] = 'o'

    def handle_info(self, args):
        if len(args) == 2:

            if args[0] in ("timeout_turn", "timeout_match", "max_memory", "time_left", "game_type", "rule"):
                self.info[args[0]] = int(args[1])
            elif args[0] == "evaluate":
                self.info[args[0]] = [int(coord) for coord in args[1].split(',')]
            elif args[0] == "folder":
                self.info[args[0]] = str(args[1])


    def handle_end(self, _args):
        sys.exit(0)

    def handle_about(self, _args):
        print("name=\"NaniBrain\", version=\"1.0\", author=\"Nathalie HUGOT-POREZ & Arnaud LECLERCQ\", country=\"France\"", flush=True)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    random.seed()
    game = Game()

    d = {
        "START": game.handle_start,
        "RESTART": game.handle_restart,
        "TURN": game.handle_turn,
        "BEGIN": game.handle_begin,
        "BOARD": game.handle_board,
        "INFO": game.handle_info,
        "END":  game.handle_end,
        "ABOUT": game.handle_about,
    }

    for line in sys.stdin:
        line = line.rstrip()
        cmd = line.split(' ')
        args = cmd[1:]
        if cmd[0] not in d:
            print("CMD unknown", flush=True)
        else:
            d[cmd[0]](args)
