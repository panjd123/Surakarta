## CMake 简易教程
____
### 什么是CMake
> CMake is the de-facto standard for building C++ code, with over 2 million downloads a month. It’s a powerful, comprehensive solution for managing the software build process

以上摘自CMake官网文档

简单来说，CMake是一种跨平台的C++项目构建工具。通过`CMakeLists.txt`指定构建项目规则，包括但不限于对第三方库的加载与链接，头文件目录的引入等等。用户只需要编写`CMakeLists.txt`， CMake 就可以为项目生成`.ninja`或`.makefile`文件，作为生成器的`ninja`与`make`据此对项目进行编译。
____
### CMake下载
[CMake官网地址](https://cmake.org/)

Windows环境下CMake下载与环境变量配置教程不胜枚举，例如[这篇博客](https://blog.csdn.net/didi_ya/article/details/123029415)，大家可以善用搜索引擎自行查阅。
环境变量配置完成后，在Windows命令行输入`cmake --version`
若终端输出cmake版本信息，即为配置成功。
____
### CMake基本命令
- 指定项目CMake最低版本
  ```CMake
  cmake_minimum_required(VERSION 3.5)
  ```
- 设定C++标准并要求编译器支持此标准
  ```CMake
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  ```
- 设定项目名称，版本与编程语言
  ```CMake
  project(Demo1 VERSION 1.0 LANGUAGES CXX)
  ```
  后续对变量`PROJECT_NAME`取值即可获得项目名`Demo1`
  对变量`value`取值操作为`${value}`
- 生成可执行文件
  ```CMake
  add_executable(Demo1 main.cpp)
  ```
  `Demo1`为可执行文件名称，`main.cpp`为可执行文件相关源文件
  如果需要添加多个源文件
  ```CMake
  add_executable(Demo1 main.cpp mainwindow.cpp ...)
  ```
  或者
  ```CMake
  set(PROJECT_SOURCES
        main.cpp
        mainwindow.cpp
        ...
    )
  add_executable(${PROJECT_NAME}, ${PROJECT_SOURCES})
  ```
- 引入外部依赖库
  ```CMake
  find_package(<package> [version] [EXACT] [QUIET] [MODULE]
             [REQUIRED] [[COMPONENTS] [components...]]
             [OPTIONAL_COMPONENTS components...]
             [NO_POLICY_SCOPE])
  ```
  - `package`为必填参数，为需要查找的包名称
  - `version`为可选参数，指定包的版本
  - `EXACT`关键字若被指定，表示查找版本必须完全与指定版本相同而非兼容即可
  - `REQUIRED`关键字若被指定，表示该第三方库为必需，若查找失败 CMake 停止执行
  - `COMPONENTS`关键字若被指定，表示查到的库中必须包含全部`[components...]`，否则 CMake 停止执行
  
    以 QT 库为例
    ```CMake
    find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
    find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)
    ```
    第一行`find_oackage`，`NAMES`关键字指定顺序查找`Qt6`与`Qt5`，且必须包含`Widgets`组件，查找到的 QT 版本赋值给变量 `QT_VERSION_MAJOR`
    第二行`find_package`根据查找到的版本引用具体模块
- 链接库
  ```CMake
  target_link_libraries(${PROJECT_NAME} PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)
  ```
  将`find_package`引入的模块链接到具体的子项目
  - `PRIVATE`为指定链接权限的关键字，意为本目标，即`${PROJECT_NAME}`链接了库`Qt${QT_VERSION_MAJOR}::Widgets`，但其他链接到`${PROJECT_NAME}`的目标并**不会**继承链接该库
  - `PUBLIC` 当前目标链接了外部库，且其他目标链接到当前目标时会继承该库
  - `INTERFACE` 当前目标并未链接外部库，仅仅导出了符号，当其他目标链接到当前目标时链接该库
特别地，如果需要在 Qt CMake 项目中引入其他模块例如`Network`，需要在 CMakeLists 中进行如上配置，另外注意链接库指令应当在生成可执行文件后
- 其他配置
在 Qt CMake 项目中，往往需要如下配置
```CMake
set(CMAKE_AUTOUIC ON) #自动处理ui文件
set(CMAKE_AUTOMOC ON) #自动处理信号槽
set(CMAKE_AUTORCC ON) #自动处理qrc资源文件
```
___
### 生成器的选择
Windows 系统默认采用`Visual Studio 2019`生成器，考虑到本课程大作业的项目规模与构建速度要求，推荐各位使用`ninja`生成器。
Windows 系统下可以使用 Python 包管理器安装 ninja
`pip install ninja`
或者你也可以拉取 [git 仓库](https://github.com/ninja-build/ninja) 手动安装，可以用`Python`构建，也可以用`CMake`
在命令行输入`ninja --version`可检查`ninja`是否已安装

___
### End
本教程的目的是在短时间内阐释最简单的 Qt CMake 项目配置，之于 CMake 技术仅仅是冰山一角，鼓励同学们进一步自主学习以熟练掌握 CMake 技术。

[CMake 官方文档](https://cmake.org/documentation/)

[一些不错的中文教程](https://zhuanlan.zhihu.com/p/500002865)
