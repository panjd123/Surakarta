## Team10 第一阶段报告

### 小组分工

孙浩翔 (CoderBak)：完成规则判断部分 Version 2, AI Version 1.A , 报告撰写

王燚 (smallsmallprogrammer)：完成规则判断部分 Version 1, 进行 Qt 学习

张昕跃 (imio21777)：完成 AI Version 1.B, 1.C, 进行 Qt 学习

注：Version 1.A,B,C 是平行的，分别用贪心、贪心、搜索实现，具体可见 commit 记录（快照），目前暂时采用 Version 1.A .

### 规则判断

#### JudgeEnd

首先判断该 move 是否 legal ，如果 illegal 直接返回 ILLEGAL_MOVE 即可.

接着计算棋盘上剩余棋子的个数，从而决定输赢.

最后，检查 STALEMATE 是否发生即可.

#### JudgeMove

首先检查一些基本内容，即依次验证 `NOT_PLAYER_TURN`, `OUT_OF_BOARD`, `NOT_PIECE`, `NOT_PLAYER_PIECE`, `ILLIGAL_NON_CAPTURE_MOVE`.

接下来较为复杂的是检查吃子的可行性. 王燚同学的 Version 1 固定棋盘大小为 6 , 进行了一系列判断（可以通过测试）. 为保证代码的可复用性和清晰度，同时支持 `board_size_` 不是 `6` 的情况，孙浩翔同学采用了以下的方法：

首先，将判断过程抽离 `JudgeMove` 函数，定义

```cpp
bool check_valid_move(const SurakartaPosition from, const SurakartaPosition to,
                      const std::shared_ptr<const SurakartaBoard> &board, const unsigned int n);
```

来检查一个吃子是否合法. 该函数通过调用 `search` 函数来向四个方向进行搜索，判断是否能够吃到目标棋子.

`search` 函数的实现较为朴素. 逐步走子，判断是否到达目标点即可.

这里我们需要考虑旋转的情况. 这里我们采用最容易理解和最清晰的方式：定义函数

```cpp
std::pair<SurakartaPosition, Direction> get_next_pos(const SurakartaPosition from, const Direction dir, const int n);
```

具体来说，我们希望，知道当前位置和走棋的方向，就可以知道走完这一步后新的位置和新的方向. 例如，在底线往南走，就会通过螺旋到达左侧（或右侧）最边上，并且方向变换为向东或向南. 这样实现的判断方式非常清晰明了，同时可以用在后续的搜索算法代码中. 该函数的具体实现可以参考我们的代码库.

于是，search 过程中，不再需要考虑坐标变换等复杂内容，只需要每次将当前位置和朝向更新为 `get_next_pos` 的返回值即可.

通过这种方式实现的代码简短易读，同时具有良好性能.

### AI 实现

目前我们实现的是贪心算法（后期会调整为搜索或其他算法）. 具体来说，我们考虑估价函数 $f$ (在代码中叫 `strategy`). 枚举所有我们可以移动的点，借助我们上面的 `search` 和 `get_next_pos` 函数得到所有可以吃的点，于是形成了一系列合法吃子移动 $(x,y)$ .

在这里，我们构造了以 $(x,y)$ 为元素的优先队列，其比较器即为 $f$ ，从而我们可以先从所有合法旋吃中选取 $f$ 最大的. 目前我们的 $f$ 取为 $y$ 到中心点的曼哈顿距离的相反数，即越靠近中心的点权重越大. 当然由于我们从算法中剥离了 $f$ 的构造，实际上只需要改变 `strategy` 函数即可改变贪心策略. 目前的估价函数还有待优化，后期将进行改进.

如果旋吃不存在，我们就会从所有移动中任意选取一个.

### 设计亮点

I. make 阶段实现了 0 error 0 warning

II. 合理的算法设计：支持任意 `board_size_` ，具有高扩展性，例如贪心策略函数

III. const correctness 的充分保障

在所有应该使用 const 声明的位置均使用了 const 声明，保证了程序的 const correctness

IV. 合理的变量命名与注释，合理的架构设计

V. 充分利用 move semantics 移动语义

通过尽可能使用 emplace_back 等移动语义来优化代码

VI. 运算符重载

通过重载运算符（例如 SurakartaMove 的 == 运算符）来使得代码清晰易懂

VII. STL 的充分使用

通过使用 STL 自带的优先队列，简化了代码

VIII. C++ 新特性的充分使用

在编程过程中使用各种语法糖和新特性，例如 auto binding (since C++17) ，lambda function (since C++11) ，auto (since C++11) ，for-each loop (since C++11) ，if with initializer (since C++17) 来大幅增强代码可读性和简洁程度

IX. 显式类型转换

在各种运算中，不可避免地要出现 `unsigned int` 加 1 减 1 之类的情况. 我们通过 `static_cast` 进行显式类型转换，防止 `unsigned int` 出现溢出，更加安全

X. 内存安全

全部使用智能指针，遵循 RAII 设计理念，降低了出现内存问题的概率

### 附注

I. 由于未来将在 Qt 中重写整个对象逻辑，故该阶段没有将 `get_next_pos` 等函数抽象到 `surakarta_toolset.cpp` 之类的文件中去.

II. AI 算法未来将会继续更新.

III. 为了进一步提高性能，实际上应该为各个 copy constructor 和 operator= 重载提供 rvalue 版本来支持 move semantics. 由于之后我们将重构整套代码，此处先不做处理.
