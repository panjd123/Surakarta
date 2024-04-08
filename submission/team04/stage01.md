- 1. **游戏规则**

  - JudgeEnd

    - 无特别的东西，只是直接根据传入的`SurakartaIllegalMoveReason`一一进行判断，以下是具体的判断

    - `SurakartaIllegalMoveReason::LEGAL_NON_CAPTURE_MOVE`

      - 合法的不吃子移动。只需判断不吃子轮数是否超过了最大的不吃子轮数即可，即`(game_info_->num_round_ - game_info_->last_captured_round_)>= game_info_->max_no_capture_round_`

      - 小于则游戏继续，大于则游戏结束并根据场上棋子的剩余个数判断输赢。

    - `SurakartaIllegalMoveReason::LEGAL_CAPTURE_MOVE`
      - 判断剩余对手棋子是否还有即可。还有则继续游戏，没有则游戏结束，当前棋手胜利。

    - 其他直接返回不合法的移动导致游戏结束。

  - JudgeMove

    - 关键在于吃子逻辑的判断，其他判断应该很直接，以下重点讲述本组的吃子逻辑的实现。

      - 如果`move.to`位置的棋子是对方棋子则进入吃子逻辑的判断

        - 添加的函数和类的成员

          - 在SurakartaBoard类中加了一个circle类的数组成员，而circle存储的是n * n棋盘的某一条吃子路径。

          - 在SurakartaRuleManager类中增加了`bool Eat(const SurakartaMove& move);`和`bool EatCircle(const SurakartaMove& move,const circle& circle,unsigned int& i);`函数。

        - 具体实现逻辑

          - 在`bool Eat(const SurakartaMove& move);`中会遍历board中的每一个circle中的每一个位置，并判断move.from是否在某一条吃子路径上。

          - 如果在，则进入`bool EatCircle(const SurakartaMove& move,const circle& circle,unsigned int& i);`开始判断是否为合法的吃子。i记录了move.from的位置，circle表示当前的具体的一条吃子路径，move是吃子移动的起始点。

            - 此函数中判断的核心为两个。

            - 一是是否经过了圆弧。由于在生成每一条circle时，"拐弯点"的位置即下标都是固定的，这为判断带来便利。只需看在遍历停止前是否经过了两个相邻的"拐弯点"即可。

            - 二是遇到的第一个棋子是否为对方棋子。这只需在遍历到第一个棋子时判断其颜色即可。这里一开始并未考虑到有些点在路径中出现了两次并且会再度遍历到自己的可能性，导致某些合法走法被判成非法，加了`(circle[index]->x == move.from.x && circle[index]->y == move.from.y)` 该判断后即可解决该问题。

      - 

- 2. **AI**

  - 本组在本阶段并未对AI实现有过高要求，而是直接进入图形化界面的设计，因而只是实现了最简易的AI。

  - 算法
    - 贪心

  - 实现

    - 写了三个函数。`GetAllPositions`,`CalculateMarks`,`GetBestMove`,各自的功能为获取所有可能的移动，计算当前棋盘的分数，获取最好的一步

    - `GetAllPositions`
      - 就找到场上所有的当前玩家的棋子，存储为move.form，并根据JudgeMove得到所有可能的move.to，把由此得到的所有可能的move存储起来。

    - `CalculateMarks`

      - 计算分数的方式没有进行太多思考，给吃子给了最高的分数，即让场上对手的棋子更少。同时给越往中间靠的棋子更高的分数。

      - 目前还在暂时并未实现相同估值的情况下随机选择一种走法。

    - `GetBestMove`
      - 根据`GetAllPositions`走可能的所有步数，由`CalculateMarks`得到所有合法步的分数，选取最大分数的move进行移动

- 3.**分工**

  - 游戏规则 : 向禹 肖俊皓 

  - AI : 肖俊皓

  - 代码仓库创建管理与提交  : 常皓飞

  - 正在实现图形化界面 :  常皓飞 向禹




