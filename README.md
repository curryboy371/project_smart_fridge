# 스마트 냉장고

### 참고링크
[유튜브](https://www.youtube.com/watch?v=PBkATeySTUc&feature=youtu.be), [협업문서](https://woaixian.notion.site/Project-TF-Team-Fridge-1ff2ba1914db8067858bd4f6338669a0)



## 1. 프로젝트 필요성 및 목적
1. 내부의 초음파 센서를 통해 식재료의 양을 실시간으로 확인할 수 있어, 문을 열어보지 않고도 신선도와 재고를 파악할 수 있다.
2. 사용자에게 유통기한 임박 등을 안내하며, 웹을 통해 이를 편리하게 모니터링할 수 있다.
3. 사용자 정보 및 냉장고 식품을 관리하여 사용자 맞춤형 레시피를 제공할 수 있고, 입출고 로그를 확장하면 음식 소비 패턴을 파악하여 시각화 및 예측이 가능하다.

## 2. 주요 기능
### **자동문 제어**

- STM32 기반 초음파 센서와 서보 모터를 이용해
- 냉장고 문을 자동으로 열고 닫음
- 양손에 물건을 들고 있을 때 매우 편리

### **식재료 인식**

- 라즈베리파이와 웹캠을 활용
- 냉장고 속 음식(식재료)을 인식하여
- 정확한 재고 파악 가능

### **데이터화 및 관리**

- 인식된 식재료 + 사용자 건강 데이터를 통합 관리
- FIFO(선입선출) 방식으로 관리해 음식물 낭비 감소

### **스마트 시스템**

- 유통기한 기반 레시피와 맞춤형 식단 추천
- 사용자 알레르기 및 선호도 고려해 식생활 제안




## 2. 시스템 구성 및 외관
1. 시스템 구성
<img width="1397" height="665" alt="image" src="https://github.com/user-attachments/assets/aad906f1-3501-4a49-a5f2-6d48115b4c2c" />

2. 외관
<img width="1228" height="815" alt="image" src="https://github.com/user-attachments/assets/97c7e24a-c5e2-4016-92f6-9a6182b27fb2" />


### 사용 부품
- Control Board : STM32 NUCLEO-F411RE ( C )
- Detect Board : Raspberry Pi 4
- Camera : Logitech 4K Webcam
- Device **:** Ultrasonic HC-SR04, Servo Motor SG90

### 사용 기술
- Web frontend : Appsmith ( Nocode Web Service + JavaScript )
- Web backend : FastAPI ( Python )
- DB : MongoDB
- LLM : GPT-API
- Computer Vision : OpenCV, Yolo5


## 3. 통신 플로우

1. 객체 인식 Flow
<img width="2083" height="764" alt="image" src="https://github.com/user-attachments/assets/fc74fd69-a76c-4ae9-aca2-cf49bfc82514" />

2. 유저 레시피 요청 Flow
<img width="1980" height="685" alt="image" src="https://github.com/user-attachments/assets/4e7ccc6f-0734-4997-b9a2-3b041a77a35f" />


## 4. 상세 수행 내용

### 1) STM32 (초음파, 서보모터 제어)
초음파 모듈(HC-SR04)에 Trigger 신호를 보내 Echo를 수신하여 거리(cm) 측정
일정 거리 이하에서 물체(손, 물건)를 인식하면 PWM 신호로 서보모터를 구동해 냉장고 문 자동 개방
이후 지속적으로 초음파로 거리를 확인하여, 물체가 사라진 경우 일정 시간 대기 후
UART를 통해 Raspberry Pi로 상태(문 개폐, 물체 감지 등) 시그널을 전송
PWM 제어를 통해 서보모터를 작동시켜 냉장고 문을 자동으로 닫음

### 2) Raspberry Pi 4 (카메라, 객체 인식)
(1) 기본 모드
카메라를 통해 실시간 영상을 지속적으로 촬영
Python thread를 활용해 STM32로부터 UART 신호를 비동기로 수신

(2) 객체 인식 트리거
STM32에서 특정 신호를 수신하면 즉시 현재 프레임을 캡처
YOLOv5 기반 객체 탐지를 비동기로 수행하여 탐지 결과 생성

(3) 데이터 생성 및 전송
탐지된 객체들의 중심 좌표를 계산해 위치 정보를 생성
인식된 객체의 ROI 및 위치 정보를 기반으로 냉장고 내부 음식 배치 이미지 생성
탐지 결과(위치, 클래스명, ROI 이미지 등)와 배치 이미지를 JSON 및 이미지 파일 형태로 Web Server에 HTTP POST 방식으로 전송

### 3) Web Server (FastAPI + MongoDB + GPT 연동)
(1) 객체 인식 데이터 처리
Raspberry Pi로부터 전달받은 객체 인식 JSON 및 배치 이미지를 수신
동일 위치에 동일 음식이 존재 → 재고 유지
위치에서 음식이 사라진 경우 → 소비 처리
소비된 음식 중 유통기한이 지난 경우 → 폐기 처리

(2) 사용자 맞춤 레시피 추천
유저 데이터 (사용자 알러지, 선호 음식 등), 현재 보관 중인 음식 데이터를 GPT API에 전달
GPT API를 통해 개인화된 레시피 추천 결과를 반환, 웹 UI에 표시

(3) 신규 음식 입고 처리
현재 시각을 입고 날짜로 저장
음식 카테고리 테이블에서 권장 유통기한을 조회 후 자동으로 유통기한 설정

(4) 음식 입출고 이력 관리
음식의 입고, 출고, 폐기 등 모든 상태 변화를 로그 테이블에 저장
추후 통계 분석 및 머신러닝 데이터셋으로 활용할 수 있도록 데이터 축적



## 5. 문제점 및 개선사항

1. 서보모터 구동력 부족
초기에는 서보모터 한 개로 냉장고 문을 열도록 설계했으나, 개폐 시 모터의 토크가 부족하여 원활한 작동이 어려움
→ 서보모터를 두 개로 증설하여 보다 안정적인 문 개폐 동작을 확보

2. 유통기한 텍스트 인식 한계
원래는 이미지에서 텍스트(OCR)를 인식해 유통기한을 자동으로 등록하려 했으나,
작은 글씨 크기 및 해상도 문제로 OCR 인식률이 낮아 실효성이 떨어짐
→ 카테고리 테이블(예: 과일, 돼지고기, 견과류 등)을 미리 구성하고,
인식된 음식 이름을 기반으로 적합한 카테고리를 찾아 권장 유통기한을 자동 설정하도록 수정

3. 카테고리 테이블 입력의 작업 효율
DB에 음식 카테고리 및 권장 유통기한 데이터를 웹 사이트에서 수동 입력하려니 작업량이 과도함
→ CSV 파일로 관리 후 Python 및 배치 스크립트를 통해 MongoDB에 자동 업로드하도록 구현하여
초기 데이터 세팅 및 수정 시 작업 시간을 대폭 절감
