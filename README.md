# Lin - Use TUI style to manage files!

![image](https://github.com/Mrwu87/Lin/blob/master/linsc.png)

### [Lin](https://github.com/Mrwu87/Lin) 一个文件管理终端UI工具，为了让使用者能更快捷的操作终端文件。秉承快捷实用的原则，设置了多个快捷键可做一系列的操作，开始时可能会感到不习惯使用随着使用次数增多，相信你会喜欢它所带来的效率提升


## 语言
####  &nbsp; &nbsp;[中文](README.md) &nbsp; [English](Eng_readme.md)

## 特点

1. 一键复制文件内容

2. 一键备份文件

3. 自动解压多个文件/文件夹

4. 压缩多个文件/文件夹

5. 图形化展示文件列表

6. 支持增删移查文件内容

7. 实时查看文件变更

8. 终端页面

9. 复制/剪切多个文件/文件夹

10. 筛选文件/文件夹功能

11. cpu 使用检测

12. 内存使用检测

   ...............

## 即将上线功能
- 文件、文件夹修改权限
- 远程传输文件功能 远程拷贝文件
- 自动识别后缀运行程序
- 文件内容替换、筛选
- 支持鼠标点选功能
- 全局查找文件
- ......
## 快捷键


| Action | Command |
|--------|---------|
|   选中文件/文件夹     |     space            |  
|   撤销选中文件     |    ctrl esc     |  
|   剪切选中文件/文件夹     |    X     |
|   刷新页面     |   ctrl r      |
|   复制文件内容     |  A     |
|    退出工具    |   ctrl w   |
|   召唤终端    |    ctrl t     |
|   退出终端     |  ctrl q       |
|   创建文件   |   ctrl n      |
|   删除选中文件/文件夹     |   ctrl d      |
|    跳转目录    |    O     |  
|   粘贴选中文件    |  V     |  
|  进入文件/文件夹     |   enter      |  
|     回退目录   |   esc    |  
|     备份文件   |   B    | 
|     压缩选中文件/文件夹   |   Z    | 
|     解压缩文件    |   U   | 
|     查看实时变化   |   T   | 
|     详细查看文件内容   |   L   | 

---

## 安装依赖包(可选)
#### pip install -r requirements.txt
## 运行程序

#### python3 Lin.py
## 配置文件(可选)

#### 编辑setting.yaml

```
editor: vi        #设定打开文件的编辑器
mouse: false      #开启鼠标模式（注意：这里开启之后就无法选取文字）
short_key:        #快捷键设置
  cut: X
  refresh: ctrl r
  copyContent: A
  quitDestop: ctrl w
  term: ctrl t
  quitTerm: ctrl q
  createFile: ctrl n
  deleteFile: ctrl d
  copyFile: C
  pasteFile: V
  goTo: O
  selectedFile: ' '
  cancelSelected: ctrl esc
  backdir: esc
  backUpfile: B
  zip: Z
  unzip: U
  tail: T
  less: L

```


## 皮肤
#### 暂未上线

