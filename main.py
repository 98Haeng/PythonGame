import pygame
import random

pygame.init() # 초기화 (반드시 필요) 
# 화면의 크기 설정
width = 700
height = 500
screen = pygame.display.set_mode((width, height)) 
# 화면 타이틀(제목) 설정
pygame.display.set_caption("선생님 몰래 춤추기") #게임 이름

## 이미지 모음
# 배경 이미지 불러오기
background = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/classroom.jpg")
# 선생님 이미지 가져오기
teach_write1 = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/선생님 판서 1.png")
teach_write2 = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/선생님 판서 2.png")
teacher_know = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/선생님 감시.png")
teacher_angry = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/선생님 인지.png")
current_teacher = teach_write1
# 학생 이미지
sit_student = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/앉은학생.png")
dance1 = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/춤학생 1.png")
dance2 = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/춤학생 2.png")
# 커서 이미지
cursor = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/cursor.png")
# 화살표 이미지
toleft = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/toleft.png")
toright = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/toright.png")
toup = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/toup.png")
todown = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/todown.png")
# 게임오버 화면
gameover = pygame.image.load("/Users/leeshinhaeng/Desktop/파이썬응용프로그래밍/파응프프로젝트/img/Game over.png")

current_image = sit_student

# 선생님 이미지 변경 시간과 관련된 변수
image_change_interval = 1000  # 이미지 변경 간격 (밀리초)
last_image_change_time = pygame.time.get_ticks()  # 마지막 이미지 변경 시간
# 2초에서 5초 사이의 랜덤한 시간 (선생님 인지로 바뀌는 시간)
next_new_image_time = last_image_change_time + random.randint(2000, 5000)

# image_files : 4개의 화살표
image_files = [toleft, toright, toup, todown]
# 랜덤으로 선택된 이미지
selected_image = random.choice(image_files) 
image_x = width  # 오른쪽 끝에서 시작
image_y = height/2  # 랜덤한 높이에서 시작
move_speed = 10 # 화살표 이동속도 (이는 점수에 따라 점점 증가)

# 점수 관련
losecount = 3 # 이 losercount가 0이 되면 게임오버
font = pygame.font.SysFont('Arial', 20) # 기본 폰트 지정
score = 0 # 점수는 0부터 시작
see_score = font.render('Your Score is {}'.format(score), True, (0, 0, 0)) # 점수 화면에 게시
see_losecount = font.render('Your Life is {}'.format(losecount), True, (0, 0, 0)) # 라이프 화면에 게시

# 게임 실행
clock = pygame.time.Clock()
run = True
game_over = False

# 시간 관련 변수
start_time = 0
elapsed_time = 0
# 초당 점수 증가 함수
def get_score():
    global score
    milliseconds = clock.tick(60)  # 매 초마다 점수를 증가시키기 위해 프레임 속도를 제한합니다 (60fps)
    seconds = milliseconds / 1000.0  # 초 단위로 변환
    score += seconds  # 초당 1씩 점수를 증가시킵니다

# 학생 이미지 변경 함수 (이미지 순환)
def now_student():
    global current_image
    if current_image == sit_student:
        current_image = dance1
    elif current_image == dance1:
        current_image = dance2
    else:
        current_image = dance1
# 일정 점수 도달시마다 점수 증가
def level_balance(score):
    global move_speed
    if score > 100:
        move_speed = 14
    if score > 200:
        move_speed = 18
    if score > 300:
        move_speed = 22
    if score > 400:
        move_speed = 26
    if score > 500:
        move_speed = 30

# correct_key 지정 함수 (selected_image에 따라 correct_key가 다름)
def cor_key(selected_image):
    global correct_key
    if selected_image == toleft: # 왼쪽 방향키 사진
        correct_key = pygame.K_LEFT
    if selected_image == toright: # 오른쪽 방향키 사진
        correct_key = pygame.K_RIGHT
    if selected_image == toup: # 위쪽 방향키 사진
        correct_key = pygame.K_UP
    if selected_image == todown: # 아래쪽 방향키 사진
        correct_key = pygame.K_DOWN

# 게임 오버 시 선생님이 분노하는 모습 나오게 하는 함수
def display_angry(angry=teacher_angry, background=background, student=current_image):
    screen.fill((0, 0, 0)) # 아무것도 없는 검은 색으로 채우기
    screen.blit(background, (0, 0)) # 배경 화면으로 채우기
    screen.blit(student, (0, 0)) # 현재 학생 이미지 화면으로 채우기
    screen.blit(angry, (0, 0)) # 선생님 화난 화면으로 채우기
    pygame.display.flip()

# 게임 오버 이후, 게임 오버 화면이 나오게끔 하기
def display_gameover(image=gameover):
    screen.fill((0, 0, 0)) # 아무것도 없는 검은 색으로 채우기
    screen.blit(image, (0, 0)) # Game Over 화면으로 채우기
    newfont = pygame.font.SysFont('Arial', 40)   # 폰트 크기 키우기
    see_score = newfont.render('Your Final Score is {}'.format(int(score)), True, (250, 0, 0)) # 최종 점수 출력
    screen.blit(see_score, [250,0]) # 최종 점수 개제
    pygame.display.flip() # 업데이트

