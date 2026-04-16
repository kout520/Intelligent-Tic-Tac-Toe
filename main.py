import sensor, time, pyb
from pyb import Pin
import chess

from qz_find import (

    ROI1, ROI2, ROI3, ROI4, ROI5, ROI6, ROI7, ROI8, ROI9,
    ROI1_1, ROI1_2, ROI1_3, ROI1_4,
    ROI2_1, ROI2_2, ROI2_3, ROI2_4,
    ROI3_1, ROI3_2, ROI3_3, ROI3_4,
    ROI4_1, ROI4_2, ROI4_3, ROI4_4,
    ROI5_1, ROI5_2, ROI5_3, ROI5_4,
    ROI6_1, ROI6_2, ROI6_3, ROI6_4,
    ROI7_1, ROI7_2, ROI7_3, ROI7_4,
    ROI8_1, ROI8_2, ROI8_3, ROI8_4,
    ROI9_1, ROI9_2, ROI9_3, ROI9_4,
    calculate_QiZi
)

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)  # 修改为RGB565模式
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)

sensor.set_auto_whitebal(False)  # 关闭自动白平衡
sensor.set_auto_gain(False)  # 关闭自动增益
sensor.set_auto_exposure(False)  # 关闭自动曝光
# 初始化串口
uart = pyb.UART(3, 115200)  # UART3, 波特率115200
# 添加定时器中断相关代码
tim = pyb.Timer(4)  # 使用定时器4
led_flag = 0
led_state = 0
# 配置定时器，周期500ms
tim.init(freq=4)  # 2Hz = 500ms
def timer_callback(timer):
    global led_state  # 声明使用全局变量
    if led_flag == 1:
        led_state = not led_state  # 翻转状态
        pin8.value(led_state)  #会影响识别，换一方法


tim.callback(timer_callback)
player_piece = None
ai_piece = None


# 全局变量
flag = 2  # 1: AI先下（执黑棋X）；2: 玩家先下（执任意颜色）
clock = time.clock()
led1 = pyb.LED(1)
pin0 = Pin('P0', Pin.IN, Pin.PULL_UP)  # 按键引脚
pin8 = Pin('P8', Pin.OUT)  # 亮灯引脚

#外部环境控制变量
an = -22
#反馈外部
j = 0



# 初始化棋盘状态
board = [[" " for _ in range(3)] for _ in range(3)]
previous_board = [[" " for _ in range(3)] for _ in range(3)]

last_move = None  # 记录最后一步棋 ('X'或'O')
first_player = None  # 先手玩家 ('X'或'O')

def get_majority_vote(detections):
    """从多次检测结果中获取众数"""
    freq = {}  # 使用普通字典代替 defaultdict
    for val in detections:
        if val in freq:
            freq[val] += 1
        else:
            freq[val] = 1
    # 返回出现次数最多的值
    return max(freq.items(), key=lambda x: x[1])[0]

def update_board_state(img):
    """更新棋盘状态（基于5次检测取众数）"""
    global QiZi1_1, QiZi1_2, QiZi1_3, QiZi2_1, QiZi2_2, QiZi2_3, QiZi3_1, QiZi3_2, QiZi3_3
    global board, previous_board, last_move, first_player

    # 保存上一次的棋盘状态
    for y in range(3):
        for x in range(3):
            previous_board[y][x] = board[y][x]

    # 每个位置进行5次检测并取众数
    positions = [
        (ROI1, ROI1_1, ROI1_2, ROI1_3, ROI1_4),  # (0,0)
        (ROI2, ROI2_1, ROI2_2, ROI2_3, ROI2_4),  # (0,1)
        (ROI3, ROI3_1, ROI3_2, ROI3_3, ROI3_4),  # (0,2)
        (ROI4, ROI4_1, ROI4_2, ROI4_3, ROI4_4),  # (1,0)
        (ROI5, ROI5_1, ROI5_2, ROI5_3, ROI5_4),  # (1,1)
        (ROI6, ROI6_1, ROI6_2, ROI6_3, ROI6_4),  # (1,2)
        (ROI7, ROI7_1, ROI7_2, ROI7_3, ROI7_4),  # (2,0)
        (ROI8, ROI8_1, ROI8_2, ROI8_3, ROI8_4),  # (2,1)
        (ROI9, ROI9_1, ROI9_2, ROI9_3, ROI9_4)   # (2,2)
    ]

    # 存储所有位置的5次检测结果
    all_detections = [[] for _ in range(9)]

    # 进行5轮检测
    for _ in range(5):
        for i, (roi, r1, r2, r3, r4) in enumerate(positions):
            result = calculate_QiZi(img, roi, r1, r2, r3, r4, 45, an)
            all_detections[i].append(result)

    # 获取每个位置的众数结果
    majority_results = [get_majority_vote(dets) for dets in all_detections]

    # 将众数结果映射到棋盘
    board[0][0] = "O" if majority_results[0] == 1 else ("X" if majority_results[0] == 2 else " ")
    board[0][1] = "O" if majority_results[1] == 1 else ("X" if majority_results[1] == 2 else " ")
    board[0][2] = "O" if majority_results[2] == 1 else ("X" if majority_results[2] == 2 else " ")
    board[1][0] = "O" if majority_results[3] == 1 else ("X" if majority_results[3] == 2 else " ")
    board[1][1] = "O" if majority_results[4] == 1 else ("X" if majority_results[4] == 2 else " ")
    board[1][2] = "O" if majority_results[5] == 1 else ("X" if majority_results[5] == 2 else " ")
    board[2][0] = "O" if majority_results[6] == 1 else ("X" if majority_results[6] == 2 else " ")
    board[2][1] = "O" if majority_results[7] == 1 else ("X" if majority_results[7] == 2 else " ")
    board[2][2] = "O" if majority_results[8] == 1 else ("X" if majority_results[8] == 2 else " ")

