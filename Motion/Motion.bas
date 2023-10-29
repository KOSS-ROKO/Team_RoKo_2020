DIM I       AS BYTE
DIM J       AS BYTE
DIM MODE    AS BYTE
DIM A          AS BYTE
DIM A_old    AS BYTE
DIM B       AS BYTE
DIM C       AS BYTE
DIM 보행속도    AS BYTE
DIM 좌우속도    AS BYTE
DIM 좌우속도2    AS BYTE
DIM 보행순서    AS BYTE
DIM 현재전압    AS BYTE
DIM 반전체크    AS BYTE
DIM 모터ONOFF    AS BYTE
DIM 자이로ONOFF AS BYTE
DIM 기울기앞뒤    AS INTEGER
DIM 기울기좌우    AS INTEGER
DIM 몇걸음 AS INTEGER
DIM 곡선방향 AS BYTE

DIM 넘어진확인 AS BYTE
DIM 기울기확인횟수 AS BYTE
DIM 보행횟수 AS BYTE
DIM 보행COUNT AS BYTE

DIM 적외선거리값  AS BYTE

DIM S11  AS BYTE
DIM S16  AS BYTE
'************************************************
DIM NO_0 AS BYTE
DIM NO_1 AS BYTE
DIM NO_2 AS BYTE
DIM NO_3 AS BYTE
DIM NO_4 AS BYTE

DIM NUM AS BYTE

DIM BUTTON_NO AS INTEGER
DIM SOUND_BUSY AS BYTE
DIM TEMP_INTEGER AS INTEGER

'**** 기울기센서포트 설정 ****
CONST 앞뒤기울기AD포트 = 0
CONST 좌우기울기AD포트 = 1
CONST 기울기확인시간 = 20  'ms

CONST 적외선AD포트  = 4

CONST min = 61   '뒤로넘어졌을때
CONST max = 107   '앞으로넘어졌을때
CONST COUNT_MAX = 3

CONST 머리이동속도 = 10
'************************************************
PTP SETON             '단위그룹별 점대점동작 설정
PTP ALLON            '전체모터 점대점 동작 설정

DIR G6A,1,0,0,1,0,0      '모터0~5번
DIR G6D,0,1,1,0,1,1      '모터18~23번
DIR G6B,1,1,1,1,1,1      '모터6~11번
DIR G6C,0,0,0,1,1,0      '모터12~17번
'************************************************
OUT 52,0   '머리 LED 켜기

'***** 초기선언 '************************************************
보행순서 = 0
반전체크 = 0
기울기확인횟수 = 0
보행횟수 = 1
모터ONOFF = 0

DIM 머리좌우    AS INTEGER
DIM 머리상하    AS INTEGER
CONST 좌우영점 = 100 
CONST 상하영점 = 113
머리좌우 = 좌우영점
머리상하 = 상하영점

'****초기위치 피드백*****************************
TEMPO 230
'MUSIC "cdefgh"

SPEED 5
GOSUB MOTOR_ON

S11 = MOTORIN(11)
S16 = MOTORIN(16)

SERVO 11, 100
SERVO 16, S16

SERVO 16, 100

GOSUB 전원초기자세
GOSUB 기본자세

GOSUB 자이로INIT
GOSUB 자이로MID
GOSUB 자이로ON

PRINT "VOLUME 200 !"
'PRINT "SOUND 12 !" '안녕하세요

GOSUB All_motor_mode3

GOTO MAIN   '시리얼 수신 루틴으로 가기
'************************************************
시작음:
    TEMPO 220
    'MUSIC "O23EAB7EA>3#C"
    RETURN
종료음:
    TEMPO 220
    MUSIC "O38GD<BGD<BG"
    RETURN
에러음:
    TEMPO 250
    MUSIC "GFFF"
    RETURN
'************************************************
MOTOR_ON: '전포트서보모터사용설정
    GOSUB MOTOR_GET
    MOTOR G6B
    DELAY 50
    MOTOR G6C
    DELAY 50
    MOTOR G6A
    DELAY 50
    MOTOR G6D
    모터ONOFF = 0
    GOSUB 시작음         
    RETURN
'************************************************
MOTOR_OFF:
    MOTOROFF G6B
    MOTOROFF G6C
    MOTOROFF G6A
    MOTOROFF G6D
    모터ONOFF = 1   
    GOSUB MOTOR_GET   
    GOSUB 종료음   
    RETURN
'************************************************
MOTOR_GET: '위치값피드백
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,1,1,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN
'************************************************
MOTOR_SET: '위치값피드백
    GETMOTORSET G6A,1,1,1,1,1,0
    GETMOTORSET G6B,1,1,1,0,0,1
    GETMOTORSET G6C,1,1,1,1,1,0
    GETMOTORSET G6D,1,1,1,1,1,0
    RETURN
'************************************************
All_motor_Reset:
    MOTORMODE G6A,1,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1,1
    MOTORMODE G6B,1,1,1,,,1
    MOTORMODE G6C,1,1,1,1,1
    RETURN
'************************************************
All_motor_mode2:
    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    MOTORMODE G6B,2,2,2,,,2
    MOTORMODE G6C,2,2,2,2,2
    RETURN
'************************************************
All_motor_mode3:
    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    MOTORMODE G6B,3,3,3,,,3
    MOTORMODE G6C,3,3,3,3,3
    RETURN
'************************************************
Leg_motor_mode1:
    MOTORMODE G6A,1,1,1,1,1
    MOTORMODE G6D,1,1,1,1,1
    RETURN
'************************************************
Leg_motor_mode2:
    MOTORMODE G6A,2,2,2,2,2
    MOTORMODE G6D,2,2,2,2,2
    RETURN
'************************************************
Leg_motor_mode3:
    MOTORMODE G6A,3,3,3,3,3
    MOTORMODE G6D,3,3,3,3,3
    RETURN
'************************************************
Leg_motor_mode4:
    MOTORMODE G6A,3,2,2,1,3
    MOTORMODE G6D,3,2,2,1,3
    RETURN
'************************************************
Leg_motor_mode5:
    MOTORMODE G6A,3,2,2,1,2
    MOTORMODE G6D,3,2,2,1,2
    RETURN
'************************************************
Arm_motor_mode1:
    MOTORMODE G6B,1,1,1,,,1
    MOTORMODE G6C,1,1,1,1,1
    RETURN
'************************************************
Arm_motor_mode2:
    MOTORMODE G6B,2,2,2,,,2
    MOTORMODE G6C,2,2,2,2,2
    RETURN
'************************************************
Arm_motor_mode3:
    MOTORMODE G6B,3,3,3,,,3
    MOTORMODE G6C,3,3,3,3,3
    RETURN
'************************************************
전원초기자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  35,  90, 190
    WAIT
    mode = 0
    RETURN
'************************************************
안정화자세:
    MOVE G6A,98,  76, 145,  93, 101, 100
    MOVE G6D,98,  76, 145,  93, 101, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  35,  90, 190
    WAIT
    mode = 0
    RETURN
'******************************************   
기본자세:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 0
    RETURN
'******************************************   
기본자세2:
    MOVE G6A,100,  76, 145,  93, 100, 100
    MOVE G6D,100,  76, 145,  93, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 0
    RETURN
'******************************************   
차렷자세:
    MOVE G6A,100, 56, 182, 76, 100, 100
    MOVE G6D,100, 56, 182, 76, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 2
    RETURN
'******************************************
앉은자세:
    GOSUB 자이로OFF
    MOVE G6A,100, 145,  28, 145, 100, 100
    MOVE G6D,100, 145,  28, 145, 100, 100
    MOVE G6B,100,  30,  80,
    MOVE G6C,100,  30,  80, 190
    WAIT
    mode = 1
    RETURN
'******************************************
'**** 자이로감도 설정 ****
자이로INIT:
    GYRODIR G6A, 0, 0, 1, 0,0
    GYRODIR G6D, 1, 0, 1, 0,0
    GYROSENSE G6A,200,150,30,150,0
    GYROSENSE G6D,200,150,30,150,0
    RETURN
'***********************************************
'**** 자이로감도 설정 ****
자이로MAX:
    GYROSENSE G6A,250,180,30,180,0
    GYROSENSE G6D,250,180,30,180,0

    RETURN
'***********************************************
자이로MID:
    GYROSENSE G6A,200,150,30,150,0
    GYROSENSE G6D,200,150,30,150,0

    RETURN
