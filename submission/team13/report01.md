# Team13 第一阶段报告

### 一、判断所采用的算法:
1. Judgemove函数，首先特殊判断几种非法移动，包括非玩家回合，超出棋盘范围的移动，移动非棋子位置和非该玩家棋子的情况，返回对应的SurakartaIllegalMoveReason中的非法移动。然后关于吃子移动的判断，具体实现是讲二维棋盘数组顺序依次编号，储存在一维数组中，则该一维数组即为吃子移动的弧线，分别从顺时针和逆时针方向进行判断能否吃子，同时要注意吃子是否经过弧线，即通过对拐角处特殊点的判断来确认。非吃子移动，只需要注意移动目标位置没有棋子，移动距离横竖坐标不超过1即可。
2. Judgeend函数，首先检查非法移动情况，根据返回值判断胜负，其次判断游戏正常结束，即玩家最后一子且被合法吃子，则游戏结束。然后是通过移动回合数判断是否棋局结束，返回棋子数多的一方为赢家。

### 二、AI 所采用的算法:
1. 遍历棋盘，找到自己的棋子（from）与能走的位置（to）。
2. 建立估值函数，对每一个move的需求度进行估值。对每一个from，calculate一个score1以反映from此点是否会被吃（特别的，若from是a1 f1 a6 f6，则额外-50）；对每一个to，calculate一个score2以反映to此点是否会被吃（//特别的，若to是b3 e3 b4 e4且不会被吃，则额外加10）；对每一对from&to（即每一个move），calculate一个score3以反映此move能否吃（使用judgemove函数）。（score1：不走就会被吃，+50；不走不会被吃，+0。）（score2：走后不会被吃，+30；走后会被吃，-40。）（score3：走可以吃，+60；走不能吃，+0。）
3. 对于如何判断某位置是否会被吃，建立两个函数：whether_be_eaten与whether_willbe_eaten，分别判断移前移后是否会被吃。建立一个二维结构体数组，只暂存本次判断所在的棋盘（包含位置与颜色）。//建立4个函数，分别从x-0、x-boardside、y-0、y-boardside（即上下左右）四个方向检索是否能实现在“至少转一个弯“的前提下第一个遇见的棋子是对手棋子。如果是，则能被吃；如果在回到原点后仍未遇到棋子或者第一个遇到的棋子是同色棋子，则至少在本次判断里没有被吃的风险。
4. 用一个一维结构体数组记录各move的分值与move本身。找到highest_score。建立一个std::vector<SurakartaMove> moving，用于提取具有highest_score的move。运用std::shuffle(moving.begin(), moving.end()，GlobalRandomGenerator::getInstance())，实现相同分值者的随机性选择，最终选择该vector的front作为最终的return。

### 三、小组分工:
- 叶霁轩：完成ai（surakarta_agent_mine.cpp）。李佳俊、武思豪：完成rule。共同完成：submission。

### 四、遇到的问题及解决方法:
1. 不了解<memory>头文件的用法，通过b站和百度能够勉强理解。
2. 在judgeend 的时候有所欠缺考虑。
3. 在开始的时候对游戏规则不理解，看了github上面给的解释不理解，最后还是看了助教给的一个知乎上面的解释理解的。
4. 学习了vector等概念，通过chatgpt、csdn、知乎、randomagent代码等了解了一些用法；通过看助教的代码了解了随机数生成与洗牌，实现相同move间的随机选择
5. 需要在函数中建立函数，询问chatgpt得知可以建立区域类；类中函数无法使用在类外建立的结构体数组，于是希望将结构体数组放入类；但为了实现boardside可变化，数组边界需要是变量，而类里似乎不允许数组长度为变量，因此最后选择使用宏BOARD_SIDE作为代替。




