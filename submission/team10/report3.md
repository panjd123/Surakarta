## Team10 第三阶段报告

### Upd

- 于 5.19 18:26 进行了与 Team04 程序的测试，应该可以顺利交互

- 于 5.22 下午进行了重构，在功能不变的前提下，server 精简为 1591 行，client 精简为 1310 行

- 于 5.22 下午完成了**附加任务2：重放功能**（Replay Engine），支持播放，暂停，上一步，下一步，支持选择 `log` 保存目录

### 前言

- 该报告撰写于5.19日下午，可能未包含部分开发内容，但是涵盖了小组在第三阶段的绝大部分开发内容

- 我们将在项目全部完成后，即最终报告中来更详细地介绍整个项目的设计，因为绘制流程图等环节比较耗时，所以我们在第三阶段报告中只介绍阶段性成果

### 我们完成了什么？

1. 我们实现了 **AI 的随时托管**. 通过勾选框，可以随时开始与停止 AI 托管.

2. 从上一阶段开始，我们就已经采用了 **server-client 双架构**，具体请见 [CoderBak/Surakarta-client](https://github.com/CoderBak/Surakarta-client) 与 [CoderBak/Surakarta-server](https://github.com/CoderBak/Surakarta-server) .

3. 我们支持**移动提示**. 在属于玩家的轮次，玩家可以点击自己的棋子. 点击后棋子将高亮，同时我们将使用两种不同的颜色来高亮玩家可以移动的位置与可以旋吃的所有棋子.

4. 我们支持了**计时功能**. 我们将计时数据从 server 转发到双方 client ，同时添加了超时认输逻辑.

5. 我们会显示**结算信息**. 游戏结束后，server 端将输出结算信息，后期我们将传送结算信息给 client 并输出到文本框

6. 我们实现了**行棋记录与日志系统**. 我们通过 `utils/logger.h` 可以随时记录想要留存的日志信息.

7. 我们实现了**移动动画**. 在点击高亮提示的旋吃子后，我们将高亮整个绕行轨道，同时将棋子绕轨道展示旋吃动画（我们实现了绕旋线的动画，而不是直接闪现）.

8. 我们实现了**濒死提示**. 玩家只能在自己的轮次点击棋子，并且只能移动到我们高亮提示的位置（即：可移动区域与可旋吃子），从而禁止了玩家走会输的步.

9. 我们实现了**任意路数棋盘**. 我们的整套代码是灵活可变的. 通过杜绝所有的 `magic number` （即：出现在代码中的各种常量，例如大量未知含义的数字），我们将所有常量定义在一个文件里. 例如，只要修改一个 `BOARD_SIZE` 常量，我们的整套游戏，从动画到规则判断，都会支持任意（偶数）大小的棋盘. 我们已经在 `8x8` 与 `10x10` 上测试了游戏效果.

10. 我们实现了**联机再来一局**. 在属于玩家的轮次，玩家可以通过点击 Retry 重新开始一局.

11. 我们实现了**主菜单与设置菜单**. 通过设置菜单，可以调整游戏常量，例如 `BOARD_SIZE`.

我们还完成了以下的**附加任务**：

1.  我们完成了**附加任务1: 棋子移动动画（含外旋线）**.

2.  我们完成了**附加任务4: 联机再来一局**.

3.  我们部分完成了**附加任务6: 服务器端 GUI**. 在服务器端我们会显示一个小的棋盘，用来展示当前对局. （最终我们将补上随时开关棋盘显示的功能）

### 小组分工

总体上来说，小组在整个开发中密切合作，使得每个人的工作量较为平均，三个组员都得到了充分的锻炼.

孙浩翔 (GitHub: CoderBak)：

- 负责完成 Surakarta-server-demo 与 Surakarta-client-demo，即提供给助教测试的无 GUI 简易程序

- 负责完善棋子动画与提示逻辑，包括：濒死提示、高亮提示、旋吃动画、路线高亮

- 负责完成再来一局功能

- 完善了 server 端的 GUI 界面

- 为游戏实现了随时的 AI 接入，即随时开始接管，随时停止接管

- 为游戏添加了日志系统，便于将日志保存在本地（后期将利用日志系统提供回放）

- 报告撰写

王燚 (GitHub: smallsmallprogrammer)：

- 负责在 Windows 平台打包了 Surakarta-server-demo 与 Surakarta-client-demo，即我们的提交内容，并发布了 [Surakarta-client-demo-v1.1](https://github.com/CoderBak/Surakarta-client-demo/releases/tag/v1.1) 与 [Surakarta-server-demo-v1.1](https://github.com/CoderBak/Surakarta-server-demo/releases/tag/v1.1)

- 开发了第一版棋子动画，包括：选中特效

- 为游戏界面添加了按钮、AI托管选项等组件

- 为游戏添加了主菜单，设置等选项

张昕跃 (GitHub: imio21777)：

- 为 server 与 client 加入了计时器，包括：整局游戏时间计时与每一步的计时

- 增加了 timeout 逻辑

- 为 server 初步增加了 GUI 界面

- 完善了游戏的“开始按钮”

- 正在开发：后端与绘制的异步

### 大致架构

我们采用 server 与 client 分离的设计. 两者之间通过 TCP Socket 实现信息交换.

#### Surakarta-server

Surakarta-server 的基本架构

```
Surakarta-server
├── CMakeLists.txt
├── board_ui.h
├── common.h
├── main.cpp
├── mainwindow.cpp
├── mainwindow.h
├── mainwindow.ui
├── server.cpp
├── server.h
├── surakarta
│   ├── agent
│   │   ├── agent_base.h
│   │   ├── agent_random.cpp
│   │   └── agent_random.h
│   ├── basic.h
│   ├── board.h
│   ├── game.cpp
│   ├── game.h
│   ├── piece.h
│   ├── reason.cpp
│   ├── reason.h
│   ├── rule_manager.cpp
│   └── rule_manager.h
├── timer.h
└── utils
    ├── global_random_generator.h
    └── logger.h
```

在 Surakarta-server 中，我们主要实现了与两个 client 的连接与规则的判断.

#### Surakarta-client

Surakarta-client 的基本架构

```
Surakarta-client
├── CMakeLists.txt
├── board_utils.h
├── image
│   ├── 22.jpg
│   ├── background-removed.png
│   └── start_button.jpg
├── main.cpp
├── mainwindow.cpp
├── mainwindow.h
├── mainwindow.ui
├── resources.qrc
├── settings.cpp
├── settings.h
├── startmenu.cpp
├── startmenu.h
└── startmenu.ui
```

Surakarta-client 主要负责与服务器端连接，并且将信息显示到 GUI 上.

#### server 与 client 的协作

（这里和上一个阶段报告一致）具体来说，我们让 server 在 boardUpdated 的时候，将棋盘发送给 client . client 处理 board 的显示，捕捉鼠标点击信号，将移动信息再次发送给 server. server 端负责游戏的判定.

在实现过程中遇到了 TCP 的粘包问题，具体解决方法就是添加分隔符. 具体可以见代码实现.

### 设计亮点

I. client 与 server 的分离设计，使得 server 可以独立部署在服务器上.

II. 合理的设计

- 我们将所有常量打包在 `common.h` 里面，例如服务器端口，`BOARD_SIZE`，棋子半径等等，实现了参数与代码完全分离，避免代码中大量 `magic number` 的出现.

- 使用信号槽来在类、控件之间交换数据

- 充分的代码注释

- 明确的文件结构，没有将全部源文件放到一个文件夹下

III. const correctness 的充分保障

在所有应该使用 const 声明的位置均使用了 const 声明，保证了程序的 const correctness

IV. C++ 新特性的充分使用

在编程过程中使用各种语法糖和新特性，例如 auto binding (since C++17) ，lambda function (since C++11) ，auto (since C++11) ，for-each loop (since C++11) ，if with initializer (since C++17) 来大幅增强代码可读性和简洁程度

V. 代码风格统一化

代码由小组成员共同完成，CoderBak 规定了必要的代码规范，例如驼峰命名法，使得代码可读性更强

VI. 更精简的架构

在使用 `clang-tidy` 和限制一行代码长度的情况下，目前 `Surakarta-server` ~~仅~~ `2062` 行代码，`Surakarta-client` ~~仅~~ `1412` 行代码，~~组员们五一还出去玩耍了，没有卷（大雾）~~

VII. ~~在 5.19 中午提交了 demo 代码到网盘，没有咕咕咕~~
