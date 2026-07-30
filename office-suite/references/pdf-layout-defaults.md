# 技术文档默认排版参考

来源：`templet.pdf`（西安电子科技大学硕士论文模板）实测值。
**所有生成的技术文档以此为默认排版**，除非用户另有指定。

## 页面与边距

| 参数 | 值 |
|------|----|
| 页面 | A4（595.28 × 841.89 pt） |
| 左边距 | 85 pt |
| 右边距 | 71 pt |
| 上边距 | 90 pt |
| 下边距 | 55 pt |
| 文字区宽度 | 439 pt |

## 页眉 / 页脚

- **页眉**：文档标题居中，9pt；正下方双细黑线（0.5pt），位于 `PAGE_H-78` 和 `PAGE_H-80`
- **页脚**：细黑线（0.5pt）位于 `BOTTOM+14pt`，页码居中于线下

## 字体

| 用途 | 字体 | 大小 | 对齐 |
|------|------|------|------|
| 章节标题（H1） | DocSerifB（粗体） | 16pt | 居中 |
| 小节标题（H2） | DocSerifB（粗体） | 13pt | 左对齐 |
| 正文 | DocSerif | 12pt，行距 20pt | 两端对齐 |
| 图表说明（caption） | DocSerif | 10pt | 居中 |
| 代码块 | Courier | 9pt，行距 13pt | 左对齐，背景 #F4F4F4 |
| 页眉/页脚 | DocSerif | 9pt | — |

**字体注册方式**（FreeSerif 系列）：
```python
pdfmetrics.registerFont(TTFont('DocSerif',  '/usr/share/fonts/opentype/freefont/FreeSerif.otf'))
pdfmetrics.registerFont(TTFont('DocSerifB', '/usr/share/fonts/opentype/freefont/FreeSerifBold.otf'))
pdfmetrics.registerFont(TTFont('DocSerifI', '/usr/share/fonts/opentype/freefont/FreeSerifItalic.otf'))
pdfmetrics.registerFontFamily('DocSerif',
    normal='DocSerif', bold='DocSerifB', italic='DocSerifI', boldItalic='DocSerifI')
# 务必用 registerFontFamily()，不要用 addMapping()
```
备用（无 FreeSerif 时）：`Times-Roman / Times-Bold / Times-Italic`

## 颜色

**纯黑，不加任何色彩。** 不得使用蓝色、彩色页眉、彩色表头等。

## 表格

- 0.5pt 黑色单线网格，无填充色
- 表头行重复（`repeatRows=1`）
- 表格说明（caption）置于表格**正下方**，居中 10pt

## 数学公式

- 用两列 `Table([公式文本, 编号])` 实现居中公式 + 右对齐编号
- 下标/上标：必须用 `<sub>` / `<super>` XML 标签，**禁止使用 Unicode 下标字符**（₂ ² 等会渲染为黑块）

## 图片

- 用 matplotlib 生成，`dpi=150`，`facecolor='white'`
- 图片说明（caption）置于图片**正下方**，居中 10pt

## 封面

- 上下各一组双粗黑线（2pt）
- 无色彩色块

## 目录

- 使用 `reportlab.platypus.tableofcontents.TableOfContents`
- 必须用 `doc.multiBuild(story)` 两遍构建以生成正确页码

## 模板脚本

`pdf_template.py`（本目录下）— 新文档直接基于此脚本修改内容，无需重新推导排版。
