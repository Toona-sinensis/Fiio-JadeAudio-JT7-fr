# 飞傲翡声 JT7 频响曲线数据 / Frequency Response Data

从公开频响曲线图数字化的 **飞傲翡声 JT7**（头戴式平板耳机）频率响应数据，可直接导入
REW、AutoEQ、VituixCAD、squig.link 等工具。

Digitized frequency response data for the **FiiO / Jade Audio JT7** planar magnetic
headphone, ready to import into REW, AutoEQ, VituixCAD or squig.link.

---

## 数据来源 / Source

| 项目 | 内容 |
|---|---|
| 产品 | 飞傲翡声 JT7（参考售价 699 元） |
| 测试设备 | B&K 5128 人工耳 |
| 补偿曲线 | JM-1 DF Target（即图中的 `JM-1 DF(B_8dB,T_-4dB)`） |
| 原始出处 | 哔哩哔哩 UP主 **A子如是说** |
| 视频 | [【A子】推荐评级：S，ChiFi供应链的奇迹之声。 —— FIIO 翡声 JT7](https://www.bilibili.com/video/BV1Y31UBuE7K) |
| 原始图表 | [`source/chart.png`](source/chart.png) 等三张（见下） |

**本仓库的数据是本人从上述视频中的频响曲线图逐像素数字化的结果，并非原始测量文件。**
原始测量与图表版权归原 UP主所有；如果你需要权威数据，请以原始视频为准。

This data was digitized by hand (per-pixel) from the charts in the source video.
It is not the original measurement file. The measurement and charts remain the
property of the original creator.

视频中共有三张 JT7 曲线图，分别与不同耳机对比，三者画的是同一条 JT7 实测曲线：

| 文件 | 对比对象 |
|---|---|
| `source/chart.png` | JM-1 DF Target / Diffuse Field Response |
| `source/chart_2_editionxs.png` | HIFIMAN Edition XS |
| `source/chart_3_ft1pro.png` | 飞傲 FT1Pro |

---

## 文件说明 / Files

```
data/
  JT7_BK5128_1-24oct.csv      1/24 倍频程，240 点（推荐使用）
  JT7_BK5128_raw.csv          像素级原始分辨率，1338 点（未平滑）
  JT7_BK5128_normalized.csv   以 1 kHz 归零
  JT7_BK5128.frd              REW / ARTA / VituixCAD 导入格式
  JT7_BK5128_REW.txt          REW 文本导入（制表符分隔）
plots/
  JT7_BK5128_response.png     曲线总览（绝对 SPL + 归一化两个视图）
verification/
  JT7_BK5128_extraction_check.png   提取轨迹叠加在三张原图上的验证图
source/
  chart.png                   原始曲线图（vs JM-1/DFR）
  chart_2_editionxs.png       原始曲线图（vs Edition XS）
  chart_3_ft1pro.png          原始曲线图（vs FT1Pro）
digitize.py                   数字化脚本，可复现全部数据
make_figures.py               生成总览图与验证图
```

### CSV 格式

两列，带表头，逗号分隔：

```csv
frequency,spl
20.00,-7.38
20.59,-7.16
21.19,-6.82
```

请按纯文本导入，不要对首行做数值解析。

---

## 主要数据特征 / Highlights

以 1 kHz 归一后（dB 相对 1 kHz）：

- **低频**：50 Hz 附近有约 +1.5 dB 的小幅抬高，80 Hz 回到 0 dB，20 Hz 处滚降至 −7.2 dB
- **中频**：200 Hz – 1 kHz 非常平直，全程在 −0.9 至 +0.9 dB 之间
- **耳道增益峰**：3.13 kHz 达到 **+12.9 dB**，是全频最高点
- **随后的凹陷**：4.83 kHz 回落至 **+3.6 dB**，谷深约 9 dB
- **二次高峰**：6 kHz 回升至 +11.3 dB，其后 8 kHz +6.4 dB、10 kHz +4.2 dB
- **极高频**：10 kHz 后快速滚降，12 kHz 到 −1.2 dB，20 kHz 至 −17.5 dB

中频平直加上突出的 3 kHz 耳道增益峰、以及 5 kHz 附近的深谷，是这个型号最显著的形态特征。
注意这不是平滑的扩散场响应。

---

## 精度说明 / Accuracy

- **坐标标定**：三张图的绘图区均为 1339×573 px，横轴 20 Hz–20 kHz（三个十倍频程），
  纵轴 +25 dB–−25 dB 线性。刻度与图内网格线逐条核对，残差在 1 px 以内
- **提取方式**：按颜色掩膜分离红色实测曲线，按列连续性追踪，剔除图例色块与对比曲线干扰
- **精度估计**：受曲线线宽与抗锯齿影响，约 **±0.3 dB**（100 Hz–8 kHz），
  15 kHz 以上曲线近垂直处误差更大
- **Y 轴含义**：图中纵轴是相对显示刻度，**不是校准后的绝对声压级**；引用时请注明归一化基准
- **相位**：原图无相位信息，`.frd` 文件中相位列全部填 0

### 单声道说明

三张源图各自只画了**一条** JT7 曲线，因此本数据是**单声道**结果，不含左右声道差异信息。
（另一个来源的 squig.link 曲线虽有 L/R 双线，但与本仓库数据不是同一测量，故未采用。）

### 关于对比曲线遮挡

第三张图（`chart_3_ft1pro.png`）中，蓝色 FT1Pro 曲线在部分频段几乎完全覆盖红色 JT7 曲线，
该处像素上不留红线痕迹，因此该图无法提供这些区间的数据。实际提取到的断点如下：

| 图 | 断点区间 |
|---|---|
| `chart.png` | 无 |
| `chart_2_editionxs.png` | 70–78 Hz、2860–3426 Hz |
| `chart_3_ft1pro.png` | 36–38 Hz、74–82 Hz、136–281 Hz（多段）、418–461 Hz、675–787 Hz、2935–3391 Hz、3702–4020 Hz |

平均值在每一频点只使用实际覆盖到该点的图，因此不影响完整覆盖。

### 多源交叉验证

三张图独立数字化后，以 1 kHz 归一逐点比较：

| 对比 | 归一化差异 RMS | 极值 |
|---|---|---|
| chart vs chart_2 | 0.09 dB | ±0.66 dB |
| chart vs chart_3 | 0.10 dB | ±1.34 dB |
| chart_2 vs chart_3 | 0.08 dB | ±1.26 dB |

三者在同一形状上收敛，说明数字化结果可靠。三张图在图表中的**纵向位置**相差约 1.1 dB，
这是截图排版差异而非数据差异，故先按 1 kHz 对齐再取平均。

验证图 [`verification/`](verification/) 中的青色描线叠加在原曲线上，可与原图逐点比对。

### 频响范围

横轴两端均为 20 Hz 与 20 kHz，数据完整覆盖该范围。

---

## 复现 / Reproduce

```bash
pip install pillow numpy matplotlib
python digitize.py 24oct      > data/JT7_BK5128_1-24oct.csv
python digitize.py normalized > data/JT7_BK5128_normalized.csv
python digitize.py raw        > data/JT7_BK5128_raw.csv
python digitize.py frd        > data/JT7_BK5128.frd
python digitize.py rew        > data/JT7_BK5128_REW.txt
python make_figures.py
```

脚本从 `source/` 读取图像，把结果输出到标准输出，由 shell 重定向写入，
自身不打开任何文件用于写入。已确认重跑结果与仓库中的数据逐点一致。

---

## 许可证 / License

- **数字化脚本与仓库整理工作**：[MIT](LICENSE)（代码部分）
- **曲线数据本身**：建议按 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
  使用，转载或二次发布时请注明原始测量来源（UP主 A子如是说）与本仓库

---

## 免责声明 / Disclaimer

本数据仅供个人学习、EQ 调试与技术交流使用。数字化的过程不可避免地引入误差，
不适合作为产品验收、退换货或商业宣传的依据。
