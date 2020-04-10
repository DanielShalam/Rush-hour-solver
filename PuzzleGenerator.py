import numpy as np
from Board import Board
import GameNodes
import random
import Hueristics
import Algorithm


def generetePuzzle(depth):
    depth = depth
    # print(puzzles_patterns[0])
    new_puzzles_patterns = []
    new_puzzles_with_depth = []

    for puzzle in puzzles_patterns:
        if puzzle[1] > depth:
            new_puzzles_patterns.append(puzzle)

    puzzle, g = random.choice(new_puzzles_patterns)

    initial_board = initFromString(puzzle)
    initial_board = Board(initial_board)
    root = GameNodes.Node(initial_board)
    _, _, _, _, _, _, _, _, nodes_path = Algorithm.aStarSearch(root, 1, False, 1)

    print("Generating random puzzle with depth " + str(depth) + "\n")
    print("depth is number of moves before XX path is clear\n")
    print(nodes_path[len(nodes_path) - depth - 1].board.board_state)

    return nodes_path[len(nodes_path) - depth - 1].board.board_state


def initFromString(_puzzle):
    board = np.chararray((1, 36))
    board[:] = [char for char in _puzzle]
    board = np.reshape(board, (6, 6))
    return board


puzzles_patterns = [["AA...OP..Q.OPXXQ.OP..Q..B...CCB.RRR.", 8],
                    ["A..OOOA..B.PXX.BCPQQQ.CP..D.EEFFDGG.", 8],
                    [".............XXO...AAO.P.B.O.P.BCC.P", 14],
                    ["O..P..O..P..OXXP....AQQQ..A..B..RRRB", 8],
                    ["AA.O.BP..OQBPXXOQGPRRRQGD...EED...FF", 9],
                    ["AA.B..CC.BOP.XXQOPDDEQOPF.EQ..F..RRR", 10],
                    [".ABBCD.A.ECD.XXE.F..II.F...H.....H..", 13],
                    ["...AAO..BBCOXXDECOFFDEGGHHIPPPKKIQQQ", 11],
                    [".ABBCC.A.DEEXX.DOFPQQQOFP.G.OHP.G..H", 11],
                    ["AAB.CCDDB..OPXX..OPQQQ.OP..EFFGG.EHH", 17],
                    ["OAAP..O..P..OXXP....BQQQ..B..E..RRRE", 25],
                    ["ABB..OA.P..OXXP..O..PQQQ....C.RRR.C.", 16],
                    ["AABBC...D.CO.EDXXOPE.FFOP..GHHPIIGKK", 18],
                    ["AAB.....B.CCDEXXFGDEHHFG..I.JJKKI...", 17],
                    [".AABB.CCDDOPQRXXOPQREFOPQREFGG.HHII.", 23],
                    ["AABBCOD.EECODFPXXO.FPQQQ..P...GG....", 20],
                    ["AOOO..A.BBCCXXD...EEDP..QQQPFGRRRPFG", 24],
                    ["AABO..CCBO..PXXO..PQQQ..PDD...RRR...", 24],
                    ["..ABB...A.J..DXXJ..DEEF..OOOF.......", 21],
                    ["A..OOOABBC..XXDC.P..D..P..EFFP..EQQQ", 11],
                    ["AABO..P.BO..PXXO..PQQQ...........RRR", 20],
                    ["..AOOOB.APCCBXXP...D.PEEFDGG.HFQQQ.H", 25],
                    ["..OOOP..ABBP..AXXP..CDEE..CDFF..QQQ.", 30],
                    ["..ABB..CA...DCXXE.DFF.E.OOO.G.HH..G.", 25],
                    ["AAB.CCDDB..OPXX.EOPQQQEOPF.GHH.F.GII", 29],
                    [".A.OOOBA.CP.BXXCPDERRRPDE.F..G..FHHG", 28],
                    ["ABBO..ACCO..XXDO.P..DEEP..F..P..FRRR", 28],
                    ["OOOA....PABBXXP...CDPEEQCDRRRQFFGG.Q", 29],
                    ["OOO.P...A.P.XXA.PBCDDEEBCFFG.HRRRG.H", 30],
                    ["O.APPPO.AB..OXXB..CCDD.Q.....QEEFF.Q", 32],
                    ["AA.OOO...BCCDXXB.PD.QEEPFFQ..P..QRRR", 36],
                    ["AAOBCC..OB..XXO...DEEFFPD..K.PHH.K.P", 39],
                    [".AR.BB.AR...XXR...IDDEEPIFFGHPQQQGHP", 39],
                    ["A..RRRA..B.PXX.BCPQQQDCP..EDFFIIEHH.", 43],
                    ["..OAAP..OB.PXXOB.PKQQQ..KDDEF.GG.EF.", 42],
                    ["OPPPAAOBCC.QOBXX.QRRRD.Q..EDFFGGE...", 44],
                    ["AAB.CCDDB.OPQXX.OPQRRROPQ..EFFGG.EHH", 46],
                    ["A..OOOABBC..XXDC.R..DEER..FGGR..FQQQ", 49],
                    ["..AOOO..AB..XXCB.RDDCEERFGHH.RFGII..", 51],
                    ["OAA.B.OCD.BPOCDXXPQQQE.P..FEGGHHFII.", 50]]
