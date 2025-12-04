#####################################作者:丁真(化名)######################################################################
def signin():
    pwd_input1=input("请输入您要注册的密码:\n")
    pwd_input2=input("请确认您要注册的密码\n")
    if pwd_input1==pwd_input2:
        global pwd
        pwd=pwd_input1
    elif pwd_input1!=pwd_input2:
        print("前后密码不一致！")
        exit()


account={
    "name":"丁真",
    "money":1000
}

def show():
    print("=======菜单=======")
    print("请输入您要执行的功能:")
    print("=================")
    print("1、查询余额")
    print("2、存钱操作")
    print("3、取钱操作")
    print("4、查看日志")
    print("5、退出程序")
    print("=================")

def load():
    while True:
        show()

        # choice = int(input())
        choice_input = input()

        # 字符串不是数字 → 无效输入
        if not choice_input.isdigit():
            print("无效输入，请输入 1-5")
            continue

        choice = int(choice_input)

        # 数字不在 1-5 范围内 → 无效输入
        if choice not in (1, 2, 3, 4, 5):
            print("无效输入，请输入 1-5")
            continue


        if choice==1:
            print(f'您现在的余额为:{account["money"]}¥')
        elif choice==2:

            try:
                save_input = float(input("请输入存入金额"))
            except ValueError:
                print("金额必须是数字")
                continue

            if save_input <= 0:
                print("金额必须大于 0")
                continue

            save = save_input

            account["money"]+=save
            print(f"成功存入{save}元！")
            transaction.append({
                "type":"存入",
                "balance":account["money"],
                "amount":save

            })
        elif choice==3:
            try:
                take_input = float(input("请输入取出金额"))
            except ValueError:
                print("金额必须是数字")
                continue

            if take_input <= 0:
                print("金额必须大于 0")
                continue

            take = take_input

            # take = float(input("请输入您要取出的金额:"))
            account["money"]-=take
            print(f"成功取出{take}元！")
            transaction.append({
                "type": "取出",
                "balance": account["money"],
                "amount": take

            })

        elif choice==4:
            if not transaction:
                print("目前暂无记录")

            else:
                for _ in transaction:
                    print(f"类型:{_['type']},移动金额:{_['amount']},剩余存款:{_['balance']}")

        elif choice==5:
            print("正在退出中......")
            exit()


transaction=[]
'''transaction.append({
    "type":,
    "balance":,
    "amount":,
    
    
    
})'''




def login():
    for _ in range(3):
        input_pwd=input("请输入您的密码:\n")
        if input_pwd == pwd:
            print("登录成功！")
            load()
        else:
            print("密码错误！")
            continue
    print("登录失败，请稍后再试！")
    exit()

def menu():
    while True:
        print("1、登录")
        print("2、注册")
        try:
            pick_input = int(input("输入你要选择的功能:"))
        except ValueError:
            raise ValueError("只能是1或者2")
        if pick_input == 1:
            login()
        elif pick_input == 2:
            signin()
        else:
            print("不能输入无效的字符")
            continue

if __name__ == "__main__":
    menu()
'''v0.2更新内容:
1、解决了存钱取钱输入字符串报错导致系统崩溃的问题
2、增加了校验环节,增强了程序的稳定性
3、解决了在执行功能时输入字符串报错导致系统崩溃的问题
'''

"""v0.3更新内容:
1、更新了注册系统
2、优化了代码结构
"""

###以用户名为键，构建一个用户数据库，每个用户拥有独立的账户、密码和日志，通过登录会话控制访问权限