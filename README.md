# 제 21회 임베디드 소프트웨어 경진대회
![IMG_6354_Original](https://github.com/user-attachments/assets/38cdf79b-06c3-4e58-9bc8-3a93783b35c3)

## 결선시연동영상 : [[team ROKO]](https://youtu.be/G8WIHnUlc4U?feature=shared)  

## 목차
[0. 팀 구성원 및 역할](#0.-팀-구성원-및-역할)  
[1. 개발 동기 및 목표](#1.-개발-동기-및-목표)  
[2. 개발 방향 및 전략](#2.-개발-방향-및-전략)  
[3. 개발의 차별성](#3.-개발의-차별성)  

---  
## 0. 팀 구성원 및 역할
### CV 및 알고리즘 파트 
| 이름 | 역할 |
| --- | --- |
| 강서영 | 영상 처리, 알고리즘 구현, 로봇 테스트 |
| 김민주 | 영상 처리, 알고리즘 구현, 로봇 테스트, 홀인 알고리즘 설계 |
| 남궁희 | 영상 처리, 알고리즘 구현, 로봇 테스트 |

### 로봇 제어 파트
| 이름 | 역할 |
| --- | --- |
| 최건웅 | 로봇 제어, 거리 검출 알고리즘 설계 및 테스트 |
| 한이연 | 로봇 제어 및 영점 조정, 모션 설계 및 테스트 |
<br>
    
## 1. 개발 동기 및 목표
로봇산업의 발전에 따라 로봇의 활동 범위가 늘어나는 과정 속에 휴머노이드 골프 로봇은 사람들에게 새로운 콘텐츠와 재미를 제공하고, 로봇이 엔터테인먼트 분야의 발전에도 기여함을 보여준다.
- 로봇에 센서를 통한 시각적인 인식 능력을 부여하여 사물, 이미지 및 비디오 분석을 가능하게 한다. 센싱 데이터를 open CV를 활용하여 가공하고, 골프 로봇을 개발하는 과정에서 컴퓨터 비전 분야에 중요한 영상 처리 과정 전반에 대한 내용을 익힌다. 
- 게임을 진행함에 있어 로봇은 다양한 상황속에서 최적의 동작을 수행해야 한다. 이를 위해서 입력받은 다양한 데이터에서 유의미한 정보를 추출하고, 높은 정확도와 성능을 수행하도록 하는 알고리즘을 설계하여 로봇의 동작을 자동화하도록 한다. 
- 인간과 유사한 동작으로 정교한 동작과 정확한 타격을 할 수 있는 골프 로봇의 개발은 휴머노이드의 운동 능력과 협조 능력을 개선한다.

<br>
  
## 2. 개발 방향 및 전략

### a. 개발 환경
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Raspberry Pi](https://img.shields.io/badge/-RaspberryPi-C51A4A?style=for-the-badge&logo=Raspberry-Pi) <br>
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white) <br>
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
 <br>

### b. 클래스 다이어그램
![roko_a2](https://github.com/user-attachments/assets/65ae742f-f658-4b32-a325-2087e0c17416) ![roko_a3](https://github.com/user-attachments/assets/3ac20f5f-0512-4d8f-af78-9c18d33f4f59)
![roko_a](https://github.com/user-attachments/assets/f1ff2404-7c2c-4f73-a784-2ef323e9c3de)


### c. 순서도
![b0](https://github.com/user-attachments/assets/0ba9b2f0-04b5-4b93-86e5-a3926f07da0c) 
![b1](https://github.com/user-attachments/assets/d9482966-4e82-49cf-9fcc-74cb3240a326) ![b2](https://github.com/user-attachments/assets/9ddcd617-182d-4b8b-abfd-710e56df8432)
![b3](https://github.com/user-attachments/assets/79134dac-21e5-4445-ac2e-a73aa808f878) ![b4](https://github.com/user-attachments/assets/e1e26890-ee72-4cc8-b77a-33f01d6da5b7)
<br>
1. Controller : 골프경기의 전반적인 알고리즘을 담고 있는 클래스
2. ImageProcessor : 영상처리 및 분석 클래스
3. Motion : 로봇의 모션을 담당하는 클래스
4. Head : 로봇의 고개 각을 조절하는 클래스
5. Robo : 로봇 제어에서 동작과 이미지 처리 관련 기능을 초기화 하고 관리하는 클래스
6. Distance : 서보 각도에 관련된 전역 변수를 정의하고 거리값을 저장하는 클래스
<br>

### d. 로봇 작동알고리즘
<br>
 
 
## 3. 개발의 차별성 
1. 거리 검출  
2. 물체 인식을 위한 동작을 최소화하는 알고리즘  
![udlr](https://github.com/user-attachments/assets/d611410a-e2d5-45af-9769-cee7fa8597d0)  
3. 홀인 알고리즘  
4. 각 단계 모듈화 및 고유 역할 부여  
![roko_a3](https://github.com/user-attachments/assets/3ac20f5f-0512-4d8f-af78-9c18d33f4f59)  

<br>

