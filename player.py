from pico2d import *

MoveSpeed = 50
MoveSpeed *= 0.1

class Player:
    def __init__(self):
        self.x = 250
        self.y = 50
        self.dirX = 0
        self.dirY = 0
        #status
        self.deadcheck = False
        self.turncheck = False
        #key
        self.pushLcheck = False
        self.pushRcheck = False
        #frame
        self.frameID = 0
        self.frame = 0
        self.reformframe = 0
        #image
        self.image = load_image(os.path.join(os.getcwd(), 'player', 'player.png'))

    def handle_events(self, event):
        # 이동 구현

        # 키를 눌렀다면?
        if event.type == SDL_KEYDOWN:
            self.Move_State_DownKey(event.key)

        # 키를 떼었다면?
        elif event.type == SDL_KEYUP:
            self.Move_State_UpKey(event.key)

        # 동시에 눌렸을때는 그자리에 있는 스프라이트를 재생한다.
        if(self.pushLcheck == True) and (self.pushRcheck == True):
            self.turncheck = False

    # Key Input process
    # Move DownKey
    def Move_State_DownKey(self, key_state):
        if key_state == SDLK_UP:
            self.dirY += 1
        elif key_state == SDLK_DOWN:
            self.dirY -= 1
        # 좌
        elif key_state == SDLK_LEFT:
            # pushRcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
            # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushRcheck == False:
                self.turncheck = False
                self.frameID = 1
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            #
            self.dirX -= 1
            self.pushLcheck = True
        # 우
        elif key_state == SDLK_RIGHT:
            # pushLcheck가 켜져있다는 뜻은 동시에 눌리고 있다는 뜻이므로
            # 누른 키의 반대쪽 키가 눌리지 않았을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushLcheck == False:
                self.turncheck = False
                self.frameID = 2
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            #
            self.dirX += 1
            self.pushRcheck = True
    # Move UpKey
    def Move_State_UpKey(self, key_state):
        if key_state == SDLK_UP:
            self.dirY -= 1
        if key_state == SDLK_DOWN:
            self.dirY += 1
        # 좌
        elif key_state == SDLK_LEFT:
            # pushRcheck가 켜져있다는 뜻은 키를 뗌과 동시에 반대키가 눌리고 있다는 뜻이므로
            # 뗀 키의 반대쪽 키가 눌리고 있을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushRcheck == True:
                self.turncheck = True
                self.frameID = 2
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            else:
                self.turncheck = False
            #
            self.dirX += 1
            self.pushLcheck = False
        # 우
        elif key_state == SDLK_RIGHT:
            # pushLcheck가 켜져있다는 뜻은 키를 뗌과 동시에 반대키가 눌리고 있다는 뜻이므로
            # 뗀 키의 반대쪽 키가 눌리고 있을때 키에 알맞는 스프라이트를 재생한다.
            if self.pushLcheck == True:
                self.turncheck = True
                self.frameID = 1
                self.frame = 0
                self.reformframe = 6
                self.turncheck = True
            else:
                self.turncheck = False
            #
            self.dirX -= 1
            self.pushRcheck = False


    def update(self):
        #global stage_time
        #stage_time += 0.1
        if self.turncheck == True:
            # 회전 이동 상태일때
            # 회전 스프라이트 끝 장면에 프레임을 고정
            if self.frame < 6:
                self.frame = (self.frame + 1) % 7
        else:
            # 만약 회전 이동 상태가 아니라면 IDLE 상태로 돌아오는
            # 스프라이트를 재생한다.(프레임을 거꾸로 돌린다)
            if self.reformframe == 0:
                self.frameID = 0
                self.frame = (self.frame + 1) % 7
            else:
                self.reformframe = self.reformframe - 1
                self.frame = self.reformframe

        #이동 계산
        self.y += self.dirY * MoveSpeed
        self.x += self.dirX * MoveSpeed

    def draw(self):
        self.image.clip_draw(self.frame * 70, self.frameID * 70, 70, 70, self.x, self.y)

        # DEBUG
        # print(str(self.pushLcheck) + " " + str(self.pushRcheck))