'***********************************************
자이로MIN:
    GYROSENSE G6A,200,100,30,100,0
    GYROSENSE G6D,200,100,30,100,0
    RETURN
'***********************************************
자이로ON:
    GYROSET G6A, 4, 3, 3, 3, 0
    GYROSET G6D, 4, 3, 3, 3, 0
    자이로ONOFF = 1
    RETURN
'***********************************************
자이로OFF:
    GYROSET G6A, 0, 0, 0, 0, 0
    GYROSET G6D, 0, 0, 0, 0, 0
    자이로ONOFF = 0
    RETURN
'**********************************************
RX_EXIT:

    ERX 4800, A, MAIN
    GOTO RX_EXIT
'**********************************************
GOSUB_RX_EXIT:

    ERX 4800, A, GOSUB_RX_EXIT2
    GOTO GOSUB_RX_EXIT

GOSUB_RX_EXIT2:
    RETURN
'****************************************
뒤로일어나기:
    HIGHSPEED SETOFF
    PTP SETON             
    PTP ALLON      

    GOSUB 자이로OFF
    GOSUB All_motor_Reset

    SPEED 15
    GOSUB 기본자세

    MOVE G6A,90, 130, 120,  80, 110, 100
    MOVE G6D,90, 130, 120,  80, 110, 100
    MOVE G6B,150, 160,  10, 100, 100, 100
    MOVE G6C,150, 160,  10, 190, 100, 100
    WAIT

    MOVE G6B,185, 160,  10, 100, 100, 100
    MOVE G6C,185, 160,  10, 190, 100, 100
    WAIT

    SPEED 12
    MOVE G6B,185,  50, 10,  100, 100, 100
    MOVE G6C,185,  50, 10,  190, 100, 100
    WAIT

    SPEED 10
    MOVE G6A, 80, 155,  80, 150, 150, 100
    MOVE G6D, 80, 155,  80, 150, 150, 100
    MOVE G6B,185,  20, 50,  100, 100, 100
    MOVE G6C,185,  20, 50,  190, 100, 100
    WAIT

    MOVE G6A, 75, 162,  55, 162, 155, 100
    MOVE G6D, 75, 162,  55, 162, 155, 100
    MOVE G6B,188,  10, 100, 100, 100, 100
    MOVE G6C,188,  10, 100, 190, 100, 100
    WAIT

    SPEED 10
    MOVE G6A, 60, 162,  30, 162, 145, 100
    MOVE G6D, 60, 162,  30, 162, 145, 100
    MOVE G6B,170,  10, 100, 100, 100, 100
    MOVE G6C,170,  10, 100, 190, 100, 100
    WAIT

    DELAY 200

    GOSUB Leg_motor_mode3   
    MOVE G6A, 60, 150,  28, 155, 140, 100
    MOVE G6D, 60, 150,  28, 155, 140, 100
    MOVE G6B,150,  60,  90, 100, 100, 100
    MOVE G6C,150,  60,  90, 190, 100, 100
    WAIT

    MOVE G6A,100, 150,  28, 140, 100, 100
    MOVE G6D,100, 150,  28, 140, 100, 100
    MOVE G6B,130,  50,  85, 100, 100, 100
    MOVE G6C,130,  50,  85, 190, 100, 100
    WAIT
    DELAY 100

    MOVE G6A,100, 150,  33, 140, 100, 100
    MOVE G6D,100, 150,  33, 140, 100, 100
    WAIT
    SPEED 10
    GOSUB 기본자세

    넘어진확인 = 1

    DELAY 200
    GOSUB 자이로ON

    RETURN
'**********************************************
앞으로일어나기:
    HIGHSPEED SETOFF
    PTP SETON             
    PTP ALLON

    GOSUB 자이로OFF

    HIGHSPEED SETOFF

    GOSUB All_motor_Reset

    SPEED 15
    MOVE G6A,100, 35,  70, 130, 100,
    MOVE G6D,100, 35,  70, 130, 100,
    MOVE G6B,15,  140,  15
    MOVE G6C,15,  140,  15
    WAIT

    SPEED 12
    MOVE G6B,15,  100,  10
    MOVE G6C,15,  100,  10
    WAIT

    SPEED 12
    MOVE G6A,100, 136,  35, 80, 100,
    MOVE G6D,100, 136,  35, 80, 100,
    MOVE G6B,15,  15,  75
    MOVE G6C,15,  15,  75
    WAIT

    SPEED 10
    MOVE G6A,100, 165,  75, 20, 100,
    MOVE G6D,100, 165,  75, 20, 100,
    MOVE G6B,15,  20,  95
    MOVE G6C,15,  20,  95
    WAIT

    DELAY 200

    GOSUB Leg_motor_mode3

    SPEED 8
    MOVE G6A,100, 165,  85, 20, 100,
    MOVE G6D,100, 165,  85, 20, 100,
    MOVE G6B,130,  50,  60
    MOVE G6C,130,  50,  60
    WAIT

    SPEED 8
    MOVE G6A,100, 165,  85, 30, 100,
    MOVE G6D,100, 165,  85, 30, 100,
    WAIT

    SPEED 8
    MOVE G6A,100, 155,  45, 110, 100,
    MOVE G6D,100, 155,  45, 110, 100,
    MOVE G6B,130,  50,  60
    MOVE G6C,130,  50,  60
    WAIT

    SPEED 6
    MOVE G6A,100, 145,  45, 130, 100,
    MOVE G6D,100, 145,  45, 130, 100,
    WAIT

    SPEED 8
    GOSUB All_motor_mode2
    GOSUB 기본자세
    넘어진확인 = 1

    DELAY 200
    GOSUB 자이로ON
    RETURN
'**********************************************
앞뒤기울기측정:
    FOR i = 0 TO COUNT_MAX
        A = AD(앞뒤기울기AD포트)   '기울기 앞뒤
        IF A > 250 OR A < 5 THEN RETURN
        IF A > MIN AND A < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF A < MIN THEN
        GOSUB 기울기앞
    ELSEIF A > MAX THEN
        GOSUB 기울기뒤
    ENDIF

    RETURN
'**************************************************
기울기앞:
    A = AD(앞뒤기울기AD포트)
    'IF A < MIN THEN GOSUB 앞으로일어나기
    IF A < MIN THEN
        ETX  4800,16
        GOSUB 뒤로일어나기

    ENDIF
    RETURN

기울기뒤:
    A = AD(앞뒤기울기AD포트)
    'IF A > MAX THEN GOSUB 뒤로일어나기
    IF A > MAX THEN
        ETX  4800,15
        GOSUB 앞으로일어나기
    ENDIF
    RETURN
'**************************************************
좌우기울기측정:
    FOR i = 0 TO COUNT_MAX
        B = AD(좌우기울기AD포트)   '기울기 좌우
        IF B > 250 OR B < 5 THEN RETURN
        IF B > MIN AND B < MAX THEN RETURN
        DELAY 기울기확인시간
    NEXT i

    IF B < MIN OR B > MAX THEN
        SPEED 8
        MOVE G6B,140,  40,  80
        MOVE G6C,140,  40,  80
        WAIT
        GOSUB 기본자세   
    ENDIF
    RETURN
'************************************************
SOUND_PLAY_CHK:
    DELAY 60
    SOUND_BUSY = IN(46)
    IF SOUND_BUSY = 1 THEN GOTO SOUND_PLAY_CHK
    DELAY 50

    RETURN
'************************************************
NUM_1_9:
    IF NUM = 1 THEN
        PRINT "1"
    ELSEIF NUM = 2 THEN
        PRINT "2"
    ELSEIF NUM = 3 THEN
        PRINT "3"
    ELSEIF NUM = 4 THEN
        PRINT "4"
    ELSEIF NUM = 5 THEN
        PRINT "5"
    ELSEIF NUM = 6 THEN
        PRINT "6"
    ELSEIF NUM = 7 THEN
        PRINT "7"
    ELSEIF NUM = 8 THEN
        PRINT "8"
    ELSEIF NUM = 9 THEN
        PRINT "9"
    ELSEIF NUM = 0 THEN
        PRINT "0"
    ENDIF

    RETURN
