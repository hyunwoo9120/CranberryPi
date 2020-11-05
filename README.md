# CranberryPi, girls in ICT
### 인원수에 기반한 냉난방 제어 시스템
#### Heating and cooling control system based on number of people

<p>
IR receiver와 IR transmitter로 냉난방 기기 조절<br>
PIGPIO IR Record and Playback http://abyz.me.uk/rpi/pigpio/examples.html<br>
Adafruit_DHT 현재 실내 온도 읽기<br>
</p>

<p>
https://www.notion.so/3-b8d38e58e18f49e8b357528154f91ec3<br>
1. people의 number_upload.py을 통해서 사진을 캡처 후 S3로 전송한다.<br>
2. number_extraction.py를 Lambda에서 실행한다.<br>
3. s3의 이미지를 트리거 받아 사람 수를 추출한다.<br>
</p>

<p>
실내 온도와 사람 수에 따른 냉난방 control 시스템을 설계
실내 온도와 사람 수를 추출하는 위 과정의 프로세스를 하나의 전체 프로세스로 병합
</p>
