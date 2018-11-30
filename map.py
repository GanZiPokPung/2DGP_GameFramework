from pico2d import *
import mainframe

class Map :
    image = None
    def __init__(self, name, subname, posy, mapSpeed):
        self.name = name
        self.subname = subname
        self.width = 500
        self.height = 4000
        # 250
        self.x = self.width / 2
        # 맵 시작위치 2000
        self.y = posy
        self.pushcheck = False
        self.endCheck = False
        if Map.image == None:
            Map.image = load_image(os.path.join(os.getcwd(), 'resources', 'map', 'Stage2_0.png'))
        #
        self.speed = mapSpeed

    def update(self, mapList):
        # 스피드에 따라 맵 이동
        self.y -= (self.speed) * mainframe.frame_time
        # 맵 이동 구간 체크
        # self.height / 2 = 2000
        # self.width + 2000 => 4000 + 2000 = 6000
        # 일정 구간에 다다르면 다음 맵을 리스트에 넣는다.
        if(self.pushcheck == False) and (self.y < 2000):
            mapList.append(Map(self.name, 1, 6000, self.speed))
            self.pushcheck = True
        else:
        # 캔버스에 벗어난 맵은 리스트에서 제거한다.
            if self.y < -3000:
                return True

        return False

    def draw(self):
        Map.image.draw(self.x, self.y)
        #print(self.y)