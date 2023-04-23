# Heuristic-algorithms

一些常用启发式算法的入门尝试，纯小白的入门记录

## 第零章、首先附一些个使用手册

### 1.py39文档

https://docs.python.org/zh-cn/3.9/

好像是官方给的使用手册，常用数据结构也就是列表元组字典，应对GA这种就足够了，更高级的结构一般也不太会用到。

### 2.markdown语法官方文档

https://markdown.com.cn/basic-syntax/

纯菜鸡一个，MD语法用到哪查到哪

### 3. github文档
<https://docs.github.com/zh>不知道有啥用先放着

### 4. git文档
<https://git-scm.com/docs>不知道有啥用先放着

# 第一章 环境配置
1~4节是基于PyCharm和Anaconda的环境配置，5节及以后是基于VScode的环境配置

## 1. pycharm安装

太简单了没啥好说的，pycharm community免费版直接上了

## 2. git安装
这个知乎回答对git安装写的相当详细<https://zhuanlan.zhihu.com/p/607970211>

只挑一点重要的过来记录一下

①记得把主分支的默认名称从master改成main，其他按教程选择就好了，或者直接按默认选项以及安装程序中的”recommended“选项，实验室选项都不选

②git用户名和邮箱与github保持一致

③本地仓库初始化

```
# 用户名和邮箱
git config --global user.name "abcd"
git config --global user.email 123@abc.com

# 检查配置信息 
git config --list

# 初始化仓库
git init

# 添加所有变化
git add .

# commit & push
git commit -m "Input your commit message"

git push origin main
...

```

## 3. git远程链接到github

①本地SSH生成，导入github

②github代码仓库URL链接到本地
```
git remote add origin git@github.com:balabalabalabala.git
```
其中`git@github.com:balabalabalabala.git`这一段是仓库地址

③对于第一次push前远程代码仓库已经非空的操作，首先需要把所有信息pull到本地然后再往远程仓库push

参考这个回答<https://zhuanlan.zhihu.com/p/88246764>

首先从远程拉取

`git pull origin master --allow-unrelated-histories #仅远程非空使用，远程仓库为空可以跳到下一行直接push`

接下来才能push上去：

`git push origin main`

针对非空仓库的关联：为什么不直接git pull origin master呢？是可以的，但是2个不同项目的不同提交记录并没有关联，最后git push origin master是不会成功的。
会出现(non-fast-forward报错)，其根本原因是repository已经存在项目且不是你本人提交（但是git只认地址），你commit的项目和远程repository不一样。

## 4. 新建.gitignore文件配置
直接在pycharm的program里new一个无类型的file，然后命名为`.gitignore`，然后根据提示自动加入git文件
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

## 5. anaconda安装和pycharm编译环境配置

①首先注意一点，默认的envs有可能在C盘不可视文件夹"program data"里面，也有可能在目录“uses/conda.”底下，
找不到了就去这两个地方看。 旧版一般是在programdata下面的，需要“显示隐藏的文件夹”，新版anaconda就默认把虚拟环境文件放在users/conda.下了。
关于这一点还有一个很重要的是【文件修改权限】，如果在program data下的话，有可能users不具有修改权限（需要管理员权限），
所以可能conda install的时候会报错，用conda可视化界面的时候也会报错“multiple errors”，解决方法是右键文件夹，属性，安全，把users的权限勾上。
但在users下面就没有这个问题，只不过在users下会占用C盘空间，而且东一块西一块不方便管理，各有各的好，自行选择。
这一点可以参考链接，里面给了如何修改envs文件夹位置和修改文件夹权限的方法。<https://blog.csdn.net/hshudoudou/article/details/126388686>

②gurobi库与anaconda虚拟环境配置
直接把gurobi的grbpy文件夹复制到虚拟环境的Lib文件夹下面是最简单粗暴高效的也是稳定成功的。conda（或者pip） install日常失灵，不大好用。

③在我用的时候，anaconda新建虚拟环境不能选R语言支持，只能勾选各个版本的python。否则会报错”multiple error(s)“，网上查了查据说可能是因为服务器在海外，是网络错误，
但试了试开clash tun模式并没有解决，不太懂，不过只要不勾选R语言支持就没问题。

## 6. VScode环境配置

# 第二章、GA-FJSP

工件-机器对应如图。对于不可选的机器，设置加工时间为-1

<img width="563" alt="image" src="https://user-images.githubusercontent.com/72543040/230000604-4b49d3bf-e4ac-4c4b-b91f-583888995d5b.png">
