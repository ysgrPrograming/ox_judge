from collections import deque
import math

scene_size = 3**9

#局面の番号を状態(n進法のリスト)に変換する
def convert_10ton(x, n):
    li = []
    for _ in range(9):
        li.append(x%n)
        x //= n
    return li

#局面の状態(n進法のリスト)から番号に変換する
def convert_nto10(x, n):
    return sum([x[i]*n**i for i in range(len(x))])

#既に勝敗が決まっている場合評価値を出力する
#出力 = (決着がついているか(bool), 評価値(int))
check_li = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
def check_bingo(x):
    li = convert_10ton(x, 3)
    ret = None
    for items in check_li:
        if li[items[0]] == li[items[1]] == li[items[2]] and li[items[0]] != 0:
            if ret != None: return (True, 0)
            if li[items[0]] == 1:
                ret = (True, 1)
            else:
                ret = (True, -1)
    if ret: return ret
    if 0 not in li: return (True, 0)
    return (False, 0)

#局面の番号から、次にありえる局面を出力する
def list_next_scenes(t):
    li = convert_10ton(t%scene_size, 3)
    new_scenes = deque()
    for i in range(9):
        if li[i] == 0:
            new_scene = t%scene_size+3**i*(turn+1)+(turn+1)%2*scene_size
            new_scenes.append(new_scene)
    return new_scenes

#局面の番号から、状態を視覚的に出力する(デバッグ用)
def print_t(t):
    turn = t//scene_size
    li = convert_10ton(t, 3)
    sign_dic = {0: "□", 1: "o", 2: "x"}
    new_li = [sign_dic[li[i]] for i in range(9)]

    #print(turn)
    for i in range(3):
        print(*new_li[i*3:i*3+3])
    print()

#scenesリストに評価値を格納し、is_confirmedリストに評価値が確定済みか記録する
scenes = [0]*(scene_size*2)
is_confirmed = [False]*(scene_size*2)
for i in range(scene_size*2):
    if is_confirmed[i]: continue
    todo = deque([i])
    while todo:
        t = todo.pop()
        if is_confirmed[t]: continue
        #print_t(t)

        #局面の勝敗が既についている時
        c = check_bingo(t)
        if c[0]:
            scenes[t] = c[1]
            is_confirmed[t] = True
            #print("confirmed", scenes[t])
            continue

        #局面の勝敗がついていない時
        turn = t//scene_size
        li = convert_10ton(t%scene_size, 3)
        scene_val = 0
        if turn == 0:
            scene_val = -float('inf')
        else:
            scene_val = float('inf')

        #次の局面としてありえる局面の番号をnew_scenesに格納する
        #既に評価済みの場合、ミニマックス法に基づいて現局面の評価値を計算する
        new_scenes = list_next_scenes(t)
        for scene in new_scenes:
            if is_confirmed[scene]:
                if turn == 0:
                    scene_val = max(scene_val, scenes[scene])
                else:
                    scene_val = min(scene_val, scenes[scene])
            else:
                break

        else:
            #現局面を評価可能の場合、評価する
            scenes[t] = scene_val/2
            is_confirmed[t] = True
            #print("confirmed", scenes[t])

        #未探索の局面がある場合、探索を続行する
        if is_confirmed[t] == False:
            new_scenes.appendleft(t)
            todo.extend(new_scenes)

#入力
turn_dic = {"p": 0, "e": 1}
turn = turn_dic[input()]
data_list = []
for i in range(3):
    part = list(map(int, input().split(' ')))
    data_list.extend(part)
scene = convert_nto10(data_list, 3)+turn*scene_size

#出力
#必勝の有無、手数を宣言
if scenes[scene] < 0:
    num = int(-math.log2(abs(scenes[scene])))
    print("Enemy wins in", num, "moves")
elif scenes[scene] == 0:
    print("Draw")
else:
    num = int(-math.log2(abs(scenes[scene])))
    print("Player wins in", num, "moves")

#手順
print_t(scene)
while check_bingo(scene)[0] == False:
    scene_val = 0
    scene_num = 0
    turn = scene//scene_size
    if turn == 0:
        scene_val = -float('inf')
    else:
        scene_val = float('inf')

    li = list_next_scenes(scene)
    for i in li:
        if turn == 0:
            if scenes[i] > scene_val:
                scene_val = scenes[i]
                scene_num = i
        else:
            if scenes[i] < scene_val:
                scene_val = scenes[i]
                scene_num = i
    scene = scene_num
    if turn == 0:
        print("Player turn:")
    else:
        print("Enemy turn:")
    print_t(scene)

print("end")
