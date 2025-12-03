class Person:
    # __init__：实例创建后，会自动执行，用来“给对象上属性”
    def __init__(self, name, age):
        print("正在执行 __init__ ...")
        self.name = name
        self.age = age

    def introduce(self):
        print(f"我叫 {self.name}，今年 {self.age} 岁")


# 创建两个不同的人
p1 = Person("李堂", 20)
p2 = Person("小张", 18)

# 调用方法
p1.introduce()
p2.introduce()
