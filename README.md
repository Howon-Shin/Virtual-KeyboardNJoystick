"# Virtual-KeyboardNJoystick" 

구현된 기능
- 키보드 입력 (pyautogui)
  * 일부 온라인게임에선 막혀있거나 정지시키는 듯 함(매크로방지)
- 투명 배경, 작업표시줄 등등 (setWindowFlags, setAttribute)
- 윈도우 포커스 회피 (win32api - SetWindowLongPtrW - WS_EX_NOACTIVATE)
- 윈도우 위치, 크기 조절 (mouse Press/Move Event)
  * setting mode 때 조절하면 Meme data 생성과 충돌로 드래그 끊겨서 normal mode 때만 작동
  * mousePressEvent와 clicked.connect 충돌로 QPushbutton으로 만들면 mousePressEvent 미작동
    -> 일단 QLabel로 해놓고 Press 위치 좌표에 따라 위치/크기 조절 구분
- 버튼 위치 조정 (dropEvent)
  * 상속 클래스로 만드려했으나 mousePressEvent와 clicked.connect 충돌
  * VirtualKeyboard의 self.setting 변수를 버튼 클래스에서 받아올 수 있으면 clicked.connect 기능을 mousePressEvent로 옮길 수 있을 것으로 생각 (공부 필요)
- 버튼 추가 (add_click)
  * 제거는 미구현이지만 구현 어렵지 않을 듯
- 버튼 세팅 저장/불러오기 (save_btns, load_btns)
  * txt 파일에 저장
  * txt 파일에 문제 있으면 재시작(os.execl)

구현 못한 것
- 멀티 터치
  * 정보 부족?
- 위치 조정시 처음 마우스 위치에 맞추기/이동시 이미지
  * 상속 클래스로 구현시 되는 건 확인