'************************************************
NUM_TO_ARR:
    NO_4 =  BUTTON_NO / 10000
    TEMP_INTEGER = BUTTON_NO MOD 10000

    NO_3 =  TEMP_INTEGER / 1000
    TEMP_INTEGER = BUTTON_NO MOD 1000

    NO_2 =  TEMP_INTEGER / 100
    TEMP_INTEGER = BUTTON_NO MOD 100

    NO_1 =  TEMP_INTEGER / 10
    TEMP_INTEGER = BUTTON_NO MOD 10

    NO_0 =  TEMP_INTEGER

    RETURN
'************************************************
Number_Play: '  BUTTON_NO = 숫자대입

    GOSUB NUM_TO_ARR

    PRINT "NPL "
    '*************

    NUM = NO_4
    GOSUB NUM_1_9

    '*************
    NUM = NO_3
    GOSUB NUM_1_9

    '*************
    NUM = NO_2
    GOSUB NUM_1_9
    '*************
    NUM = NO_1
    GOSUB NUM_1_9
    '*************
    NUM = NO_0
    GOSUB NUM_1_9
    PRINT " !"

    ' GOSUB SOUND_PLAY_CHK
    '    PRINT "SND 16 !"
    '    GOSUB SOUND_PLAY_CHK
    RETURN
    '************************************************
    RETURN
'************************************************
적외선거리센서확인:

    적외선거리값 = AD(적외선AD포트)

    IF 적외선거리값 > 50 THEN '50 = 적외선거리값 = 25cm
        'MUSIC "C"
        DELAY 200
    ENDIF

    RETURN
'******************************************
변수값_음성값출력:

    J = AD(적외선AD포트)   '적외선거리값 읽기
    BUTTON_NO = J
    GOSUB Number_Play
    GOSUB SOUND_PLAY_CHK
    GOSUB GOSUB_RX_EXIT

    RETURN
'************************************************  
MAIN: '라벨설정

    ETX 4800, 38 ' 동작 멈춤 확인 송신 값

MAIN_2:
    GOSUB 앞뒤기울기측정
    GOSUB 좌우기울기측정
    GOSUB 적외선거리센서확인

    ERX 4800,A,MAIN_2   

    A_old = A

    '**** 입력된 A값이 0 이면 MAIN 라벨로 가고
    '**** 1이면 KEY1 라벨, 2이면 key2로... 가는문
    ON A GOTO MAIN,KEY1,KEY2,KEY3,KEY4,KEY5,KEY6,KEY7,KEY8,KEY9,KEY10,KEY11,KEY12,KEY13,KEY14,KEY15,KEY16,KEY17,KEY18,KEY19,KEY20,KEY21,KEY22,KEY23,KEY24,KEY25,KEY26,KEY27,KEY28,KEY29,KEY30,KEY31,KEY32,KEY33,KEY34,KEY35,KEY36,KEY37,KEY38,KEY39,KEY40,KEY41,KEY42,KEY43,KEY44,KEY45,KEY46,KEY47,KEY48,KEY49,KEY50,KEY51,KEY52,KEY53,KEY54,KEY55,KEY56,KEY57,KEY58,KEY59,KEY60,KEY61,KEY62,KEY63,KEY64,KEY65,KEY66,KEY67,KEY68,KEY69,KEY70,KEY71,KEY72,KEY73,KEY74,KEY75,KEY76,KEY77,KEY78,KEY79,KEY80,KEY81,KEY82,KEY83,KEY84,KEY85,KEY86,KEY87,KEY88,KEY89,KEY90,KEY91,KEY92,KEY93,KEY94,KEY95,KEY96,KEY97,KEY98,KEY99,KEY100,KEY101,KEY102,KEY103,KEY104,KEY105,KEY106,KEY107,KEY108,KEY109,KEY110,KEY111,KEY112,KEY113,KEY114,KEY115,KEY116,KEY117,KEY118,KEY119,KEY120,KEY121,KEY122,KEY123,KEY124,KEY125,KEY126,KEY127,KEY128,KEY129,KEY130,KEY131,KEY132,KEY133,KEY134,KEY135,KEY136,KEY137,KEY138,KEY139,KEY140,KEY141,KEY142,KEY143,KEY144,KEY145,KEY146,KEY147,KEY148,KEY149,KEY150,KEY151,KEY152,KEY153,KEY154,KEY155,KEY156,KEY157,KEY158,KEY159,KEY160,KEY161,KEY162,KEY163,KEY164,KEY165,KEY166,KEY167,KEY168,KEY169,KEY170,KEY171,KEY172,KEY173,KEY174,KEY175,KEY176,KEY177,KEY178,KEY179,KEY180
'*****책갈피

    IF A > 100 AND A < 110 THEN
        BUTTON_NO = A - 100
        GOSUB Number_Play
        GOSUB SOUND_PLAY_CHK
        GOSUB GOSUB_RX_EXIT


    ELSEIF A = 250 THEN
        GOSUB All_motor_mode3
        SPEED 4
        MOVE G6A,100,  76, 145,  93, 100, 100
        MOVE G6D,100,  76, 145,  93, 100, 100
        MOVE G6B,100,  40,  90,
        MOVE G6C,100,  40,  90,
        WAIT
        DELAY 500
        SPEED 6
        GOSUB 기본자세

    ENDIF

    GOTO MAIN   
'*******************************************
'      MAIN 라벨로 가기
'*******************************************
'실험
KEY1:
    ETX  4800,1
    GOTO 좌어드레스
    GOTO RX_EXIT 
KEY2:
    ETX  4800,2
    GOTO 좌추후퍼팅1
    GOTO RX_EXIT
KEY3:
    ETX  4800,3
    GOTO 좌추후퍼팅2
    GOTO RX_EXIT
KEY4:
    ETX  4800,4
    GOTO 왼쪽턴5
    GOTO RX_EXIT
KEY5:
    ETX  4800,5
    GOSUB 왼쪽턴10
    GOTO RX_EXIT
KEY6:
    ETX  4800,6
    GOTO 왼쪽턴20
    GOTO RX_EXIT
KEY7:
    ETX  4800,7
    GOTO 왼쪽턴45
    GOTO RX_EXIT
KEY8:
    ETX  4800,8
    GOTO 왼쪽턴60
    GOTO RX_EXIT
KEY9:
    ETX  4800,9
    GOTO 오른쪽턴5
    GOTO RX_EXIT
KEY10: '0
    ETX  4800,10
    GOTO 오른쪽턴10
    GOTO RX_EXIT
KEY11: ' ▲
    ETX  4800,11
    GOTO 오른쪽턴20
    GOTO RX_EXIT
KEY12: ' ▼
    ETX  4800,12
    GOTO 오른쪽턴45
    GOTO RX_EXIT
KEY13: '▶
    ETX  4800,13
    GOTO 오른쪽턴60
    GOTO RX_EXIT
KEY14: ' ◀
    ETX  4800,14
    'GOTO 왼쪽옆으로70연속_골프
    GOTO RX_EXIT
KEY15: ' A
    ETX  4800,15
    'GOTO 왼쪽옆으로20_골프
    GOTO RX_EXIT
KEY16: ' POWER
    ETX  4800,16
    GOSUB Leg_motor_mode3
    IF MODE = 0 THEN
        SPEED 10
        MOVE G6A,100, 140,  37, 145, 100, 100
        MOVE G6D,100, 140,  37, 145, 100, 100
        WAIT
    ENDIF
    SPEED 4
    GOSUB 앉은자세   
    GOSUB 종료음

    GOSUB MOTOR_GET
    GOSUB MOTOR_OFF

    GOSUB GOSUB_RX_EXIT
KEY16_1:
    IF 모터ONOFF = 1  THEN
        OUT 52,1
        DELAY 200
        OUT 52,0
        DELAY 200
    ENDIF
    ERX 4800,A,KEY16_1
    ETX  4800,A

    '**** RX DATA Number Sound ********
    BUTTON_NO = A
    GOSUB Number_Play
    GOSUB SOUND_PLAY_CHK

    IF  A = 16 THEN    '다시 파워버튼을 눌러야만 복귀
        GOSUB MOTOR_ON
        SPEED 10
        MOVE G6A,100, 140,  37, 145, 100, 100
        MOVE G6D,100, 140,  37, 145, 100, 100
        WAIT

        GOSUB 기본자세2
        GOSUB 자이로ON
        GOSUB All_motor_mode3
        GOTO RX_EXIT
    ENDIF

    GOSUB GOSUB_RX_EXIT
    GOTO KEY16_1

    GOTO RX_EXIT
KEY17: ' C
    ETX  4800,17
    'GOTO 머리왼쪽90도
    GOTO RX_EXIT
