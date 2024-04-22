## Team10 第二阶段报告

### 小组分工

孙浩翔 (CoderBak)：

- 负责完成第一版 Surakarta-Qt (已废弃) ，主要包含棋盘设计

- 负责完成 Surakarta-server 和 Surakarta-client 的架构设计

- 负责完成 Surakarta-server 和 Surakarta-client 的基本框架 (无 GUI 界面)

- 发布 Surakarta-server v0.1 ，并部署在个人服务器上

- 报告撰写

王燚 (smallsmallprogrammer)：

- 在 Surakarta-client 中实现了棋盘与棋子的绘制与鼠标点击逻辑

- 进一步完善了 socket 的信息传输

张昕跃 (imio21777)：

- 合作完成了第一版 Surakarta-Qt (已废弃)

- 将第一版的大部分功能迁移到 Surakarta-client 上

- 进一步完善了 socket 的信息传输

### 大致架构

我们采用 server 与 client 分离的设计. 两者之间通过 TCP Socket 实现信息交换.

#### Surakarta-server

Surakarta-server 的基本架构

```
Surakarta-server
├── CMakeLists.txt
├── common.h
├── main.cpp
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
└── utils
    └── global_random_generator.h
```

在 Surakarta-server 中，我们主要实现了与两个 client 的连接与规则的判断.

#### Surakarta-client

Surakarta-client 的基本架构

```
Surakarta-client
├── CMakeLists.txt
├── board_utils.h
├── main.cpp
├── mainwindow.cpp
├── mainwindow.h
└── mainwindow.ui
```

Surakarta-client 主要负责与服务器端连接，并且将信息显示到 GUI 上.

#### server 与 client 的协作

具体来说，我们让 server 在 boardUpdated 的时候，将棋盘发送给 client . client 处理 board 的显示，捕捉鼠标点击信号，将移动信息再次发送给 server. server 端负责游戏的判定.

在实现过程中遇到了 TCP 的粘包问题，具体解决方法就是添加分隔符. 具体可以见代码实现.

### 实现效果

目前主要完成了以下的几个任务：

- client 可以与 server 通信. server 目前支持一对玩家的对弈.

- client 棋盘可点击. 点击有选中特效.

- 下棋方有权限进行重来一局的操作，目前的效果是，在按下 Retry 后，两边不需要重新连接，游戏自动重置，随机分配玩家.

- 任意 `board_size` . 通过修改一个数值，即可修改全局 `board_size` ，不会引发任何问题. 所以我们的演示将使用 `10x10` 棋盘进行.

- 发布了 server v0.1 的开箱即用版本. 通过将所有需要的 Qt 库打包，我们发布了可以在没有安装 Qt 框架的 Linux 系统上运行的 server 程序 (约 `23 MB`). 目前已经 `7x24` 运行在 CoderBak 的 Ubuntu 22.04 服务器上. 具体请见 [Server-release v0.1](https://github.com/CoderBak/Surakarta-server/releases/tag/v0.1) .

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

V. 内存更加安全

例如，当一个 client 失去连接时，server 再次发送信息可能会导致未定义行为，我们采用如下的方式来处理 socket 的断开

```cpp
connect(client1, &QTcpSocket::disconnected, this, &Server::socketDisconnected1);
connect(client2, &QTcpSocket::disconnected, this, &Server::socketDisconnected2);

void Server::socketDisconnected1() {
    if (client1) {
        qDebug() << "Game stopped because client 1 stopped";
    }
    socketDisconnected();
}

void Server::socketDisconnected2() {
    if (client2) {
        qDebug() << "Game stopped because client 2 stopped";
    }
    socketDisconnected();
}

void Server::socketDisconnected() {
    if (client1) {
        qDebug() << "Client 1 stopped.";
        client1->deleteLater();
        client1 = nullptr;
    }
    if (client2) {
        qDebug() << "Client 2 stopped.";
        client2->deleteLater();
        client2 = nullptr;
    }
}
```

这样只要有一个 client 断开，游戏自动结束，server 恢复到监听状态.

VI. 代码风格统一化

代码由小组成员共同完成，CoderBak 规定了必要的代码规范，例如驼峰命名法，使得代码可读性更强


### 附注

- 网络传输目前使用的是原生 TCP Socket Server ，之后会迁移到助教提供的网络接口上.