def check_violations(count_x, count_o, total_moves):
    """检测所有可能的违规行为"""
    global last_move, first_player,led_flag
    led_flag = 0
    if first_player is not None and total_moves >1:
        # 1. 检测棋子消失
        disappeared = []
        for y in range(3):
            for x in range(3):
                if previous_board[y][x] in ["O", "X"] and board[y][x] == " ":
                    disappeared.append((y, x, previous_board[y][x]))

        # 2. 检测新增棋子
        new_pieces = []
        #current_player = None
        for y in range(3):
            for x in range(3):
                if previous_board[y][x] == " " and board[y][x] in ["O", "X"]:
                    new_pieces.append((y, x, board[y][x]))
                    #current_player = board[y][x]

        # 3. 检测连续下棋
        if len(new_pieces) > 2:
            # 多个位置同时出现新棋子
            uart.write(b'A,1,3,4\n')
            led_flag = 1
            print("违规: 同时下了多颗棋子!")
        elif len(new_pieces) == 2:
            y, x, player = new_pieces[0]
            if last_move == player:
                uart.write(b'A,1,3,4\n')
                led_flag = 1
                print(f"违规: 玩家 {player} 连续下了两步!")
            last_move = player

        # 4. 检测棋子被修改
        if disappeared and not new_pieces:
            for y, x, player in disappeared:
                uart.write(b'A,1,3,4\n')
                led_flag = 1
                print(f"违规: 位置({y},{x})的{player}棋子被移除了!")
    if first_player == "X":
        if count_o > count_x or count_x > count_o + 1:
            uart.write(b'A,1,3,4\n')
            led_flag = 1

    if first_player == "O":
        if count_x > count_o or count_o > count_x + 1:
            uart.write(b'A,1,3,4\n')
            led_flag = 1



def print_board():
    """打印当前棋盘状态"""
    print("当前棋盘：")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

text0 = (26,18,22,200)#判断明暗
text1=(62,220,206,17)
text2=(282,16,14,193)
# 等待按键按下
def wait_key():
    global QiZi1_1, QiZi1_2, QiZi1_3, QiZi2_1, QiZi2_2, QiZi2_3, QiZi3_1, QiZi3_2, QiZi3_3,an,j,flag
    while pin0.value():
        img = sensor.snapshot()
        #身外判定(环境变化判定）
        statistics=img.get_statistics(roi=text0)
        statistics1=img.get_statistics(roi=text1)
        statistics2=img.get_statistics(roi=text2)
        grey = statistics.mean()
        grey1 = statistics1.mean()
        grey2 = statistics2.mean()

        grey0 = (grey+grey1+grey2)/3
        #print(grey0)
        img.draw_rectangle(text0)
        img.draw_rectangle(text1)
        img.draw_rectangle(text2)
        if grey0 < 40:#暗
            an = -15
            j = 1
        else:
            an = -22
            j = 0
        # 处理串口接收数据：在每个循环中检测是否有数据进入
        if uart.any():
            # 尽可能读取所有数据，注意这里假设接收到完整一行“AB\n”
            recv = uart.read().decode()  # 将字节串解码为字符串
            # 输出接收到的数据以便调试
            print("接收串口：", recv)
            # 判断接收到的字符串是否包含 "AB\n"
            if "Huan2\n" in recv:
                # 切换 flag 的值：如果当前为2则设置为1，否则设置为2
                flag = 1
                print("flag 切换为：玩家后手", flag)
            elif "Huan1\n" in recv:
                # 切换 flag 的值：如果当前为2则设置为1，否则设置为2
                flag = 2
                print("flag 切换为：玩家先手", flag)
        pin8.value(1)

    while not pin0.value():
        pin8.value(0)
        time.sleep_ms(30)
def reset_game():
    global board, player_piece, ai_piece,previous_board,last_move,first_player
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "],
    ]
    previous_board = [[" " for _ in range(3)] for _ in range(3)]
    last_move = None  # 记录最后一步棋 ('X'或'O')
    first_player = None  # 先手玩家 ('X'或'O')
    player_piece = None
    ai_piece = None

