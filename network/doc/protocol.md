# 网络协议

## 游戏基本流程

1. 客户端连接服务端
2. 客户端向服务端发送 `READY_OP` 表示准备就绪
3. 服务端收到两个来自不同客户端的`READY_OP`后认为选手已就绪，服务端向双方客户端回复 `READY_OP` 表示比赛开始，对黑棋方开始计时
4. 客户端轮流发送 `MOVE_OP`
5. **服务端**收到某个客户端发送的 `MOVE_OP` 或后：
    1. 如果操作合法，操作会被转发给**双方客户端**
    2. 如果操作非法，操作仍然会先被转发给**双方客户端**，随后会发送 `END_OP` 给**双方客户端**，游戏结束，可以离开
6. 任意一方发送 `LEAVE_OP` 后，可以断开连接（在这之前保持连接，等待可能的 `READY_OP`）或任意一方发送 `READY_OP` 请求再来一局，相当于做了第二步

默认参数规定（比赛、测试或其他没另外指明的场合，你需要设置的默认参数）：

1. 棋盘：6路
2. 超时：3s
3. max_no_capture_round：40
4. 端口：10086
5. 用户名：Team0，0 改成你的小组
6. 房间号：1

比赛前根据测试情况，可能修改超时和max_no_capture_round以保证比赛可以在一节课内结束。如果你们有任何建议，可以直接发给助教。

> 更具体的协议请仔细阅读以下内容，仔细按照协议通信。如果发现协议有漏洞（少考虑等），可以在 Issues 中反应，或微信和助教探讨。

## 网络协议

一个完整的请求包含一个操作符 `OP` 以及至多三个数据段 `data1` 、 `data2`和`data3`。操作符指定了当前请求需要执行的操作，数据段则在此基础上给出了一些额外信息。

所有数据段都不应该包含空格、制表符、换行符等分隔符以及**中文**，以防止意外情况。

所有数据段都以 QString 形式发送，例如数字 1，应该发送字符串 `Qstring("1")`，枚举变量 `PieceColor::BLACK` 应该发送对应的整数的字符串，例如这里是 `QString("0")`。请用 `static_cast<int>` 和 `to_string` 等方法将枚举变量转换为整数再转换为字符串。

下面给出本次作业中可能用到的所有请求及其处理行为，"空"代表这个消息无关紧要，发送与否不应该影响你程序实现的正确性。

### `READY_OP(1)`

既是准备，也是申请。客户端要向服务端发送自己希望执的颜色和房间号。

> 对局结束后，若需要再来一局，客户端需要向服务端再次发送 `READY_OP`。

- `data1`: 用户名（空）
- `data2`: 执棋颜色（可为空，见自动执棋颜色）
- `data3`: 房间号，约定为`[0,255]`内的整数

**用户名**：只能包含英文字母大小写、数字和下划线 `_`，不得包含空格、换行符、制表符等分隔符。

用户名可以为空

**颜色编码**：黑则 "`BLACK`"，白则 "`WHITE`"，默认为空让服务器决定。

自动执棋颜色：客户端可以留空 `己方执棋颜色` 这一参数，由服务端自动分配。例如，如果一方 "`BLACK`"，一方为空，则空的一方为 "`WHITE`"。如果都为空，先连接到的为黑，后者为白。

**房间号**：阶段三并不要求服务端支持多房间联机，没有实现多房间服务端附加任务的小组，房间号可以发送`1`或者不发，规定正式比赛时房间号为`1`。

不打算做附加任务的服务端实现的时候可以完全不看这个参数，直接当作没有房间这个概念就行了。但如果服务端实现了多房间，收到客户端发送的空的时候，你视作 `1` 即可。

### `READY_OP(2)`

服务端收到双方的 `READY_OP` 后需要分别发送不同的 `READY_OP` 给双方客户端以通知对局开始，以及通知对局双方的用户名。

- `data1`: **通信方对手**用户名
- `data2`: **通信方**执棋颜色
- `data3`: 房间号

例如，Alice 发送了 `["Alice", "BLACK", "1"]` 的 `READY_OP`，Bob 发送了 `["Bob", "", "1"]` 的 `READY_OP`，服务端需要向 Alice 发送 `["Bob", "BLACK", "1"]` 的 `READY_OP`，向 Bob 发送 `["Alice", "WHITE", "1"]` 的 `READY_OP`。

### `REJECT_OP`

客户端向服务端发送`READY_OP`后，若服务端判断客户端对局准备不合法，会向非法一方发送 `REJECT_OP` 拒绝连接。

- `data1`: 对局准备不合法的客户端用户名
- `data2`: 拒绝理由（空）
- `data3`: 空

> 例如，服务端同一个房间收到了两个客户端执黑棋的`READY_OP`，则判定第二个（时间顺序上）发送`READY_OP`的客户端对局准备不合法。以及非法的用户名，非法的房间号，非法的颜色都需要拒绝。

