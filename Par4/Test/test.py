class YourClassName:
    def turn(self, dir, angle=0, loop=1, sleep=0.5, arm=False):
        """ parameter :
        dir : {LEFT, RIGHT}
        """
        dir_list = {
            "LEFT": {45: 159, 20: 158, 10: 157, 5: 156},
            "RIGHT": {45: 154, 20: 153, 10: 152, 5: 151}
        }

        while angle > 0:
            angles = list(dir_list[dir].keys())
            angles.sort(reverse=True)
            for a in angles:
                if angle >= a:
                    print(f"Rotating {dir} by {a} degrees. {angle}")
                    #self.TX_data_py2(dir_list[dir][a])
                    #time.sleep(sleep)
                    angle -= a
                    break
            if angle<5 and angle>2.5:
                print(f"Rotating {dir} by {a} degrees. {angle}")
                #self.TX_data_py2(dir_list[dir][a])
                #time.sleep(sleep)
                angle -= 5
            if angle<2.5:  
                print(f"Angle too small to rotate further. {angle}")
                break

# 입력값 테스트
your_class = YourClassName()
your_class.turn("LEFT", 88)  # 예시 입력: 29도

print("End")
