# Runtest



## Introduction
> 今年第一次参加家仿比赛的时候，给的测试数据在我的电脑上运行总是Broken pipe等各种情况
后来在Server端测试的时候并没有出现各种奇怪的问题，Server端用的是python程序测试，比赛
匆忙结束忘记向TC要代码了，为了以后调试测试方便写了个小程序来运行测试。

* This is a tool to run test data in HomeSimulation platform.

## Useage
* Exmaple:(Runing it stage-phase 1)
```
python runtest_it_1.py
```
### Modify
* Add Teams on runstage file:
```python
teams = {
"Example": "Example",
#Enter team list
}
```
* Change stage and test data amount
```python
ts = runtest.Tester(mode, phase , num)
```
mode:`"it"`,`"nt"`
phase: `1` or `2`
num: data amount(>=1)

* Change `cserver` and `client` file location in `Tester` class
```python
SERVERDIR=" " #Server Dir
CLIENTDIR=" " #Client Dir
```
* Change  More running command in `runtest.py`
