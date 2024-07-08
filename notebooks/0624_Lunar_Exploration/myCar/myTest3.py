## 클래스 선언부
class Car :
    color = "" # 인스턴스 변수
    speed = 0  # 인스턴스 변수
    count = 0  # 클래스 변수 * 여러 인스턴스가 공유한다.

    def __init__(self) :
        self.speed = 0
        Car.count +=1

## 변수 선언부
myCar1, myCar2, = None, None

## 메인코드 부분
myCar1 = Car()
myCar1.speed = 30
print("자동차1의 현재속도는 %dkm, 생성된 자동차는 총 %s대입니다." % (myCar1.speed, Car.count))

myCar2 = Car()
myCar2.speed = 60
print("자동차2의 현재 속도는 %dkm, 생산된 자동차는 총 %d대입니다." % (myCar2.speed, myCar2.count))