KEY18: ' E
    ETX  4800,18   
    'GOSUB 자이로OFF
    GOSUB 에러음
KEY18_wait:
    ERX 4800,A,KEY18_wait   

    IF  A = 26 THEN
        GOSUB 시작음
        GOSUB 자이로ON
        GOTO RX_EXIT
    ENDIF

    GOTO KEY18_wait
    GOTO RX_EXIT
KEY19: ' P2
    ETX  4800,19
    'GOTO 오른쪽턴60_골프
    GOTO RX_EXIT
KEY20: ' B   
    ETX  4800,20
    'GOTO 오른쪽옆으로20_골프
    GOTO RX_EXIT
KEY21: ' △
    ETX  4800,21
    GOTO 고개상향3
    GOTO RX_EXIT
KEY22: ' *   
    ETX  4800,22
    'GOTO 왼쪽턴45_골프
    GOTO RX_EXIT
KEY23: ' G
    ETX  4800,23
    GOTO RX_EXIT
KEY24: ' #
    ETX  4800,24
    'GOTO 오른쪽턴45_골프
    GOTO RX_EXIT
KEY25: ' P1
    ETX  4800,25
    'GOTO 왼쪽턴60_골프
    GOTO RX_EXIT
KEY26: ' ■
    ETX  4800,26

    SPEED 5
    GOSUB 기본자세2   
    TEMPO 220
    'MUSIC "ff"
    GOSUB 기본자세
    GOTO RX_EXIT
KEY27: ' D
    ETX  4800,27
    'GOTO 머리오른쪽90도
    GOTO RX_EXIT
KEY28: ' ◁
   ETX 4800,28
   'GOTO 고개좌향3
   GOTO RX_EXIT
KEY29: ' □
    ETX  4800,29
    'GOTO 고개중앙
    GOTO RX_EXIT
KEY30: ' ▷
    ETX  4800,30
    'GOTO 고개우향3
    GOTO RX_EXIT
KEY31: ' ▽
    ETX  4800,31
    'GOTO 고개하향3
    GOTO RX_EXIT
KEY32: ' F
    ETX  4800,32
    'GOTO 후진종종걸음_골프
    GOTO RX_EXIT
'***********************************
KEY33:
    ETX 4800,33
    GOTO RX_EXIT
KEY34:
    ETX 4800,34
    GOTO RX_EXIT
KEY35:
    ETX 4800,35
    GOTO RX_EXIT
KEY36:
    ETX 4800,36
    GOTO RX_EXIT
KEY37:
    ETX 4800,37
    GOTO RX_EXIT
KEY38:
    ETX 4800,38
    GOTO RX_EXIT
KEY39:
    ETX 4800,39
    GOTO RX_EXIT
KEY40:
    ETX 4800,40
    GOTO RX_EXIT
KEY41:
    ETX 4800,41
    GOTO RX_EXIT
KEY42:
    ETX 4800,42
    GOTO RX_EXIT
KEY43:
    ETX 4800,43
    GOTO RX_EXIT
KEY44:
    ETX 4800,44
    GOTO RX_EXIT
KEY45:
    ETX 4800,45
    GOTO RX_EXIT
KEY46:
    ETX 4800,46
    GOTO RX_EXIT
KEY47:
    ETX 4800,47
    GOTO RX_EXIT
KEY48:
    ETX 4800,48
    GOTO RX_EXIT
KEY49:
    ETX 4800,49
    GOTO RX_EXIT
KEY50:
    ETX 4800,50
    GOTO RX_EXIT
KEY51:
    ETX 4800,51
    GOTO RX_EXIT
KEY52:
    ETX 4800,52
    GOTO RX_EXIT
KEY53:
    ETX 4800,53
    GOTO RX_EXIT
KEY54:
    ETX 4800,54
    GOTO RX_EXIT
KEY55:
    ETX 4800,55
    GOTO RX_EXIT
KEY56:
    ETX 4800,56
    GOTO RX_EXIT
KEY57:
    ETX 4800,57
    GOTO RX_EXIT
KEY58:
    ETX 4800,58
    GOTO RX_EXIT
KEY59:
    ETX 4800,59
    GOTO RX_EXIT
KEY60:
    ETX 4800,60
    GOTO RX_EXIT
KEY61:
    ETX 4800,61
    GOTO RX_EXIT
KEY62:
    ETX 4800,62
    GOTO RX_EXIT
KEY63:
    ETX 4800,63
    GOTO RX_EXIT
KEY64:
    ETX 4800,64
    GOTO RX_EXIT
KEY65:
    ETX 4800,65
    GOTO RX_EXIT
KEY66:
    ETX 4800,66
    GOTO RX_EXIT
KEY67:
    ETX 4800,67
    GOTO RX_EXIT
KEY68:
    ETX 4800,68
    GOTO RX_EXIT
KEY69:
    ETX 4800,69
    GOTO RX_EXIT
KEY70:
    ETX 4800,70
    GOTO RX_EXIT
KEY71:
    ETX 4800,71
    GOTO RX_EXIT
KEY72:
    ETX 4800,72
    GOTO RX_EXIT
KEY73:
    ETX 4800,73
    GOTO RX_EXIT
KEY74:
    ETX 4800,74
    GOTO RX_EXIT
KEY75:
    ETX 4800,75
    GOTO RX_EXIT
KEY76:
    ETX 4800,76
    GOTO RX_EXIT
KEY77:
    ETX 4800,77
    GOTO RX_EXIT
KEY78:
    ETX 4800,78
    GOTO RX_EXIT
KEY79:
    ETX 4800,79
    GOTO RX_EXIT
KEY80:
    ETX 4800,80
    GOTO RX_EXIT
KEY81:
    ETX 4800,81
    GOTO RX_EXIT
KEY82:
    ETX 4800,82
    GOTO RX_EXIT
KEY83:
    ETX 4800,83
    GOTO RX_EXIT
KEY84:
    ETX 4800,84
    GOTO RX_EXIT
KEY85:
    ETX 4800,85
    GOTO RX_EXIT
KEY86:
    ETX 4800,86
    GOTO RX_EXIT
KEY87:
    ETX 4800,87
    GOTO RX_EXIT
KEY88:
    ETX 4800,88
    GOTO RX_EXIT
KEY89:
    ETX 4800,89
    GOTO RX_EXIT
KEY90:
    ETX 4800,90
    GOTO RX_EXIT
KEY91:
    ETX 4800,91
    GOTO RX_EXIT
KEY92:
    ETX 4800,92
    GOTO RX_EXIT
KEY93:
    ETX 4800,93
    GOTO RX_EXIT
KEY94:
    ETX 4800,94
    GOTO RX_EXIT
KEY95:
    ETX 4800,95
    GOTO RX_EXIT
KEY96:
    ETX 4800,96
    GOTO RX_EXIT
KEY97:
    ETX 4800,97
    GOTO RX_EXIT
KEY98:
    ETX 4800,98
    GOTO RX_EXIT
KEY99:
    ETX 4800,99
    GOTO RX_EXIT
'*************북마크
'######### ------------------- KEY100-110 전진걸음
KEY100:
    ETX 4800,100
    보행횟수 = 1
    GOTO 전진종종걸음
    GOTO RX_EXIT
KEY101:
    ETX 4800,101
    보행횟수 = 3
    GOTO 전진종종걸음
    GOTO RX_EXIT
KEY102:
    ETX 4800,102
    보행횟수 = 5
    GOTO 전진종종걸음
    GOTO RX_EXIT
KEY103:
    ETX 4800,103
    보행횟수 = 7
    GOTO 전진종종걸음
    GOTO RX_EXIT
KEY104:
    ETX 4800,104
    보행횟수 = 9
    GOTO 전진종종걸음
    GOTO RX_EXIT
'----------------------------------
KEY105:
    ETX 4800,105
    몇걸음 = 1
    GOTO 전진걸음
    GOTO RX_EXIT
KEY106:
    ETX 4800,106
    GOTO RX_EXIT
KEY107:
    ETX 4800,107
    GOTO RX_EXIT
KEY108:
    ETX 4800,108
    GOTO RX_EXIT
KEY109:
    ETX 4800,109
    GOTO RX_EXIT
'######### ------------------- KEY110-119 후진걸음
KEY110:
    ETX 4800,110
    보행횟수 = 1
    GOTO 후진종종걸음
    GOTO RX_EXIT
