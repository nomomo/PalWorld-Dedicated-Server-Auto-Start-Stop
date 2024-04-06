<div align="center">

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/nomomo/PalWorld-Dedicated-Server-Auto-Start-Stop/blob/main/README.md) (Translated by ChatGPT)

</div>

# PalWorld-Dedicated-Server-Auto-Start-Stop

- 이것은 PalWorld Windows 서버를 자동으로 켜고 끄기 위한 간단한 파이썬 스크립트 입니다.
- PalWorld 서버가 구동 중이지 않을 때, 유저가 접속을 시도하면 자동으로 서버를 켭니다.
- PalWorld 서버가 구동 중일 때, 온라인인 유저가 없으면 일정 시간 후 서버를 자동으로 끕니다.
- Webserver 을 통해 서버를 On-Off 할 수 있는 Admin Page 를 제공합니다.

## 한계

- 이 툴은 개인적인 사용을 위해 만든 스크립트로 현재 개발 중입니다. 생각나는대로 코딩하여 코드가 클린하지 않고 많은 버그가 있습니다.
- Windows 환경만을 지원합니다.
- 소규모 서버에서만 테스트 되었습니다.
- 알 수 없는 보안 문제가 발생할 수도 있으니 주의하십시오.

## 어떻게 사용합니까?

만약 테스트 해보고 싶다면 아래의 방법을 따르십시오. 2024년 1월 28일 PalWorld v0.1.3.0 기준으로 정상 동작합니다.

### 사전 준비

RCON 사용을 위해 `PalWorldSettings.ini` 파일에서 `RCONEnabled=True` 로 설정하십시오.

이 파일은 서버를 최초 1회 실행하면 생성되며 기본 경로는 `{PalServerPath}\PalServer\Pal\Saved\Config\WindowsServer\PalWorldSettings.ini` 입니다. 만약 해당 파일에 아무런 내용도 없는 경우 `{PalServerPath}\PalServer\DefaultPalWorldSettings.ini` 파일의 내용을 `PalWorldSettings.ini` 파일에 붙여넣기 하십시오.

### 내려받기

본 리포지토리에서 Download ZIP 기능을 이용하여 코드를 내려받거나, 다음의 명령어를 실행하십시오.

```bash
git clone https://github.com/nomomo/PalWorld-Dedicated-Server-Auto-Start-Stop.git
```

### Install Dependencies

본 스크립트는 Python 3.10 버전에서 테스트 되었습니다.

관련된 패키지 설치를 위하여 커맨드 창에서 다음을 실행합니다.

```bash
pip install flask psutil schedule git+https://github.com/ttk1/py-rcon.git
```

### setting.py 파일 수정

서버 설정에 맞게 `src\settings.json` 파일을 수정합니다.

`palworldExePath` 에는 `{PalServerPath}\PalServer\PalServer.exe` 의 경로를 입력하십시오.

```json
{
    // PalWorld
    "palworldExePath": "C:\\steamcmd\\steamapps\\common\\PalServer\\PalServer.exe", //PalWorld Server exe file
    "palworldServerIP": "0.0.0.0",          // PalWorld Server IP. This is used for "Auto Start". Use "0.0.0.0" to open to all. use "localhost"
    "palworldServerPort": 8211,             // PalWorld Server PublicPort in PalWorldSettings.ini. This is used for "Auto Start".
    "palworldRCONHost": "localhost",        // RCON host. use "0.0.0.0" to open to all. use "localhost".
    "palworldRCONPort": 25575,              // RCONPort in PalWorldSettings.ini. Default is 25575
    "palworldAdminPassword": "topSecretPassword",   // AdminPassword in PalWorldSettings.ini

    // Web Server
    "useWebServer": true,                   // Use simple admin page
    "webServerHost": "localhost",           // webserver hostname. use "0.0.0.0" to open to all. use "localhost"
    "webServerPort": 8212,                  // webserver port
    "showAction": true,                     // show action area
    "showServerOnBtn": true,                // show "Server On" button
    "showServerOffBtn": true,               // show "Server Off" button
    "showUpdateServerStatusBtn": true,      // show "Update Server Status" button
    "showServerIPAddress": true,            // show IP Address

    // Auto Start
    "useAutoStart": true,                   // when user try to access, start the server automatically

    // Auto Stop
    "useAutoStop": true,                    // if True && there is are no players online, server will automatically stop
    "ServerAutoStopSeconds": 600.0,         // the server will automatically stop after ServerAutoStopSeconds seconds.
    "ServerAutoStopCheckInterval": 10.0,    // AutoStop event is checked every ServerAutoStopCheckInterval seconds.
    "palworldMainProcessName": "PalServer-Win64-Shipping-Cmd.exe"    // don't change, if there is no problem
}
```

