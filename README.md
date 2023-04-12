# Heuristic-algorithms

一些常用启发式算法的入门尝试，纯小白的入门记录

# 第零章、首先附一些个使用手册。。

## 1.py39文档

https://docs.python.org/zh-cn/3.9/

好像是官方给的使用手册，常用数据结构也就是列表元组字典，应对GA这种就足够了，更高级的结构一般也不太会用到。

## 2.markdown语法官方文档

https://markdown.com.cn/basic-syntax/

纯菜鸡一个，MD语法用到哪查到哪

# 第一章 环境配置
1~5节是基于PyCharm和Anaconda的环境配置，6节及以后是基于VScode的环境配置

## 1. pycharm安装

太简单了没啥好说的，pycharm community免费版直接上了

## 2. git安装
这个知乎回答对git安装写的相当详细<https://www.zhihu.com/search?type=content&q=git%E5%AE%89%E8%A3%85>

只挑一点重要的过来记录一下

①记得把主分支的默认名称从master改成main，其他按教程选择就好了，或者直接按默认选项以及安装程序中的”recommended“选项，实验室选项都不选

②git用户名和邮箱与github保持一致

## 3. git远程链接到github

①本地SSH生成，导入github

②github代码仓库URL链接到本地

③对于第一次push前远程代码仓库已经非空的操作，首先需要把所有信息pull到本地然后再往远程仓库push,参考这个回答<https://zhuanlan.zhihu.com/p/88246764>

`git pull origin master --allow-unrelated-histories`

④.gitignore文件配置
```
##ignore this file##
/target/
/.idea/
/.settings/
/.vscode/
/bin/

.classpath
.project
.settings
.idea
 ##filter databfile、sln file##
*.mdb
*.ldb
*.sln
##class file##
*.com
*.class
*.dll
*.exe
*.o
*.so
# compression file
*.7z
*.dmg
*.gzx
*.iso
*.jar
*.rar
*.tar
*.zip
*.via
*.tmp
*.err
*.log
*.iml
# OS generated files #
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
Icon?
ehthumbs.db
Thumbs.db
.factorypath
/.mvn/
/mvnw.cmd
/mvnw
```

## 4. anaconda安装和pycharm编译环境配置

①首先注意一点，默认的envs有可能在C盘不可视文件夹"program data"里面，也有可能在目录“uses/conda.”底下，
找不到了就去这两个地方看。 旧版一般是在programdata下面的，需要“显示隐藏的文件夹”，新版anaconda就默认把虚拟环境文件放在users/conda.下了

②gurobi库与anaconda虚拟环境配置
直接把gurobi的grbpy文件夹复制到虚拟环境的Lib文件夹下面是最简单粗暴高效的也是稳定成功的。conda（或者pip） install日常失灵，不大好用。

# 5. VScode环境配置

# 第二章、GA-FJSP

工件-机器对应如图。对于不可选的机器，设置加工时间为-1

<img width="563" alt="image" src="https://user-images.githubusercontent.com/72543040/230000604-4b49d3bf-e4ac-4c4b-b91f-583888995d5b.png">