KEY111:
    ETX 4800,111
    보행횟수 = 3
    GOTO 후진종종걸음
    GOTO RX_EXIT
KEY112:
    ETX 4800,112
    보행횟수 = 5
    GOTO 후진종종걸음
    GOTO RX_EXIT
KEY113:
    ETX 4800,113
    GOTO RX_EXIT
KEY114:
    ETX 4800,114
    GOTO RX_EXIT
KEY115:
    ETX 4800,115
    GOTO RX_EXIT
KEY116:
    ETX 4800,116
    GOTO RX_EXIT
KEY117:
    ETX 4800,117
    GOTO RX_EXIT
'######### ------------------- KEY118-119 옆걸음
KEY118:
    ETX 4800,118
    GOTO 오른쪽옆걸음
    GOTO RX_EXIT
KEY119:
    ETX 4800,119
    GOTO 왼쪽옆걸음
    GOTO RX_EXIT
'######### ------------------- KEY121-150 고개각도
KEY120:
    ETX 4800,120
    GOTO 고개중앙
    GOTO RX_EXIT
KEY121:
    ETX 4800,121
    GOTO 고개상하중앙
    GOTO RX_EXIT
KEY122:
    ETX 4800,122
    GOTO 고개좌우중앙
    GOTO RX_EXIT
KEY123:
    ETX 4800,123
    GOTO RX_EXIT
KEY124:
    ETX 4800,124
    GOTO 고개하향3
    GOTO RX_EXIT
KEY125:
    ETX 4800,125
    GOTO 고개하향6
    GOTO RX_EXIT
KEY126:
    ETX 4800,126
    GOTO 고개하향9
    GOTO RX_EXIT
KEY127:
    ETX 4800,127
    GOTO 하화각이동
    GOTO RX_EXIT
KEY128:
    ETX 4800,128
    GOTO RX_EXIT
KEY129:
    ETX 4800,129
    GOTO 고개상향3
    GOTO RX_EXIT
KEY130:
    ETX 4800,130
    GOTO 고개상향6
    GOTO RX_EXIT
KEY131:
    ETX 4800,131
    GOTO 고개상향9
    GOTO RX_EXIT
KEY132:
    ETX 4800,132
    GOTO 상화각이동
    GOTO RX_EXIT
KEY133:
    ETX 4800,133
    GOTO RX_EXIT
KEY134:
    ETX 4800,134
    GOTO 고개좌향3
    GOTO RX_EXIT
KEY135:
    ETX 4800,135
    GOTO 고개좌향6
    GOTO RX_EXIT
KEY136:
    ETX 4800,136
    GOTO 좌화각이동
    GOTO RX_EXIT
KEY137:
    ETX 4800,137
    GOTO RX_EXIT
KEY138:
    ETX 4800,138
    GOTO 고개우향3
    GOTO RX_EXIT
KEY139:
    ETX 4800,139
    GOTO 고개우향6
    GOTO RX_EXIT
KEY140:
    ETX 4800,140
    GOTO 우화각이동
    GOTO RX_EXIT
KEY141:
    ETX 4800,141
    GOTO RX_EXIT
KEY142:
    ETX 4800,142
    GOTO RX_EXIT
KEY143:
    ETX 4800,143
    GOTO RX_EXIT
KEY144:
    ETX 4800,144
    GOTO RX_EXIT
KEY145:
    ETX 4800,145
    GOTO RX_EXIT
KEY146:
    ETX 4800,146
    GOTO RX_EXIT
KEY147:
    ETX 4800,147
    GOTO RX_EXIT
KEY148:
    ETX 4800,148
    GOTO RX_EXIT
KEY149:
    ETX 4800,149
    GOTO RX_EXIT
KEY150:
    ETX 4800,150
    GOTO RX_EXIT
'######### ------------------- KEY151-160 몸 회전
KEY151:
    ETX 4800,151
    GOTO 오른쪽턴5
    GOTO RX_EXIT
KEY152:
    ETX 4800,152
    GOTO 오른쪽턴10
    GOTO RX_EXIT
KEY153:
    ETX 4800,153
    GOTO 오른쪽턴20
    GOTO RX_EXIT
KEY154:
    ETX 4800,154
    GOTO 오른쪽턴45
    GOTO RX_EXIT
KEY155:
    ETX 4800,155
    GOTO 오른쪽턴60
    GOTO RX_EXIT
KEY156:
    ETX 4800,156
    GOTO 왼쪽턴5
    GOTO RX_EXIT
KEY157:
    ETX 4800,157
    GOTO 왼쪽턴10
    GOTO RX_EXIT
KEY158:
    ETX 4800,158
    GOTO 왼쪽턴20
    GOTO RX_EXIT
KEY159:
    ETX 4800,159
    GOTO 왼쪽턴45
    GOTO RX_EXIT
KEY160:
    ETX 4800,160
    GOTO 왼쪽턴60
    GOTO RX_EXIT
KEY161:
    ETX 4800,161
    GOTO RX_EXIT
KEY162:
    ETX 4800,162
    GOTO RX_EXIT
KEY163:
    ETX 4800,163
    GOTO RX_EXIT
KEY164:
    ETX 4800,164
    GOTO RX_EXIT
KEY165:
    ETX 4800,165
    GOTO RX_EXIT
KEY166:
    ETX 4800,166
    GOTO RX_EXIT
KEY167:
    ETX 4800,167
    GOTO RX_EXIT
KEY168:
    ETX 4800,168
    GOTO RX_EXIT
KEY169:
    ETX 4800,169
    GOTO RX_EXIT
'####### --------------------- KEY170-189 좌우퍼팅
'퍼팅강도들은 임의로 지정했으므로 추후 수정할 것
'#### 우퍼팅(->) --------------
KEY170:
    ETX 4800,170
    GOTO 우퍼팅1  '톡 치기
    GOTO RX_EXIT
KEY171:
    ETX 4800,171
    GOTO 우퍼팅2  '쪼금 더 세게
    GOTO RX_EXIT
KEY172:
    ETX 4800,172
    GOTO 우퍼팅3    '적당히 보다 좀 약하게
    GOTO RX_EXIT
KEY173:
    ETX 4800,173
    GOTO 우퍼팅4   '적당히 치기
    GOTO RX_EXIT
KEY174:
    ETX 4800,174
    GOTO 우퍼팅5      '세게 치기
    GOTO RX_EXIT
'#### 좌퍼팅(<-) --------------
KEY175:
    ETX 4800,175
    GOTO 좌퍼팅1  '톡 치기
    GOTO RX_EXIT
KEY176:
    ETX 4800,176
    GOTO 좌퍼팅2  '쪼금 더 세게
    GOTO RX_EXIT
KEY177:
    ETX 4800,177
    GOTO 좌퍼팅3    '적당히 보다 좀 약하게
    GOTO RX_EXIT
KEY178:
    ETX 4800,178
    GOTO 좌퍼팅4    '적당히 치기
    GOTO RX_EXIT
KEY179:
    ETX 4800,179
    GOTO 좌홀인용톡치기      '세게 치기
    GOTO RX_EXIT
'####### --------------------- KEY180 만세
KEY180:
    ETX 4800,180
    GOTO 만세
    GOTO RX_EXIT

'#---------------------------------------------------------------------------------#
'#                                				                   
'#                                     함수들 작성			                   
'#                                				                   
'#---------------------------------------------------------------------------------#

'-----------------------------------------------------------------------
'				# 퍼팅 함수				
'-----------------------------------------------------------------------

'### ------------------- 우퍼팅 함수 ------------------- ###
우퍼팅1:
    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  130,  10, 10
    WAIT

    MOVE G6C,145,  130,  10, 10
    WAIT

    MOVE G6C,145,  60,  10, 10
    WAIT

    MOVE G6C,135,  40,  30, 10
    WAIT

    MOVE G6C,140,  10,  80, 10
    WAIT

    DELAY 400

    MOVE G6B,100,  35,  90,
    MOVE G6C,140,  10,  70, 10
    WAIT

    '**** 퍼팅강도 ******
    SPEED 1
    MOVE G6C,140,  30,  100, 10
    WAIT
    DELAY 1000
    '******************

    SPEED 8
    MOVE G6C,135,  50,  60, 190
    WAIT

    GOSUB 기본자세
    RETURN