### `MOVE_OP`

决定如何行棋后，客户端向服务端发送 `MOVE_OP`

- `data1`: 初始点坐标
- `data2`: 移动后点坐标
- `data3`: 空

坐标编码：用 `A1`，`F6` 这种表示，坐标轴方向同 [surakarta.md](../../guidance/surakarta/surakarta.md) 中所示（特别地，若你显示时需要旋转棋盘，坐标的对应关系应该不变，如初始棋盘下，A1总是对应了黑棋，即时你旋转180度后左上角看起来是白棋）。

理论上，客户端收到的 `MOVE_OP` 只会是对方的移动，故无需发送执棋颜色，由服务端维护一个 `QTcpSocket* ` 与 `PieceColor` 的映射关系，并正确转发 `MOVE_OP`。

> 关于服务端的超时判断，我们规定：服务端将 `MOVE_OP` 转发给客户端后开始计时，特别地，开始游戏时是 `READY_OP` 发送给两个客户端后开始计时，如果在规定时间内服务端没有收到 `MOVE_OP`则判断超时，即使此时客户端已经发送了 `MOVE_OP` 但是还没传输到或者还没被服务端处理（所以建议客户端发送留出一点点余量，比如 0.5s，其实校园网的延迟是远低于0.1s的）。
>
> 第一步的超时设定也许意味着，在**比赛**时，如果你将手动下棋设为默认，你可能会因为从接收到服务端的 READY_OP到手动开启托管的手速慢导致超时，你需要避免这个问题，比如在客户端发送 ready 前就设置好托管，或者保证自己的手速够快，或者让 AI 在刚开始时足够快。

### `RESIGN_OP`

认输，替代 `MOVE_OP`，向服务端发送 `RESIGN_OP`，服务端收到后不转发，而是直接进入发送 `END_OP` 的流程。

> 我们规定 `RESIGN_UP` 只能在自己的回合发送，如果在对方回合发送，服务端应该忽略这个请求。

- `data1`: 空
- `data2`: 空
- `data3`: 空

> 无处落子时及时认输才是君子之道

### `END_OP`

`END_OP`表示游戏结束，服务端向双方发送结束信息，客户端在收到后应该立刻停止其他操作，进行结算显示。

这个回复和第一阶段中的 SurakartaMoveResponse 有几乎完全相同的含义，除了超时和投降时不需要提供 move 的信息，以及枚举变量发送的是字符串形式的整数！！！请不要发成枚举变量的名字。

- `data1`: SurakartaIllegalMoveReason，如果 EndReason 是 RESIGN 或 TIMEOUT 等与 move 无关的原因，则此处可为空。
- `data2`: SurakartaEndReason
- `data3`: 获胜方 PieceColor，比如平局则为 `PieceColor::NONE` 对应的枚举变量

这里三个量都回复数字，包括颜色，这和 `READY_OP` 中的不同。

```c++
enum class PieceColor : PieceColorMemoryType {
    BLACK,
    WHITE,
    NONE
};
enum class SurakartaIllegalMoveReason {
    LEGAL,                     // unused
    LEGAL_CAPTURE_MOVE,        // capture a opponent's piece, and the move consists at least one corner loop
    LEGAL_NON_CAPTURE_MOVE,    // just as the name
    ILLIGAL,                   // unused
    NOT_PLAYER_TURN,           // move when it's not the player's turn.
    OUT_OF_BOARD,              // from or to position is out of board
    NOT_PIECE,                 // move a position that is not a piece
    NOT_PLAYER_PIECE,          // move a piece that is not the player's
    ILLIGAL_CAPTURE_MOVE,      // try to capture a opponent's piece, but the move can't consist any corner loop
    ILLIGAL_NON_CAPTURE_MOVE,  // otherwise
    GAME_ALREADY_END,          // unused
    GAME_NOT_START             // unused
};
enum class SurakartaEndReason {
    NONE,          // not end
    STALEMATE,     // both players can't make more move
    CHECKMATE,     // one player's all pieces are captured
    TRAPPED,       // unused, one player's pieces are all trapped, no legal move can be made.
    RESIGN,        // one player resigns.
    TIMEOUT,       // one player's time is out.
    ILLIGAL_MOVE,  // one player makes an illegal move
};
```

### `LEAVE_OP`

任何时候，发送 `LEAVE_OP` 说明即将立刻断开连接，如果在游戏进行时离开，视作投降。

建议在结束离开时发送以告知服务器。游戏中建议正常放弃，即用 `RESIGN_OP`。因为第三阶段只要求实现最小的可支持一局比赛的操作，所以事实上可以不实现这个操作。

- `data1`: 己方用户名（空）
- `data2`: 离开的原因（空）
- `data3`: 空


### `CHAT_OP`

聊天功能，可选择性实现

- `data1`: 己方用户名
- `data2`: 聊天内容
- `data3`: 空
