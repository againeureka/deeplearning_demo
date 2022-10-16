# README



### M1 Mac, PyQt5 실행하는 법

- How can I run pyqt5 on my Mac with M1chip (ppc64el architecture)?
- https://stackoverflow.com/questions/65901162/how-can-i-run-pyqt5-on-my-mac-with-m1chip-ppc64el-architecture


- Open terminal with Rosetta 2
  (https://dev.to/courier/tips-and-tricks-to-setup-your-apple-m1-for-development-547g)
  
- 아키텍처가 i386인지 확인

```bash
    $ arch
    i386
```
  
- Use non-homebrew python (mine was in /usr/bin/python3) to create virtual environment

```bash
    $ /usr/bin/python3 -m venv env
```

- 가상환경 진입

```bash
    $ source env/bin/activate
    $ which python3

- Upgrade pip

```bash
    $ pip install --upgrade pip
```

- Install PyQt5

```bash
    $ pip install PyQt5
```


### 추가 작업

```bash
    $ pip install -r requirement.txt
```