'----------------------------------------
우퍼팅2:
    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  130,  10, 10
    WAIT
    MOVE G6C,145,  130,  10, 10
    WAIT
    MOVE G6C,145,  60,  10, 10
    WAIT
    MOVE G6C,135,  40,  30, 10
    WAIT
    MOVE G6C,140,  10,  80, 10
    WAIT
    DELAY 400
    MOVE G6B,100,  35,  90,
    MOVE G6C,140,  10,  70, 10
    WAIT
    '**** 퍼팅강도 ******
    SPEED 3
    MOVE G6C,140,  30,  100, 10
    WAIT
    DELAY 1000
    '******************
    SPEED 8
    MOVE G6C,135,  50,  60, 190
    WAIT
    GOSUB 기본자세
    RETURN
'----------------------------------------

우퍼팅3:
    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  130,  10, 10
    WAIT
    MOVE G6C,145,  130,  10, 10
    WAIT
    MOVE G6C,145,  60,  10, 10
    WAIT
    MOVE G6C,135,  40,  30, 10
    WAIT
    MOVE G6C,140,  10,  80, 10
    WAIT
    DELAY 400
    MOVE G6B,100,  35,  90,
    MOVE G6C,140,  10,  70, 10
    WAIT
    '**** 퍼팅강도 ******
    SPEED 5
    MOVE G6C,140,  30,  100, 10
    WAIT
    DELAY 1000
    '******************
    SPEED 8
    MOVE G6C,135,  50,  60, 190
    WAIT
    GOSUB 기본자세
    RETURN
'----------------------------------------

우퍼팅4:
    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  130,  10, 10
    WAIT
    MOVE G6C,145,  130,  10, 10
    WAIT
    MOVE G6C,145,  60,  10, 10
    WAIT
    MOVE G6C,135,  40,  30, 10
    WAIT
    MOVE G6C,140,  10,  80, 10
    WAIT
    DELAY 400
    MOVE G6B,100,  35,  90,
    MOVE G6C,140,  10,  70, 10
    WAIT
    '**** 퍼팅강도 ******
    SPEED 7
    MOVE G6C,140,  30,  100, 10
    WAIT
    DELAY 1000
    '******************
    SPEED 8
    MOVE G6C,135,  50,  60, 190
    WAIT
    GOSUB 기본자세
    RETURN
'----------------------------------------

우퍼팅5:
    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,100,  130,  10, 10
    WAIT
    MOVE G6C,145,  130,  10, 10
    WAIT
    MOVE G6C,145,  60,  10, 10
    WAIT
    MOVE G6C,135,  40,  30, 10
    WAIT
    MOVE G6C,140,  10,  80, 10
    WAIT
    DELAY 400
    MOVE G6B,100,  35,  90,
    MOVE G6C,140,  10,  70, 10
    WAIT
    '**** 퍼팅강도 ******
    SPEED 9
    MOVE G6C,140,  30,  100, 10
    WAIT
    DELAY 1000
    '******************
    SPEED 8
    MOVE G6C,135,  50,  60, 190
    WAIT
    GOSUB 기본자세
    RETURN

'### ------------------- 좌퍼팅 함수 ------------------- ###
좌퍼팅1:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT

    DELAY 400

    'MOVE G6C,135,  40,  90, 10
    WAIT

   SPEED 6
        MOVE G6C,135,  10,  80, 10
        WAIT
        DELAY 1000

		SPEED 8
        MOVE G6C,135,  100,  10, 10
        WAIT

        MOVE G6C,135,  50,  60, 190
        WAIT
	

    GOSUB 기본자세
    RETURN
    GOTO RX_EXIT
'----------------------------------------
좌퍼팅2:
   GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT
    DELAY 400
    SPEED 6
        MOVE G6C,135,  10,  70, 25
        WAIT
        DELAY 1000

		SPEED 8
        MOVE G6C,135,  100,  10, 10
        WAIT

        MOVE G6C,135,  50,  60, 190
        WAIT
    GOSUB 기본자세
    RETURN
    GOTO RX_EXIT
'----------------------------------------
좌퍼팅3:
    GOSUB All_motor_mode3
    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT
    DELAY 400
    SPEED 9
        MOVE G6C,135,  10,  60, 25
        WAIT
        DELAY 1000

		SPEED 8
        MOVE G6C,135,  100,  10, 10
        WAIT

        MOVE G6C,135,  50,  60, 190
        WAIT
    
    GOSUB 기본자세
    RETURN
    GOTO RX_EXIT
'----------------------------------------
좌퍼팅4:
    MUSIC "cdg"
    RETURN
    GOTO RX_EXIT
'----------------------------------------
좌홀인용톡치기:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT
    
		SPEED 6
        MOVE G6C,135,  20,  85, 10
        WAIT
        DELAY 1000

		SPEED 8
        MOVE G6C,135,  100,  10, 10
        WAIT

        MOVE G6C,135,  50,  60, 190
        WAIT

        GOSUB 기본자세
    GOTO RX_EXIT
'#### --------------어드레스 및 추후퍼팅 함수 ------------------- ####
DIM 어드레스스위치 AS BYTE
어드레스스위치 = 0

좌어드레스:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  20,  90, 10
    WAIT

    어드레스스위치 = 1
    GOTO RX_EXIT
'----------------------------------------
좌추후퍼팅1:
    IF 어드레스스위치 = 1 THEN
		SPEED 6
        MOVE G6C,135,  10,  80, 10
        WAIT
        DELAY 1000

		SPEED 8
        MOVE G6C,135,  100,  10, 10
        WAIT

        MOVE G6C,135,  50,  60, 190
        WAIT
	
		어드레스스위치=0

        GOSUB 기본자세
    ELSE
		어드레스스위치=0
    ENDIF
    GOTO RX_EXIT
    
좌추후퍼팅2:
    IF 어드레스스위치 = 1 THEN
		SPEED 6
        MOVE G6C,135,  10,  70, 25
        WAIT
        DELAY 1000

		SPEED 8
        MOVE G6C,135,  100,  10, 10
        WAIT

        MOVE G6C,135,  50,  60, 190
        WAIT
	
		어드레스스위치=0

        GOSUB 기본자세
    ELSE
		어드레스스위치=0
    ENDIF
    GOTO RX_EXIT   
    
좌추후퍼팅3:
    IF 어드레스스위치 = 1 THEN
		SPEED 9
        MOVE G6C,135,  10,  60, 25
        WAIT
        DELAY 1000

		SPEED 8
        MOVE G6C,135,  100,  10, 10
        WAIT

        MOVE G6C,135,  50,  60, 190
        WAIT
	
		어드레스스위치=0

        GOSUB 기본자세
    ELSE
		어드레스스위치=0
    ENDIF
    GOTO RX_EXIT  
'--------------------------------------------------------
우어드레스:
    GOSUB All_motor_mode3

    SPEED 8
    MOVE G6A,97,  76, 145,  93, 100, 100
    MOVE G6D,97,  76, 145,  93, 100, 100
    MOVE G6B,100,  35,  90,
    MOVE G6C,150,  100,  10, 10
    WAIT

    MOVE G6C,135,  40,  40, 10
    WAIT

    MOVE G6C,135,  10,  80, 10
    WAIT

    어드레스스위치 = 1
    GOTO RX_EXIT
'----------------------------------------
우추후퍼팅:
    IF 어드레스스위치 = 1 THEN
		SPEED 6
    	MOVE G6C,140,  30,  100, 10
    	WAIT
   		DELAY 1000

		SPEED 8

        MOVE G6C,135,  50,  60, 190
       	WAIT
	
		어드레스스위치=0

        GOSUB 기본자세
    ELSE
		어드레스스위치=0
    ENDIF
    GOTO RX_EXIT
'-----------------------------------------------------------------------
'				# 걸음 함수				
'-----------------------------------------------------------------------
'몇 걸음 걸을 지에 대한 변수 생성하여 걸음 카운트 함
'걷기 스텝: 오른쪽으로 기울기 -> 왼발 들기 -> 왼발 뻗고 착지 -> 왼발 중심 이동 -> 오른발 들기 -> 오른발 뻗고 착지

'#########  ------------------------------ 전진/후진종종걸음 #############
전진종종걸음:
    GOSUB All_motor_mode3
    보행COUNT = 0
    SPEED 7
    HIGHSPEED SETON

    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 147,  93, 101
        MOVE G6D,101,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 전진종종걸음_1
    ELSE
        보행순서 = 0
        MOVE G6D,95,  76, 147,  93, 101
        MOVE G6A,101,  76, 147,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 전진종종걸음_4
    ENDIF