### Run main.py

커맨드 창에서 `src` 폴더 경로로 이동한 후, 다음을 실행합니다.

```bash
python main.py
```

콘솔 창이 자동으로 켜지고 로그가 출력됩니다. 로그는 app.log 파일에 기록됩니다.

설정에서 `"useWebServer": True`인 경우, Admin Page가 잘 접속되는지 확인하십시오. 기본값의 경우 `http://localhost:8212/` 입니다.

<img src="https://github.com/nomomo/PalWorld-Dedicated-Server-Auto-Start-Stop/blob/main/images/AdminPageSample.png?raw=true" width="300px">

## Known Issue

- 유저의 닉네임에 유니코드 문자가 포함되면 RCON Commands 에서 ShowPlayers 명령이 동작하지 않습니다. 이 오류는 수신된 읽어야 하는 문자 개수와 실제 수신된 문자의 개수가 달라 발생합니다.
- 해결 방법: 설치된 py-rcon 패키지와 함께 설치된 connection.py 파일을 열고 _read 함수의 내용을 다음과 같이 수정합니다.

```Python
def _read(self, length):
    packet_data = self.sock.recv(length)
    if len(packet_data) < length:
        #raise Exception('Received few bytes!') # disable raise exception
        return packet_data
    return packet_data
```

## 동작 원리

### 서버 자동 시작

1. PalWorld 서버가 구동 중이지 않으면 8211 포트를 열어 패킷을 수신합니다.
1. `\x09\x08\x00` 으로 시작하는 패킷이 수신되길 기다립니다.
1. 패킷이 수신되면 8211 포트를 닫고, `palworldExePath` 경로에 위치한 파일을 실행하여 서버를 시작합니다.

### 서버 자동 정지

1. RCON을 통해 현재 서버에 있는 플레이어 수를 체크합니다. (`ShowPlayers` command)
1. 플레이어 수가 0이면 RCON을 통해 `Shutdown` command 를 사용하여 서버를 정상 종료합니다.

## Future works

언제 걸릴지 모름

- 코드 정리
- pip install 지원
- Admin page 꾸미기
- 일정 시간마다 서버를 자동으로 재부팅. 재부팅 전 서버 메시지로 일정 간격마다 미리 알림
- 자동 백업
- IP Blacklist

## Change logs

### 0.0.2 (2024-02-03)

- 설정을 위해 settings.py 파일 대신 settings.json 을 수정하도록 변경
- 소켓에 임의의 패킷이 입력되는 경우 UDT 연결이 종료되는 문제 수정

### 0.0.1 (2024-01-28)

- 최초 커밋

## License

MIT

## Dependencies

- [py-rcon](https://github.com/ttk1/py-rcon)
- [psutil](https://pypi.org/project/psutil/)
- [Schedule](https://pypi.org/project/schedule/)
- [Flask](https://pypi.org/project/Flask/)

## Happy??

<a href="https://www.buymeacoffee.com/nomomo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-yellow.png" alt="Buy Me A Coffee" height="60"></a>