while run:    
    screen.blit(background, (0, 0)) # 배경
    screen.blit(current_image, (0, 0)) # 현재 학생 모습
    screen.blit(current_teacher, (0, 0)) # 현재 선생님 모습
    screen.blit(cursor, (180,250)) # 커서 (클릭해야 하는 범위)
    screen.blit(selected_image, (image_x,image_y)) # 입력 허용범위 : 110~230
    screen.blit(see_score, [120,0])     # 점수
    screen.blit(see_losecount, [500, 0])  # 라이프

    # 매초마다 점수 1점씩 증가  
    get_score()
    see_score = font.render('Your Score is {}'.format(int(score)), True, (0, 0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: # 게임 종료시
                running = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # correct_key 받는 함수 (입력 방향키에 따라 다르게)
                cor_key(selected_image)
                # 정확한 키가 눌렸는지 확인
                if image_x >= 110 and image_x <= 230 and event.key == correct_key: # 지정 범위 (110~230) 사이인지, correct_key를 제대로 입력 했는지
                    print("정확히 눌렀습니다!") # score를 +해주는 방식으로 진행
                    score += 10 # 점수 10점 추가
                    see_score = font.render('Your Score is {}'.format(score), True, (0, 0, 0)) # 점수 화면 업데이트
                elif event.key == pygame.K_SPACE:
                    pass
                else:
                    print("잘못 눌렀습니다.") # 선생님이 인지하는 방향으로 진행
                    losecount -= 1 # 라이프 감소
                    see_losecount = font.render('Your Life is {}'.format(losecount), True, (0, 0, 0))
                # 일정 점수 도달시마다 move_speed 증가
                level_balance(score)
                # 학생 이미지 변경
                now_student()
            # 스페이스바를 누르면 원래 이미지(앉은 학생)로 돌아감
            elif event.key == pygame.K_SPACE:
                current_image = sit_student
            # 앉은 학생일 때 시작 시간 측정
            if current_image == sit_student:
                start_time = pygame.time.get_ticks()
            # 다른 상태라면 시작 시간은 0
            else:
                start_time = 0
    # 경과 시간 계산
    elapsed_time = pygame.time.get_ticks() - start_time
    # 앉은 상태에서, 7초동안 움직이지 않을 경우 게임 오버
    if current_image == sit_student and elapsed_time >= 7000:
        print("게임 오버!")
        game_over = True
    # 화살표 이미지 이동
    image_x -= move_speed # 점점 x좌표가 감소하게끔 작성
    # 이미지가 밖을 벗어나면, 오른쪽에서 다시 나오게끔
    if image_x < -50: 
        selected_image = random.choice(image_files)  # 새로운 이미지 선택
        image_x = width
    
    # 일정하게 선생님이 판서하는 모습 이미지를 재현할 수 있도록 코드 작성
    current_time = pygame.time.get_ticks() # 현재 시간을 밀리초 단위로 저장
    if current_time - last_image_change_time >= image_change_interval: 
        if current_teacher == teach_write1:
            current_teacher = teach_write2
        else:
            current_teacher = teach_write1
        last_image_change_time = current_time
    # 기존 선생님 이미지에서, 선생님이 인지하는 이미지가 랜덤한 타이밍에 생겨날 수 있게 조치
    if current_time >= next_new_image_time:
        # 새로운 이미지가 나타날 시간에 도달하면 이미지 변경
        current_teacher = teacher_know
        last_image_change_time = current_time
        if current_image != sit_student:
            losecount -= 1
            # 마지막 이미지 변경 시간(last_image_change_time)에서 2~5초 사이의 랜덤한 시간(random.randint(2000, 5000))을 더하여 다음 새로운 이미지가 나타날 시간을 설정
            see_losecount = font.render('Your Life is {}'.format(losecount), True, (0, 0, 0))
        # 마지막 변경 시간에서 랜덤하게 2~5초 이후 랜덤한 시간으로 선생님이 감지하는 이미지 등장
        next_new_image_time = last_image_change_time + random.randint(2000, 5000)  # 다음 새로운 이미지가 나타날 시간 갱신
    # 게임 오버 조건 (라이프 모두 소진)
    if losecount == 0:
        game_over = True  # losecount가 0이면 게임 오버 상태로 설정 -> if game_over (212번째 줄)로 연결
    clock.tick(120)
    screen.blit(see_score, [120,0])        # 점수 업데이트 후 표시
    screen.blit(see_losecount, [500, 0])   # 라이프 업데이트 후 표시
    # 게임 오버 화면 및 점수 출력
    if game_over:
        display_angry()
        pygame.time.wait(2000) # 2초 대기 후
        run=False # 게임 중단
        # 게임 오버 화면 함수 실행
        display_gameover()
        pygame.time.wait(3000)  # 5초 대기 후 자동 종료
# 게임 종료
pygame.quit()