전진종종걸음_1:
    MOVE G6A,95,  90, 125, 100, 104
    MOVE G6D,104,  77, 147,  93,  102
    MOVE G6B, 85
    MOVE G6C,115
    WAIT

전진종종걸음_2:
    MOVE G6A,103,   73, 140, 103,  100
    MOVE G6D, 95,  85, 147,  85, 102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0

        GOTO RX_EXIT
    ENDIF

    보행COUNT = 보행COUNT + 1
    IF 보행COUNT > 보행횟수 THEN  GOTO 전진종종걸음_2_stop

    ERX 4800,A,전진종종걸음_4
    IF A <> A_old THEN
전진종종걸음_2_stop:
        MOVE G6D,95,  90, 125, 95, 104
        MOVE G6A,104,  76, 145,  91,  102
        MOVE G6C, 100
        MOVE G6B,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        GOTO RX_EXIT
    ENDIF

전진종종걸음_4:
    MOVE G6D,95,  95, 120, 100, 104
    MOVE G6A,104,  77, 147,  93,  102
    MOVE G6C, 85
    MOVE G6B,115
    WAIT

전진종종걸음_5:
    MOVE G6D,103,    73, 140, 103,  100
    MOVE G6A, 95,  85, 147,  85, 102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    보행COUNT = 보행COUNT + 1
    IF 보행COUNT > 보행횟수 THEN  GOTO 전진종종걸음_5_stop

    ERX 4800,A,전진종종걸음_1
    IF A <> A_old THEN

전진종종걸음_5_stop:
        MOVE G6A,95,  90, 125, 95, 104
        MOVE G6D,104,  76, 145,  91,  102
        MOVE G6B, 100
        MOVE G6C,100
        WAIT
        HIGHSPEED SETOFF
        SPEED 15
        GOSUB 안정화자세
        SPEED 5
        GOSUB 기본자세2

        GOTO RX_EXIT
    ENDIF
    GOTO 전진종종걸음_1

후진종종걸음:
    GOSUB All_motor_mode3
    넘어진확인 = 0
    보행COUNT = 0
    SPEED 7
    HIGHSPEED SETON

    IF 보행순서 = 0 THEN
        보행순서 = 1
        MOVE G6A,95,  76, 145,  93, 101
        MOVE G6D,101,  76, 145,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 후진종종걸음_1
    ELSE
        보행순서 = 0
        MOVE G6D,95,  76, 145,  93, 101
        MOVE G6A,101,  76, 145,  93, 98
        MOVE G6B,100
        MOVE G6C,100
        WAIT

        GOTO 후진종종걸음_4
    ENDIF

후진종종걸음_1:
    MOVE G6D,104,  76, 147,  93,  102
    MOVE G6A,95,  95, 120, 95, 104
    MOVE G6B,115
    MOVE G6C,85
    WAIT

후진종종걸음_2:
    MOVE G6A, 103,  79, 147,  89, 100
    MOVE G6D,95,   65, 147, 103,  102
    WAIT

    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF
    보행COUNT = 보행COUNT + 1
    IF 보행COUNT > 보행횟수 THEN  GOTO 후진종종걸음_2_stop

    ERX 4800,A, 후진종종걸음_4
    IF A <> A_old THEN

후진종종걸음_2_stop:
        MOVE G6D,95,  85, 130, 100, 104
        MOVE G6A,104,  77, 146,  93,  102
        MOVE G6C, 100
        MOVE G6B,100
        WAIT

        'SPEED 15
        GOSUB 안정화자세
        HIGHSPEED SETOFF
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

후진종종걸음_4:
    MOVE G6A,104,  76, 147,  93,  102
    MOVE G6D,95,  95, 120, 95, 104
    MOVE G6C,115
    MOVE G6B,85
    WAIT

후진종종걸음_5:
    MOVE G6D, 103,  79, 147,  89, 100
    MOVE G6A,95,   65, 147, 103,  102
    WAIT
    GOSUB 앞뒤기울기측정
    IF 넘어진확인 = 1 THEN
        넘어진확인 = 0
        GOTO RX_EXIT
    ENDIF

    보행COUNT = 보행COUNT + 1
    IF 보행COUNT > 보행횟수 THEN  GOTO 후진종종걸음_5_stop

    ERX 4800,A, 후진종종걸음_1
    IF A <> A_old THEN 

후진종종걸음_5_stop:
        MOVE G6A,95,  85, 130, 100, 104
        MOVE G6D,104,  77, 146,  93,  102
        MOVE G6B, 100
        MOVE G6C,100
        WAIT

        'SPEED 15
        GOSUB 안정화자세
        HIGHSPEED SETOFF
        SPEED 5
        GOSUB 기본자세2

        'DELAY 400
        GOTO RX_EXIT
    ENDIF

    GOTO 후진종종걸음_1

'------------------------
전진걸음: '종종걸음 아닌 것
    보행COUNT = 0
    보행속도 = 13
    좌우속도 = 4
    넘어진확인 = 0

    GOSUB Leg_motor_mode3

    IF 몇걸음 <> 1 THEN
        FOR i=1 TO 몇걸음
            SPEED 4 '오른쪽기울기
            MOVE G6A, 88,  74, 144,  95, 110
            MOVE G6D,108,  76, 146,  93,  96
            MOVE G6B,100
            MOVE G6C,100
            WAIT

            SPEED 10 '왼발들기
            MOVE G6A, 90, 90, 120, 105, 110,100
            MOVE G6D,110,  76, 147,  93,  96,100
            MOVE G6B,90
            MOVE G6C,110
            WAIT

            SPEED 보행속도 '왼발뻗어착지
            MOVE G6A, 86,  56, 145, 115, 110
            MOVE G6D,108,  76, 147,  93,  96
            WAIT

            SPEED 좌우속도 '왼발중심이동
            GOSUB Leg_motor_mode3
            MOVE G6A,110,  76, 147, 93,  96
            MOVE G6D,86, 100, 145,  69, 110
            WAIT

            SPEED 보행속도 '오른발들기
            MOVE G6A,110,  76, 147,  93, 96,100
            MOVE G6D,90, 90, 120, 105, 110,100
            MOVE G6B,110
            MOVE G6C,90
            WAIT

            SPEED 보행속도 '오른발뻗어착지
            MOVE G6D, 86,  56, 145, 115, 110
            MOVE G6A,108,  76, 147,  93,  96
            WAIT

	NEXT i
    ELSE
	SPEED 4 '오른쪽기울기
	MOVE G6A, 88,  74, 144,  95, 110
	MOVE G6D,108,  76, 146,  93,  96
	MOVE G6B,100
	MOVE G6C,100
	WAIT

	SPEED 10 '왼발들기
	MOVE G6A, 90, 90, 120, 105, 110,100
	MOVE G6D,110,  76, 147,  93,  96,100
	MOVE G6B,90
	MOVE G6C,110
	WAIT

        SPEED 보행속도 '왼발뻗어착지
        MOVE G6A, 86,  56, 145, 115, 110
        MOVE G6D,108,  76, 147,  93,  96
        WAIT

        SPEED 좌우속도 '왼발중심이동
        GOSUB Leg_motor_mode3
        MOVE G6A,110,  76, 147, 93,  96
        MOVE G6D,86, 100, 145,  69, 110
        WAIT

        SPEED 보행속도 '오른발들기
        MOVE G6A,110,  76, 147,  93, 96,100
	MOVE G6D,90, 90, 120, 105, 110,100
	MOVE G6B,110
	MOVE G6C,90
	WAIT

	SPEED 보행속도 '오른발뻗어착지
	MOVE G6D, 86,  56, 145, 115, 110
	MOVE G6A,108,  76, 147,  93,  96
	WAIT
	ENDIF
    GOTO RX_EXIT

'############ ------------------------------ 옆걸음 ###############

오른쪽옆걸음:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6D, 95,  90, 125, 100, 107, 100
    MOVE G6A,107,  77, 147,  93, 107 , 100
    WAIT

    SPEED 12
    MOVE G6D, 102,  77, 147, 93, 100, 100
    MOVE G6A,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6D,95,  76, 147,  93, 98, 100
    MOVE G6A,95,  76, 147,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT

