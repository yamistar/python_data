## 클래스 선언 부분 ##
class Car : 
    color = ""
    speed = 0

    # def __init__(self) :
    #     # 생성자, 이 부분에 초기화할 코드 입력 - 파라미터 없는 버젼
    #     self.color = "빨강"
    #     self.speed = 0

    def __init__(self, value1, value2) :
         # 생성자, 이 부분에 초기화할 코드 입력 - 파라미터 있는 버
         self.color = value1
         self.speed = value2

    def upSpeed(self, value) :
        self.speed += value
    
    def downSpeed(self, value) :
        self.speed -= value

## 메인 코드 부분 ##
# myCar1 = Car() # 파라미터 없이 호출
# myCar2 = Car()

myCar1 = Car("빨강", 30) # 파라미터 있이 호출
myCar2 = Car("파랑", 60)

print("자동차1의 색상은 %s이며, 현재 속도는 %dKm 입니다." % (myCar1.color, myCar1.speed))
print("자동차2의 색상은 %s이며, 현재 속도는 %dKm 입니다." % (myCar2.color, myCar2.speed))