# 主循环
while True:

    clock.tick()
    wait_key()
    time.sleep_ms(200)
    img = sensor.snapshot()


    update_board_state(img)  # 更新棋盘状态

    print_board()            # 打印棋盘
    #反馈暗环境
    if j == 1:
        uart.write(b'A,1,3,5\n')


    # 检查游戏结果
    # 检查游戏结果（获胜或平局），注意在flag==2时只有当player_piece已确定后才判断玩家胜负
    if flag == 1:

        # 统计当前落子数
        count_x = sum(row.count("X") for row in board)
        count_o = sum(row.count("O") for row in board)
        total_moves = count_x + count_o
        # 模式1：AI先下（AI执X，玩家执O）
        first_player = "X"
        check_violations(count_x, count_o, total_moves)
        if chess.check_win(board, 'O') and led_flag == 0:
            print("你赢啦!")
            uart.write(b'A,1,3,0\n')
            reset_game()
            continue
        elif chess.check_win(board, 'X') and led_flag == 0:
            print("我赢啦！")
            uart.write(b'A,0,3,1\n')
            reset_game()
            continue
        elif chess.check_draw(board) and led_flag == 0:
            print("平局啦！")
            uart.write(b'A,1,3,2\n')
            reset_game()
            continue


        # 根据默认的 check_turn 判断当前轮到谁下（check_turn按 X先走规则）
        if chess.check_turn(board) == "X" and led_flag == 0:

                #led_flag = 0
                print("轮到X下棋！")
                line, col = chess.computer_move(board)
                # 更新内部棋盘状态
                board[line][col] = "X"
                uart_msg = 'A,0,{},{}\n'.format(line, col).encode()
                uart.write(uart_msg)
                print("Computer places X at ({},{})".format(line, col))

                sensor.flush()
        else:
            print("该你下棋（O）！")
            uart.write(b'A,1,3,3\n')  # 发送提示信号给玩家

    elif flag == 2:
        # 模式2：玩家先下；第一回合玩家落子后根据棋盘判断 player_piece 与 ai_piece
        # 只有当 player_piece 已确定后才判断游戏结果
        #检查犯规

        # 统计当前落子数
        count_x = sum(row.count("X") for row in board)
        count_o = sum(row.count("O") for row in board)
        total_moves = count_x + count_o
        #print(total_moves)
        check_violations(count_x, count_o, total_moves)
        #检查胜利
        if player_piece is not None and led_flag == 0:
            if chess.check_win(board, player_piece):
                print("{}赢啦!".format(player_piece))
                # 玩家胜时发送信号，例如A,1,3,0
                uart.write(b'A,1,3,0\n')
                reset_game()
                continue
            elif chess.check_win(board, ai_piece):
                print("{}赢啦!".format(ai_piece))
                uart.write(b'A,0,3,1\n')
                reset_game()
                continue
        # 平局判断
        if chess.check_draw(board) and led_flag == 0:
            print("平局啦！")
            uart.write(b'A,1,3,2\n')
            reset_game()
            continue

        # 如果玩家还未确定执棋颜色，则寻找第一个落子
        if player_piece is None and total_moves >= 1:
            found = False
            for i in range(3):
                for j in range(3):
                    if board[i][j] != " ":
                        player_piece = board[i][j]
                        first_player = player_piece
                        ai_piece = "O" if player_piece == "X" else "X"
                        print("玩家第一个落子在 ({},{}): {}。故玩家执 {}，AI执 {}。".format(i, j, board[i][j],
                                                                         player_piece, ai_piece))
                        found = True
                        break
                if found:
                    break

        # 当玩家还未落子时（总落子数为0），提示玩家下棋
        if total_moves == 0:
            print("轮到玩家下棋（还未落子），请落子……")
            uart.write(b'A,1,3,3\n')
        # 判断当前回合：玩家先下，所以总落子数为偶数时轮到玩家；为奇数时轮到AI
        elif total_moves % 2 == 0 and led_flag == 0:
            print("轮到玩家({})下棋！请落子……".format(player_piece))
            uart.write(b'A,1,3,3\n')
        else:
            print("轮到AI({})下棋！".format(ai_piece))
            # AI计算落子位置，调用 computer_move_for 并传入 ai_piece
            line, col = chess.computer_move_for(board, ai_piece)
            # 立即更新内存棋盘状态，防止摄像头采集时出现误判
            board[line][col] = ai_piece
            if ai_piece == "X" and led_flag == 0:

                    led_flag = 0
                    uart_msg = 'A,0,{},{}\n'.format(line, col).encode()
                    print("Computer places X at ({},{})".format(line, col))
                    uart.write(uart_msg)
            elif ai_piece == "O" and led_flag == 0:

                    led_flag = 0
                    uart_msg = 'A,1,{},{}\n'.format(line, col).encode()
                    print("Computer places O at ({},{})".format(line, col))
                    uart.write(uart_msg)

            sensor.flush()

    # 可在此增加适当延时，以避免循环过快（根据实际情况配置）
    #pin8.value(1)
    time.sleep_ms(10)