왼쪽옆걸음: 
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 12
    MOVE G6A, 95,  90, 125, 100, 104, 100
    MOVE G6D,105,  76, 146,  93, 104, 100
    WAIT

    SPEED 12
    MOVE G6A, 102,  76, 146, 93, 100, 100
    MOVE G6D,90,  80, 140,  95, 107, 100
    WAIT

    SPEED 12
    MOVE G6A,95,  76, 146,  93, 98, 100
    MOVE G6D,95,  76, 146,  93, 98, 100
    WAIT

    SPEED 3
    GOSUB 기본자세2

    GOTO RX_EXIT
'-----------------------------------------------------------------------
'				# 고개 함수				
'-----------------------------------------------------------------------
'DIM 좌우각 AS BYTE
'DIM 상하각 AS BYTE
'좌우각 = 0
'상하각 = 0

'좌우영점 = 100, 상하영점=113
'머리좌우 = 100, 머리상하=113
'# ----------------- 중앙 맞추기 ------------------- #
고개중앙:
   SPEED 3
   머리상하 = 상하영점
   머리좌우 = 좌우영점
   SERVO 11,머리좌우
   SERVO 16,머리상하
   GOTO RX_EXIT

고개상하중앙:
   SPEED 3
   머리상하 = 상하영점
   SERVO 16,머리상하
   GOTO RX_EXIT

고개좌우중앙:
   SPEED 3
   머리좌우 = 좌우영점
   SERVO 11,머리좌우
   GOTO RX_EXIT

'# -------------------- 고개 이동 ----------------------- #
고개하향3:
   SPEED 3
   머리상하 = 머리상하 - 3
   SERVO 16, 머리상하
   GOTO RX_EXIT

고개하향6:
   SPEED 3
   머리상하 = 머리상하 - 6
   SERVO 16, 머리상하
   GOTO RX_EXIT

고개하향9:
   SPEED 3
   머리상하 = 머리상하 - 9
   SERVO 16, 머리상하
   GOTO RX_EXIT

하화각이동:
   SPEED 3
   머리상하 = 머리상하 - 30
   SERVO 16, 머리상하
   GOTO RX_EXIT
'------------------------
고개상향3:
   SPEED 3
   머리상하= 머리상하 + 3
   SERVO 16, 머리상하
   GOTO RX_EXIT

고개상향6:
   SPEED 3
   머리상하= 머리상하 + 6
   SERVO 16, 머리상하
   GOTO RX_EXIT

고개상향9:
   SPEED 3
   머리상하= 머리상하 + 9
   SERVO 16, 머리상하
   GOTO RX_EXIT

상화각이동:
   SPEED 3
   머리상하 = 머리상하 + 30
   SERVO 16, 머리상하
   GOTO RX_EXIT
'--------------------
고개좌향3:
   SPEED 3
   머리좌우= 머리좌우 - 3
   SERVO 11, 머리좌우
   GOTO RX_EXIT

고개좌향6:
   SPEED 3
   머리좌우= 머리좌우 - 6
   SERVO 11, 머리좌우
   GOTO RX_EXIT

좌화각이동:
   SPEED 3
   머리좌우= 머리좌우 - 30
   SERVO 11, 머리좌우
   GOTO RX_EXIT
'-----------------------
고개우향3:
   SPEED 3
   머리좌우= 머리좌우 + 3
   SERVO 11, 머리좌우
   GOTO RX_EXIT

고개우향6:
   SPEED 3
   머리좌우= 머리좌우 + 6
   SERVO 11, 머리좌우
   GOTO RX_EXIT

우화각이동:
   SPEED 3
   머리좌우= 머리좌우 + 30
   SERVO 11, 머리좌우
   GOTO RX_EXIT

'-----------------------------------------------------------------------
'				# 턴 함수				
'-----------------------------------------------------------------------
왼쪽턴5:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,100,  81, 145,  88, 106, 100
    MOVE G6D,94,  71, 145, 98, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,97,  81, 145,  88, 104, 100
    MOVE G6D,91,  71, 145, 98, 96, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    GOTO RX_EXIT

왼쪽턴10:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,100,  86, 145,  83, 106, 100
    MOVE G6D,94,  66, 145, 103, 100, 100
    WAIT

    SPEED 12
    MOVE G6A,97,  86, 145,  83, 104, 100
    MOVE G6D,91,  66, 145, 103, 96, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2
    GOTO RX_EXIT

왼쪽턴20:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 8
    MOVE G6A,95,  96, 145,  73, 108, 100
    MOVE G6D,91,  56, 145,  113, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  96, 145,  73, 108, 100
    MOVE G6D,88,  56, 145,  113, 102, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT

왼쪽턴45:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 10
    MOVE G6A,95,  106, 145,  63, 108, 100
    MOVE G6D,91,  46, 145,  123, 102, 100
    WAIT

    SPEED 12
    MOVE G6A,91,  106, 145,  63, 108, 100
    MOVE G6D,88,  46, 145,  123, 102, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2
    
    GOTO RX_EXIT

왼쪽턴60:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 15
    MOVE G6A,95,  116, 145,  53, 108, 100
    MOVE G6D,91,  36, 145,  133, 102, 100
    WAIT

    SPEED 15
    MOVE G6A,91,  116, 145,  53, 108, 100
    MOVE G6D,88,  36, 145,  133, 102, 100
    WAIT

    SPEED 10
    GOSUB 기본자세2

    GOTO RX_EXIT
오른쪽턴5:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,97,  71, 145,  98, 103, 100
    MOVE G6D,97,  81, 145,  88, 103, 100
    WAIT

    SPEED 12
    MOVE G6A,94,  71, 145,  98, 101, 100
    MOVE G6D,94,  81, 145,  88, 101, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT
오른쪽턴10:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 5
    MOVE G6A,97,  66, 145,  103, 103, 100
    MOVE G6D,97,  86, 145,  83, 103, 100
    WAIT

    SPEED 12
    MOVE G6A,94,  66, 145,  103, 101, 100
    MOVE G6D,94,  86, 145,  83, 101, 100
    WAIT
    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100
    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT

오른쪽턴20:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2
    SPEED 8
    MOVE G6A,95,  56, 145,  113, 105, 100
    MOVE G6D,95,  96, 145,  73, 105, 100
    WAIT

    SPEED 12
    MOVE G6A,93,  56, 145,  113, 105, 100
    MOVE G6D,93,  96, 145,  73, 105, 100
    WAIT

    SPEED 6
    MOVE G6A,101,  76, 146,  93, 98, 100
    MOVE G6D,101,  76, 146,  93, 98, 100

    WAIT

    GOSUB 기본자세2

    GOTO RX_EXIT

오른쪽턴45:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 10
    MOVE G6A,95,  46, 145,  123, 105, 100
    MOVE G6D,95,  106, 145,  63, 105, 100
    WAIT

    SPEED 12
    MOVE G6A,93,  46, 145,  123, 105, 100
    MOVE G6D,93,  106, 145,  63, 105, 100
    WAIT

    SPEED 8
    GOSUB 기본자세2

    GOTO RX_EXIT

오른쪽턴60:
    MOTORMODE G6A,3,3,3,3,2
    MOTORMODE G6D,3,3,3,3,2

    SPEED 15
    MOVE G6A,95,  36, 145,  133, 105, 100
    MOVE G6D,95,  116, 145,  53, 105, 100
    WAIT

    SPEED 15
    MOVE G6A,90,  36, 145,  133, 105, 100
    MOVE G6D,90,  116, 145,  53, 105, 100
    WAIT

    SPEED 10
    GOSUB 기본자세2

    GOTO RX_EXIT
'-----------------------------------------------------------------------
'				# 세리머니				
'-----------------------------------------------------------------------
만세:
    GOSUB 기본자세
    GOSUB Arm_motor_mode3
    GOSUB Leg_motor_mode2
    SPEED 15
    MOVE G6A,100,  76, 145,  93, 100
    MOVE G6D,100,  76, 145,  93, 100
    MOVE G6B,100,  180,  120
    'MOVE G6C,100,  180,  120
    WAIT	'

    SPEED 10
    FOR i = 1 TO 3'

        MOVE G6B,100,  145,  100
        'MOVE G6C,100,  145,  100
        WAIT

        MOVE G6B,100,  180,  130
        'MOVE G6C,100,  180,  130
        WAIT	
    NEXT i
    DELAY 200
    SPEED 8
    GOSUB 기본자세
    GOSUB All_motor_Reset
    GOTO RX_EXIT
    

공치기자세:
    GOSUB 기본자세
    GOSUB All_motor_Reset
    GOTO RX_EXIT
	