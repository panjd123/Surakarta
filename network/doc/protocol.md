# 网络协议

## 游戏基本流程

**6路棋盘**

1. 客户端连接服务端
2. 客户端向服务端发送 `READY_OP` 表示准备就绪
3. 服务端收到两个来自不同客户端的`READY_OP`后认为选手已就绪，向客户端发送`READY_OP`表示比赛开始，对黑棋方开始计时
4. 双方轮流发送 `MOVE_OP`
5. 当一方认输、超时或违规，比赛结束
6. 服务端向双方发送`END_OP`表示游戏结束，可以离开
7. 任意一方发送 `LEAVE_OP` 后，可以断开连接（在这之前保持连接）或 **任意一方**发送 `READY_OP` 请求再来一局，相当于做了第二步

> 更具体的协议请仔细阅读以下内容，仔细按照协议通信。如果发现协议有漏洞（少考虑等），可以在 Issues 中反应，或微信和助教探讨。

## 网络协议

一个完整的请求包含一个操作符 `OP` 以及至多三个数据段 `data1` 、 `data2`和`data3`。操作符指定了当前请求需要执行的操作，数据段则在此基础上给出了一些额外信息。

下面给出本次作业中可能用到的所有请求及其处理行为，"空"代表接收方可以不处理（但也要能接受为空，不能假设这个一定有值），发送方也可以置这个数据段为空。

### `READY_OP`

即是准备，也是申请。**请求对局方**要向服务端发送自己希望执的颜色，对方同样回应 `READY_OP` 表示对局成立。

1. 建立连接成功时，客户端是请求对局方，也就是服务端在收到客户端任何通信前不与客户端进行交流。
2. 对局结束后，若需要再来一局，客户端需要向服务端再次发送`READY_OP`。

- `data1`: 己方用户名
- `data2`: 己方执棋颜色（**服务端回应该字段留空**）
- `data3`: 房间号，约定为`[0,255]`内的整数

**用户名**：只能包含英文字母大小写、数字和下划线 `_`，不得包含空格、换行符、制表符等分隔符。

**颜色编码**：黑则 "`BLACK`"，白则 "`WHITE`"。

**房间号**：阶段三并不要求服务端支持多房间联机，没有实现多房间服务端附加任务的小组，房间号可以默认发送`1`，规定正式比赛时房间号为`1`。

### `REJECT_OP`

客户端向服务端发送`READY_OP`后，若服务端判断客户端对局准备不合法，会向其发送`REJECT_OP`拒绝连接。

- `data1`: 对局准备不合法的客户端用户名
- `data2`: 空
- `data3`: 空

> 例如，服务端同一个房间收到了两个客户端执黑棋的`READY_OP`，则判定第二个（时间顺序上）发送`READY_OP`的客户端对局准备不合法

### `MOVE_OP`

决定如何行棋后，向服务端发送 `MOVE_OP`

- `data1`：初始点坐标
- `data2`：移动后点坐标
- `data3`：空

坐标编码：用 `A1`，`F6` 这种表示，坐标轴方向同 [surakarta.md](../../guidance/surakarta/surakarta.md) 中所示，双方不旋转棋盘，也就是视角是相同的。

> 关于服务端的超时判断，我们不妨规定，服务端将来自客户端`A`的`MOVE_OP`转发给客户端`B`后开始计时（特别地，开始游戏时，双方就绪后服务端从发送`READY_OP`开始对黑棋方计时），如果在规定时间内没有收到来自`B`的`MOVE_OP`则判断`B`超时，忽略局域网延迟

### `GIVEUP_OP`

认输，替代 `MOVE_UP`，向对方发送 `GIVEUP_OP`

- `data1`：己方用户名（空）
- `data2`：问候语（空）
- `data3`：空

> 无处落子时及时认输才是君子之道

### `END_OP`
`END_OP`表示游戏结束，服务端向双方发送，客户端收到后可以断开连接，或发送再来一局的准备。

