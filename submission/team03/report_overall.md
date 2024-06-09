# **Surakarta第二、三阶段报告**
## **一、代码实现**
### **A.初步实现游戏界面**
> 1.绘制棋盘棋子：
> 2.计时器：运用timerEvent函数，并通过ui界面的label显示倒计时。
> 3.选子落子：
> 4.游戏结束弹窗：
> 5.选择下棋模式：
### **B.完善逻辑**
> 1.使玩家可以选择黑棋或白棋：让代码中固定执棋方变为可以变动的参数，在ui中插入选项让玩家可以选择
### C.联网和ai接入
> 1.采用了十分先进的技术
### D.遇到的问题及解决方法
> 1.关于调换黑白棋执棋方：开始时调换执棋方会有闪现闪退的情况，在修复了原先代码中的一些问题后，能正常实现
## **二、任务分工**
- [李甘](https://github.com/orgs/surakarta-game/people/Nictheboy)：绘制游戏界面，实现游戏逻辑，实现联网，接入ai,热情地帮助其他同学在大作业中遇到的问题....(我不太知道其他的了)
- [李佳祎](https://github.com/orgs/surakarta-game/people/TheSkyFuker54188)：保存游戏棋谱，复现，显示可移动位置，书写阶段报告
- [杨雪苹](https://github.com/orgs/surakarta-game/people/xiaoyang060219)：倒计时，判断是否超时，玩家可以选择黑棋或者白棋，书写阶段报告

## **三、仓库地址**
(https://github.com/surakarta-game/surakarta-game.git): 主仓库
(https://github.com/surakarta-game/surakarta-core.git): 内含libsurakarta源代码，为"game"提供"rule management" 和 "AI" 功能
(https://github.com/surakarta-game/qt-cmake-windows-workflow.git): qt部分
(https://github.com/surakarta-game/network-framework.git): 网络部分
