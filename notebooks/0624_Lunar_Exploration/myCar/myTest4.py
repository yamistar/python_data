## 상속과 메소드 오버라이딩

## 클래스 선언부
class Car : 
    speed = 0
    def upSpeed(self, value) :
        self.speed += value

        print("현재 속도 (수퍼 클래스) : %d " % self.speed)

class Sedan(Car) :
    def upSpeed(self, value):  # 메소드 오버라이딩
        self.speed +=value

        if self.speed > 150 :
            self.speed = 150
            print("현재 속도 (서브클래스) : %d" % self.speed)

class Truck(Car) :
    pass
    
## 변수 선언부
sedan1, truck1 = None, None

## 메인 코드부
truck1 = Truck()
sedan1 = Sedan()

print("트럭 --> ", end="")
truck1.upSpeed(200)

print("승용차 --> ", end="")
sedan1.upSpeed(200)
