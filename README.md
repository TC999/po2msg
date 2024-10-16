# po2msg
git专用po语言文件转msg，使用python编写

## 为什么要重写？

用于单独生成 git-for-windows 语言包的脚本，原版po2msg.sh文件过于复杂，且只能在linux下运行（还一直报错），故使用python重写

## 使用方法

安装 python 3.8

克隆此仓库
```git
git clone https://github.com/TC999/po2msg.git
```

安装依赖
```pip
pip install polib
```

使用方法
```python
python main.py <xx_xx.po> <xx_xx.msg>
```
> [!note]
>
> 文件名不能乱改，必须是语言编码，例如`zh_cn.po`、`zh_tw.po`、`en_us.po`等

## 报告BUG：
[GitHub 议题](https://github.com/TC999/po2msg/issues)