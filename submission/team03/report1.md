# 第一阶段报告

## 综述与概况

在这一阶段，我们组实现了 Surakarta 棋的规则助手以及一个简单的基于搜索算法的 AI。在[这里](https://github.com/surakarta-game/surakarta-rule-ai)可以看到我们的代码。

我们的代码不仅可以通过[panjd123](https://github.com/panjd123/Surakarta)提供的测试，而且也可以通过我们为了测试[部分新增组件](https://github.com/surakarta-game/surakarta-rule-ai/blob/main/src/surakarta/surakarta_utils.h)而[添加的测试](https://github.com/surakarta-game/surakarta-rule-ai/blob/537679bd528ec36845d6fa81f992a1800e4bd16f/src/tests/surakarta_rule_manager_test.cpp#L94)。同时，我们的 AI 可以有效地击败随机 Agent，在搜索层数分别为3，4，5时击败随机 Agent 的概率分别为 93.77%，95.39%，96.78%，不被击败的概率分别为 96.88%，99.51%，（99.95%）。

## 规则助手使用的算法

我们使用了一个很有用的抽象，这一抽象基于这样一个事实：在吃子的过程中，我们想象棋子是一格一格逐渐移动的，给定一个棋子和一个方向（上下左右），我们便可以唯一地确定棋子运动一格后到达的位置和朝向的方向。这一抽象在[SurakartaPieceMoveUtil](https://github.com/surakarta-game/surakarta-rule-ai/blob/537679bd528ec36845d6fa81f992a1800e4bd16f/src/surakarta/surakarta_utils.h#L91)中实现：
```
算法 下一格(位置甲, 方向甲)
返回 (位置乙, 方向乙) 或 无法移动
过程 根据规则挪动棋子，略
```

我们判断一个棋子是否可以移动到某个位置的算法位于[SurakartaMovablityUtil](https://github.com/surakarta-game/surakarta-rule-ai/blob/537679bd528ec36845d6fa81f992a1800e4bd16f/src/surakarta/surakarta_utils.h#L406C7-L406C29)，这一算法的思想是根据规则穷尽某棋子可以到达的所有位置:

```cpp
算法 可以不吃地移动到(棋子，目的位置)
返回 可以 或 不可以
过程 穷尽 上、下、左、右、左上、右上、左下、右下
        常量 下一格位置 = 棋子按这个方向移动到达的位置
        如果 下一格位置 没有棋子
            返回 可以
    穷尽完毕
    返回 不可以

算法 可以吃子地移动到(棋子，目的位置)
返回 可以 或 不可以
过程 穷尽 上、下、左、右 并用 初始方向 表示
        变量 当前位置 = 棋子 的 位置
        变量 当前方向 = 初始方向
        变量 跨过弧线的次数 = 0
        循环 直到 明确地退出
            常量 移动结果 = 调用算法“下一格(当前位置, 当前方向)”
            如果 移动结果 是 无法移动
                退出循环
            常量 (下一个位置, 下一个方向) = 移动结果
            当前位置 = 下一个位置
            如果 下一个方向 ！= 当前方向
                跨过弧线的次数 加一
            当前方向 = 下一个方向
            如果 当前位置 == 目的位置
                如果 跨过弧线的次数 > 0
                    返回 可以
                否则
                    退出循环
            如果 当前位置 有棋子
                退出循环
            如果 (当前位置 == 棋子 的 位置) 且 跨过弧线的次数 == 4
                退出循环
        继续循环
        循环结束
        返回 不可以

算法 可以移动到(棋子，目的位置)
返回 可以 或 不可以
过程 调用算法”可以不吃地移动到(棋子，目的位置)“
    调用算法“可以吃子地移动到(棋子，目的位置)”
    如果 上述两次调用有至少一个结果为“可以”
        返回 可以
    否则
        返回 不可以
```

此外，我们通过[SurakartaGetAllLegalTargetUtil](https://github.com/surakarta-game/surakarta-rule-ai/blob/537679bd528ec36845d6fa81f992a1800e4bd16f/src/surakarta/surakarta_utils.h#L266)穷尽一个棋子可以到达的所有位置。[SurakartaGetAllLegalTargetUtil](https://github.com/surakarta-game/surakarta-rule-ai/blob/537679bd528ec36845d6fa81f992a1800e4bd16f/src/surakarta/surakarta_utils.h#L323)通过对棋盘上某方的每一个存在的棋子调用上述算法，来穷尽某方全部可能的移动。这一算法虽然简单，但是是我们 AI 算法的基础。

## AI 使用的算法

我们的 AI 采用了搜索算法，[代码](https://github.com/surakarta-game/surakarta-rule-ai/blob/main/src/surakarta/surakarta_agent/surakarta_agent_mine.cpp)并不复杂，仅有 65 行。伪代码如下：
```
算法 计算权重(移动, 剩余深度)
参数 alpha 和 beta
返回 浮点数
过程 如果 (当前为我方)
        变量 权
        如果 这一移动是吃子的
            权 = 1
        否则
            权 = 0
        如果 剩余深度 > 1
            找出 对方下一步全部的可能移动
            使用算法“计算权重(移动, 剩余深度 - 1)”计算出每一个对方的移动的权重
            返回 这些权重中最小的 乘以 alpha
    否则（即当前为对方）
        变量 权
        如果 这一移动是吃子的
            权 = -1
        否则
            权 = 0
        如果 剩余深度 > 1
            找出 我方下一步全部的可能移动
            使用算法“计算权重(移动, 剩余深度 - 1)”计算出每一个我方的移动的权重
            返回 这些权重中最大的 乘以 beta

算法 找出最佳移动
参数 alpha、beta 和 深度
过程 找出我方全部可能移动
    使用算法“计算权重(移动, 深度)”计算出每一个我方的移动的权重
    返回权重最大的移动
```

## 小组分工

- [李甘](https://github.com/orgs/surakarta-game/people/Nictheboy)： 修改另外两位组员的代码并撰写了报告
- [李佳祎](https://github.com/orgs/surakarta-game/people/TheSkyFuker54188)： 写出了第一个版本的JudgeMove，学习面向对象程序设计范式和 Qt 类库的相关功能，并为其他组员提供了鼓励
- [杨雪苹](https://github.com/orgs/surakarta-game/people/xiaoyang060219)： 写出了第一个版本的EndReason，学习面向对象程序设计范式和 Qt 类库的相关功能，并为其他组员提供了鼓励

## 代码框架设计

采用了[panjd123](https://github.com/panjd123/Surakarta)提供的代码框架

## 遇到的问题及解决方法

最初，经常遇到 Segmentation Fault。经尝试发现，错误的原因是修改了[surakarta_rule_manager.h](https://github.com/surakarta-game/surakarta-rule-ai/blob/main/src/surakarta/surakarta_rule_manager.h)。我们猜测，由于[libsurakarta_ta_lib.so](https://github.com/surakarta-game/surakarta-rule-ai/blob/main/surakarta_ta/lib/libsurakarta_ta_lib.so)中的[SurakartaRuleManagerImp](https://github.com/surakarta-game/surakarta-rule-ai/blob/main/src/surakarta_ta/surakarta_rule_manager_imp.h)类以[SurakartaRuleManager](https://github.com/surakarta-game/surakarta-rule-ai/blob/main/src/surakarta_ta/surakarta_rule_manager_imp.h)类为基类，而前者在编译时使用了后者未经修改的头文件，所以导致修改[SurakartaRuleManager](https://github.com/surakarta-game/surakarta-rule-ai/blob/main/src/surakarta_ta/surakarta_rule_manager_imp.h)的声明后偏移量不一致，导致运行时错误。不再修改这一文件后问题解决。解决错误过程中仓库的快照位于[这里](attachment/PoC.zip)

一开始 AI 算法中最后的“最大”写成了“最小”，导致几乎每局必输。在分析后想到可能是因为某处写反导致的，于是成功定位到了错误。

## 原始数据

各个层数下 AI 与随机 Agent 对局的胜率数据可以在[这里](attachment/ai-data-1.txt)看到。

## 特别鸣谢
- [panjd123](https://github.com/panjd123/Surakarta)：为我们提供了[基础框架、标准程序和单元测试](https://github.com/panjd123/Surakarta-RuleAiTest)
- [CH3COOH-JYR](https://github.com/CH3COOH-JYR)：为我们提供了算法的基础思路
- [yermog](https://github.com/yermog)：我们对于如何实现 Agent 之间的对决进行了富有启发性的讨论
- [andylizf](https://github.com/andylizf)：教会了我[规范的 commit 格式](https://www.conventionalcommits.org/en/v1.0.0/)，并在[某些事情](https://github.com/SageSeekerSociety/cheese-backend)中体谅了我时间的紧张，使本阶段的按时完成成为了可能

