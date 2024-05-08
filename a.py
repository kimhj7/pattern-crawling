import numpy as np
base = 3000

multiply = 0
a1 = 1
a2 = 1
a3 = 2
a4 = 3
a5 = 4
a6 = 6
a7 = 8
a8 = 11
a9 = 15
a10 = 20
a11 = 30
a12 = 40
a13 = 60
a14 = 80
a15 = 120
a16 = 160
a17 = 240
a18 = 320
a19 = 480
a20 = 640


def chip_selection(price):
    # 칩 값과 이름을 튜플 리스트로 저장
    chips = [
        (500000, '6'),
        (100000, '5'),
        (25000, '4'),
        (5000, '3'),
        (2000, '2'),
        (1000, '1')
    ]

    # 결과를 저장할 문자열
    result = []

    for value, name in chips:
        if price >= value:
            count = price // value  # 해당 칩으로 몇 개 살 수 있는지 계산
            price %= value  # 남은 금액 계산
            if count > 0:
                result.append(f"{name}번칩 {int(count)}개")

    # 결과 출력
    print(", ".join(result))
    print(result)

def abc():
    global multiply

    multiply = base / a1

    return multiply

m = abc()

print(a1*m, a2*m, a3*m, a4*m, a5*m, a6*m, a7*m, a8*m, a9*m, a10*m, a11*m, a12*m, a13*m, a14*m, a15*m, a16*m, a17*m, a18*m, a19*m, a20*m)
print(chip_selection(a20*m))