数据段格式参考阶段一的[测试程序规定](https://github.com/panjd123/Surakarta-RuleAiTest/blob/main/src/surakarta/)。

数据段含义是

- `data1`: 胜者棋子颜色
- `data2`: 游戏结束原因，若一方中途离开此处可留空
- `data3`: 最后一次`MOVE_OP`的性质，若游戏以一方认输结束或一方中途离开，此处留空

具体格式为
```c++
enum class PieceColor : PieceColorMemoryType {
    BLACK,
    WHITE,
    NONE // 平局规定棋子颜色
}; // data1
enum class SurakartaEndReason {
    STALEMATE,     // both players can't make more move
    CHECKMATE,     // one player's all pieces are captured
    TRAPPED,       // one player's pieces are all trapped, no legal move can be made.
    RESIGN,        // one player resigns.
    TIMEOUT,       // one player's time is out.
    ILLIGAL_MOVE,  // one player makes an illegal move
}; // data2
enum class SurakartaIllegalMoveReason {
    LEGAL,                     // unused
    LEGAL_CAPTURE_MOVE,        // capture a opponent's piece, and the move consists at least one corner loop
    LEGAL_NON_CAPTURE_MOVE,    // just as the name
    ILLIGAL,                   // unused
    NOT_PLAYER_TURN,           // unused, move when it's not the player's turn.
    OUT_OF_BOARD,              // from or to position is out of board
    NOT_PIECE,                 // move a position that is not a piece
    NOT_PLAYER_PIECE,          // move a piece that is not the player's
    ILLIGAL_CAPTURE_MOVE,      // try to capture a opponent's piece, but the move can't consist any corner loop
    ILLIGAL_NON_CAPTURE_MOVE,  // otherwise
    GAME_ALREADY_END,          // unused
    GAME_NOT_START             // unused
}; // data3
```

数据段发送**字符串**即可，无需发送枚举变量。

### `LEAVE_OP`

任何时候，发送 `LEAVE_OP` 说明即将立刻断开连接，如果在游戏进行时离开，判定另一方胜利。

- `data1`：己方用户名（空）
- `data2`：离开的原因（空）
- `data3`：空

> 任何时候，断开前都先发 `LEAVE_OP`，以区分意外断开。接受方可以不用回复，直接断开（不用回复，但一定要断开）。
>
> 这里的“断开”需要解释一下，对于我们的网络库，你可以理解成这里只能客户端主动断开服务端（也就是接口里的 bye），然后客户端甩手就走，不管服务端愿不愿意。反过来服务端要主动和客户端断开只能约定一个协议，服务端给客户端发一个特定消息后（比如上面的 END_OP），客户端再同上主动离开（bye），然后服务端收到这个这个信号后才会离开（对应槽函数 leave）。具体的 TCP 协议怎么处理这些问题远远超过了本课要求，所以你不需要深究。
>
> 所以你实现这个操作的全过程大概会像这样：
> 
> - 客户端主动离开时先发 `LEAVE_OP` 再 `bye`，服务端收到 `bye` 后会自动触发槽函数 `leave` 断开。
> - 服务端主动断开先发 `END_OP`，客户端收到后可选地回复 `LEAVE_OP` 然后必须执行 `bye`，服务端收到 `bye` 后自动触发槽函数 `leave` 断开。注意：服务端主动断开的情况只有与胜者断开或出现平局时与双方均断开。
> - 为了简单，**你可以假设**服务端一定会收到客户端回复的 `bye`，但如果真的没收到，你可以在一开始打算主动断开时就从逻辑上断开连接，也就是以后收到这个 client 发的信号都直接 return 不处理。或者你可以自己研究网络协议和 Qt 的原始网络库设计更合理的方法来处理，但这远远超过了本课程的要求范围。

### `CHAT_OP`

只要保持连接，就可以发送 `CHAT_OP` 聊天或交换信息。

- `data1`：用户名
- `data2`：信息内容
- `data3`：空

> 上面所提到的特殊编码（颜色，坐标，用户名）均不能莫名其妙包含空格，制表符，换行等无关字符，保证编码严格统一。
