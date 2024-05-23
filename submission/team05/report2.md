# 第二阶段报告

- 类的关系

  class SurakartaBoard里引用了SurakartaPosition和SurakartaPiece的成员

  class SurakartaGame引用了SurakartaBoard，SurakartaGameInfo和SurakartaRuleManager的成员

  class SurakartaRuleManager引用了SurakartaBoard和SurakartaGameInfo的成员

  

- 超时和认输功能：

  1.超时判断：在game的头文件里定义两个Qtimer变量，分别为黑棋和白棋的回合计时。如果超时就调用messagebox弹出来显示下棋超时，游戏结束。

      QTimer* blackTimerId;               // 黑方定时器
      QTimer* whiteTimerId;               // 白方定时器
  2.认输：在界面加一个认输的按钮，点击后会调用messagebox显示玩家认输，游戏结束。

      pushButton2 = new QPushButton(Widget);
      pushButton2->setObjectName("pushButton2");
      QObject::connect(pushButton2, &QPushButton::clicked, &Ui_Widget::resign);

- 困难：

  有不同的文件，很多class, 所以一开始不熟悉的时候写的很慢，要不断去翻不同文件去找class的成员。



- 小组分工：

刘承枭：画棋盘和棋子，本地轮流移子功能，类的完善。

陈雪欣：超时和认输功能。

赵怡瑾：“再来一局”功能。