# 第二阶段报告

## 小组分工

郑子姗：代码框架，棋盘、棋子绘制、挪子逻辑

蔡乐宜：吃子逻辑、显示信息、结束逻辑

张宇衡：整体debug及内容补充、超时及认输判定

## 亮点

我们灵活的使用了namespace来避免不同代码之间可能的命名冲突，灵活的使用Qtimer来实现游戏结束若干秒后自动重开，我们灵活使用widget和status bar来添加小组件并能在状态栏显示游戏最终结果。
我们使用了对周围点的比较算法和有效点击区域算法来使得点击在棋子所覆盖的范围内都能操控棋子，大大增强了操作的简便性，同时可以判断对棋盘的非法点击。

## 代码框架

我们使用qpainter类绘制棋盘和棋子，使用mainwindow类来代表和操纵棋子，建立了gamemap数组来帮助判断棋盘信息，使用statusbar类显示信息，以及把原有的Surakarta各个类稍加修改来判断游戏信息。

我们的设计流程如下： 1. 绘制棋盘、棋子 2. 编写基本移子逻辑，包括如何判断鼠标点击、编写移子和吃子规则逻辑，利用原有rule判断该动作是否合法，从而决定是否更新棋盘

其中判断鼠标点击的方法如下：我们先用——函数来获取鼠标的位置，然后计算出鼠标和各个点之间的距离，与模糊边界做比较，从而得知鼠标点击的具体格点坐标
判断的其中一部分代码如下：

```int x = event->x(); // 获取鼠标位置
int y = event->y();
int selectId = -1;
if (!beinside(x, y))
    return;
int col = (x - kBlockSize * 2 - kBoardMargin) / kBlockSize; // 列 x
int row = (y - kBlockSize * 2 - kBoardMargin) / kBlockSize; // 行 y
int leftTopPosX = kBoardMargin + kBlockSize * 2 + kBlockSize * col;
int leftTopPosY = kBoardMargin + kBlockSize * 2 + kBlockSize * row;// 设初值
clickPosRow = -1;
clickPosCol = -1;
int len = 0;
selectPos = false;
bool have_position = 0;// 计算鼠标和点的距离 判断鼠标要点哪个点
len = sqrt((x - leftTopPosX) * (x - leftTopPosX) + (y - leftTopPosY) * (y - leftTopPosY));
if (len < kPosDelta)
{
    clickPosRow = row;
    clickPosCol = col;
    if (game->gameMap[clickPosRow][clickPosCol] != 0)
        selectPos = true;
    have_position = 1;
}
```

更新棋盘的方法如下：我们用布尔值piece_clicked和select数组来标记并判断轮到一方下棋时鼠标是第几次点击 鼠标第一次点击的位置为对应要移动的棋子位置坐标，鼠标第二次点的位置为该棋子要移动到的地方

```game->gameMap[clickPosRow][clickPosCol] = game->gameMap[selectPosRow][selectPosCol];
game->gameMap[selectPosRow][selectPosCol] = 0;
```

我们通过gamemap数组来表示棋子的状态，再运用surakarta的判断逻辑来确定移动是否合法，如果合法就通过重画棋盘来更新位置。

3. 编写游戏结束相关逻辑，利用endreason判断游戏是否结束
4. 编写信息条代码，显示游戏轮数以及玩家信息
5. 编写超时、认输结束游戏逻辑代码

游戏分为pvp和pvc两个模式，其中pvc暂未编写；游戏结束后点击pvp即可重启再来一局

## 遇到的问题及解决方法

我们在编写过程中发现有时自行添加的代码逻辑无法和原有的rule和game类契合，因此稍加改动，将原有逻辑与现有代码整合，成功判断了移子和吃子规则。
