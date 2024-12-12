import random

# 添加需要进行多少局 才可以退出游戏
Money = 100
gambling_count = 0
loan_amount = 0
interest_rate = 0.1  # 10%的利息率
base_bet = 1
total_profit_loss = 0  # 用于统计整局的正负情况
game_rounds = 0  # 新增：用于记录游戏局数

# 随机生成大小
def random_size():
    return random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)

def get_user_input(prompt, valid_inputs):
    while True:
        local_value = input(prompt)  # 使用局部变量 local_value
        if local_value in valid_inputs:
            return local_value
        print("输入错误，请重新输入！")

def get_positive_integer(prompt):
    while True:
        try:
            local_value = int(input(prompt))
            if local_value > 0:
                return local_value
            print("赌注必须大于0，请重新输入！")
        except ValueError:
            print("赌注输入错误，请输入一个有效的整数！")
def loan_policy():
    global Money, loan_amount
    print("你的钱不够了，需要贷款吗？")
    loan_choice = get_user_input("是否贷款？(y/n): ", ["y", "n"])
    if loan_choice == "y":
        loan_amount = get_positive_integer("请输入贷款金额：")
        Money += loan_amount
        print(f"你贷款了 {loan_amount} 金币，当前贷款总额为 {loan_amount} 金币。")
    else:
        print("你选择不贷款，游戏结束。")
        print(f"你目前的积蓄为： {Money - loan_amount} 金币。")
        # exit()

def repay_loan():
    global Money, loan_amount
    if loan_amount > 0:
        print(f"你当前的贷款总额为 {loan_amount} 金币。")
        repay_choice = get_user_input("是否还款？(y/n): ", ["y", "n"])
        if repay_choice == "y":
            repay_amount = get_positive_integer("请输入还款金额：")
            if repay_amount > Money:
                print("你没有足够的金币进行还款，请重新输入！")
                return
            if repay_amount > loan_amount:
                print("还款金额超过了贷款总额，请重新输入！")
                return
            loan_amount -= repay_amount
            Money -= repay_amount
            print(f"你还款了 {repay_amount} 金币，当前贷款总额为 {loan_amount} 金币。")

while True:
    if Money <= 1:
        loan_policy()
    print(f"整局正负情况： {total_profit_loss} 金币")
    # 每次游戏需要支付底注
    if Money < base_bet:
        print(f"你的金币不足 {base_bet} 金币，无法继续游戏。")
        loan_policy()
    Money -= base_bet
    total_profit_loss -= base_bet

    value = get_user_input("猜大小: 请输入n(大)或m(小)：", ["n", "m"])
    guess = "大" if value == "n" else "小"

    bet = get_positive_integer("赌注：")
    Money -= bet
    total_profit_loss -= bet

    random_value = random_size()
    sum_random = sum(random_value)
    result = "小" if sum_random < 11 else "大"

    if gambling_count < 3:
        Money += bet * 2
        total_profit_loss += bet * 2
        print("猜对了！")
        print(f"赌博次数: {gambling_count}")
        gambling_count += 1
    else:
        if guess == result:
            Money += bet * 2
            total_profit_loss += bet * 2
            print("猜对了！")
        else:
            print("猜错了！")

    # 计算利息
    if loan_amount > 0:
        interest = int(loan_amount * interest_rate)
        Money -= interest
        loan_amount += interest
        total_profit_loss -= interest
        print(f"你支付了 {interest} 金币的利息，当前贷款总额为 {loan_amount} 金币。")
        print(f"你目前的金币数为： {Money}")
    # 询问是否还款
    if loan_amount > 0 and Money > 0:
        repay_loan()

    print(f"你目前的金币数为： {Money}")

    # 新增：每局游戏结束后增加游戏局数
    game_rounds += 1
    if game_rounds % 10 == 0:
        exit_choice = get_user_input(f"你已经进行了 {game_rounds} 局游戏，是否退出游戏？(y/n): ", ["y", "n"])
        if exit_choice == "y":
            print(f"你已经进行了 {game_rounds} 局游戏，游戏结束。")
            break

print("游戏结束！")
print(f"整局正负情况： {total_profit_loss} 金币")
