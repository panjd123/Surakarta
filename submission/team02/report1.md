# 第一阶段报告

## JudgeMove规则判断

### 吃子

我们通过数组手动维护了两个大小圈分别的吃子路径，并在判断吃子动作是否合法时从正反两个方向分别搜索这两条吃子路径。如果路径有经过完整的弧线并且没有其它棋子遮挡，就判断这个动作是LEGAL_CAPTURE_MOVE；反之就是ILLEGAL_CAPTURE_MOVE。同时，吃子还需要满足to所在的位置是敌方的棋子，否则这个动作应该归属于不合法的非吃子行为。

*在这个部分，为了节省存储空间，我们将棋盘的二维数组进行id编码，然后用这个一维编码存储吃子路径。例如：*

### 移动

为了减少可能的歧义，我们先判断是否是合法/非法吃子动作再判断是否是合法/非法的移动动作。先判断吃子可以确保from的位置是己方棋子、to的位置是空位。

在这一部分的判断中我们先排除了几种特殊的非法动作：通过将move.player与current_player进行比较，判断是否是NOT_PLAYER_TURN；通过判断from位置的棋子先判断是否是NOT_PIECE或者NOT_PLAYER_PIECE；通过比较from和to的x与y判断是否在棋盘内，从而检查OUT_OF_BOARD的这类情况。排除了上述情况后，再通过将from.x与to.x，from.y与to.y的绝对值与1比较来判断移动的距离是否规范。如果是，那么判断这是一个LEGAL_NON_CAPTURE_MOVE;若不是，那么判断这是一个ILLEGAL_NON_CAPTURE_MOVE。

*注：存在一种特殊情况，就是棋子进行的是合法距离的移动动作，但to的位置有对方棋子，这个非法动作的判断究竟属于哪一类不易分析。但通过测试我们最终将这个动作归属于ILLEGAL_NON_CAPTURE_MOVE。*

## JudgeEnd规则判断
###
1. CHECKMATE：
我们先统计了白棋和黑棋的数量。 
若出现以下情况：
- 如果其中有一方的数量小于等于1且当前由另一方落子，如果另一方有合理的吃子行为,则游戏结束，结束理由为CHEKCKMATE，即一方的棋子全部被吃完，另一方获胜。
- 如果有一方棋子已经全部被吃完则判定另一方获胜，结束理由为CHECKMATE。
  
2.ILLIGAL_MOVE：
- 如果有一方是不合法吃子或不合法移动，则游戏直接结束，结束理由为ILLIGAL_MOVE，另一方获胜。
  
3.STALEMATE：
如果没有出现合法的吃子行为，则做如下判断：
- 一旦没有吃子的轮数大于max_no_capture_round（ *具体判断代码如下(game_info_->num_round_) > game_info_->max_no_capture_round_ - 1 + game_info_->last_captured_round_* ）则判定为僵局，棋手不能再做任何有效移动，即认为游戏结束，结束理由为STALEMATE，并根据黑白棋的剩余总数判断获胜方，总数多的获胜（或相同，则平局）。

## Surakarta_Agent AI 思路
在这一部分我们采用了一个简单的贪心算法，先维护一个数组，内容是为棋盘上的每一个点按照优先级赋予不同的分值（学习参考文献1进行棋盘上棋子的价值估计），然后对于棋盘上每一个己方棋子所在位置的每一个合法落子点进行搜索。我们优先考察能够产生LEGAL_CAPTURE_MOVE即能够吃子的to位置，然后对它们进行排序。如果能吃子，那么就选择得分最高的的那个位置作为目标位置；如果不能吃子，就搜索所有能够合法移动的目标点，选择得分最高的一个将棋子移动过去。

    for (auto& p1 : from) {
        for (auto& p2 : to) {
            SurakartaMove move = {p1, p2, game_info_->current_player_};
            SurakartaIllegalMoveReason reason = rule_manager_->JudgeMove(move);
            if (reason == SurakartaIllegalMoveReason::LEGAL_CAPTURE_MOVE) {
                if(get_value(p1,p2)>sum)  {rd_move=move;sum=get_value(p1,p2);flag=1;}
            } 
        }
    }
    if(flag)return rd_move;//如果找到了，就进行这一步吃子动作
    for (auto& p1 : from) {
        for (auto& p2 : to) {
            SurakartaMove move = {p1, p2, game_info_->current_player_};
            SurakartaIllegalMoveReason reason = rule_manager_->JudgeMove(move);
            if (reason == SurakartaIllegalMoveReason::LEGAL_NON_CAPTURE_MOVE) {
                if(get_value(p1,p2)>sum){rd_move=move;sum=get_value(p1,p2);flag=1;}
            }//如果找不到最佳的吃子动作，就找最佳的不吃子位置 
        }
    }

## 小组分工
Surakarta_rule_manager由小组三位成员共同完成；Surakarta_agent_mine中张宇衡写了完整的贪心算法，蔡乐宜和郑子姗共同写了Minmax算法的框架，但最终合并采用了贪心算法作为Ai的思路。

## 参考文献
1.李东轩, 胡伟, 王静文. 基于Alpha-Beta算法的苏拉卡尔塔棋博弈系统研究[J]. 智能计算机与应用, 2022, 12 (02): 123-125.
