import random
#添加需要进行多少局 才可以退出游戏
Money = 100
赌博次数 = 0
贷款金额 = 0
利息率 = 0.1  # 10%的利息率
底注 = 1
整局正负 = 0  # 用于统计整局的正负情况
游戏局数 = 0  # 新增：用于记录游戏局数

# 随机生成大小
def random_size():
    return random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)

def get_user_input(prompt, valid_inputs):
    while True:
        value = input(prompt)
        if value in valid_inputs:
            return value
        print("输入错误，请重新输入！")

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("赌注必须大于0，请重新输入！")
        except ValueError:
            print("赌注输入错误，请输入一个有效的整数！")

def loan_policy():
    global Money, 贷款金额
    print("你的钱不够了，需要贷款吗？")
    loan_choice = get_user_input("是否贷款？(y/n): ", ["y", "n"])
    if loan_choice == "y":
        loan_amount = get_positive_integer("请输入贷款金额：")
        贷款金额 += loan_amount
        Money += loan_amount
        print(f"你贷款了 {loan_amount} 金币，当前贷款总额为 {贷款金额} 金币。")
    else:
        print("你选择不贷款，游戏结束。")
        print(f"你目前的积蓄为： {Money-贷款金额} 金币。")
        # exit()

def repay_loan():
    global Money, 贷款金额
    if 贷款金额 > 0:
        print(f"你当前的贷款总额为 {贷款金额} 金币。")
        repay_choice = get_user_input("是否还款？(y/n): ", ["y", "n"])
        if repay_choice == "y":
            repay_amount = get_positive_integer("请输入还款金额：")
            if repay_amount > Money:
                print("你没有足够的金币进行还款，请重新输入！")
                return
            if repay_amount > 贷款金额:
                print("还款金额超过了贷款总额，请重新输入！")
                return
            贷款金额 -= repay_amount
            Money -= repay_amount
            print(f"你还款了 {repay_amount} 金币，当前贷款总额为 {贷款金额} 金币。")

while True:
    if Money <= 1:
        loan_policy()
    print(f"整局正负情况： {整局正负} 金币")
    # 每次游戏需要支付底注
    if Money < 底注:
        print(f"你的金币不足 {底注} 金币，无法继续游戏。")
        loan_policy()
    Money -= 底注
    整局正负 -= 底注

    value = get_user_input("猜大小: 请输入n(大)或m(小)：", ["n", "m"])
    daxiaodexuanzezhi = "大" if value == "n" else "小"

    duzhu = get_positive_integer("赌注：")
    Money -= duzhu
    整局正负 -= duzhu

    random_value = random_size()
    sum_random = sum(random_value)
    touzizhi = "小" if sum_random < 11 else "大"

    if 赌博次数 < 3:
        Money += duzhu * 2
        整局正负 += duzhu * 2
        print("猜对了！")
        print(f"赌博次数: {赌博次数}")
        赌博次数 += 1
    else:
        if daxiaodexuanzezhi == touzizhi:
            Money += duzhu * 2
            整局正负 += duzhu * 2
            print("猜对了！")
        else:
            print("猜错了！")

    # 计算利息
    if 贷款金额 > 0:
        interest = int(贷款金额 * 利息率)
        Money -= interest
        贷款金额 += interest
        整局正负 -= interest
        print(f"你支付了 {interest} 金币的利息，当前贷款总额为 {贷款金额} 金币。")
        print(f"你目前的金币数为： {Money}")
    # 询问是否还款
    if 贷款金额 > 0 and Money > 0:
        repay_loan()

    print(f"你目前的金币数为： {Money}")

    # 新增：每局游戏结束后增加游戏局数
    游戏局数 += 1
    if 游戏局数 % 10 == 0:
        exit_choice = get_user_input(f"你已经进行了 {游戏局数} 局游戏，是否退出游戏？(y/n): ", ["y", "n"])
        if exit_choice == "y":
            print(f"你已经进行了 {游戏局数} 局游戏，游戏结束。")
            break

print("游戏结束！")
print(f"整局正负情况： {整局正负} 金币")
