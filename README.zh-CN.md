<p align="center">
  <a href="https://doi.org/10.5281/zenodo.23629681"><img src="assets/hero.svg" alt="The Arithmetic Topos — 五卷与附录环绕整体算术曲线 𝔛_ℤ 的 D6 蜂巢" width="100%"></a>
</p>

<p align="center">
  <a href="https://doi.org/10.5281/zenodo.23629681"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.23629681.svg" alt="DOI"></a>
  <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.zh-hans"><img src="https://img.shields.io/badge/license-CC%20BY--NC--ND%204.0-0A131E?style=flat" alt="许可：CC BY-NC-ND 4.0"></a>
  <a href="code/LICENSE"><img src="https://img.shields.io/badge/code-Apache%202.0-0A131E?style=flat" alt="代码：Apache 2.0"></a>
  <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/tag/v1.0.0"><img src="https://img.shields.io/badge/release-1.0.0-1E5A88?style=flat" alt="版本 1.0.0"></a>
  <img src="https://img.shields.io/badge/pages-2%2C001-536372?style=flat" alt="2,001 页">
  <img src="https://img.shields.io/badge/ledger-111%20items%20%C2%B7%2053%20conjectures-536372?style=flat" alt="台账 111 项，其中 53 项猜想">
  <img src="https://img.shields.io/badge/series-07-536372?style=flat" alt="系列 07">
  <a href="VERIFY.md"><img src="https://img.shields.io/badge/OpenPGP-signed-B8913B?style=flat" alt="OpenPGP 签名"></a>
  <a href="VERIFY.md"><img src="https://img.shields.io/badge/timestamps-RFC%203161%20%C2%B7%20Bitcoin-B8913B?style=flat" alt="RFC 3161 与比特币时间戳"></a>
</p>

<p align="center">
  <b><a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Preview.pdf">阅读预览版</a></b>（283 页，72.9 MB）·
  <a href="#下载">下载</a> ·
  <a href="#五卷">五卷</a> ·
  <a href="#随书代码">代码</a> ·
  <a href="#引用">引用</a> ·
  <a href="VERIFY.md">校验</a> ·
  <a href="README.md">English</a>
</p>

<br>

# The Arithmetic Topos

Vincent Liu · Research Architecture Edition 1 · 2026 · [English](README.md)

> *Langlands 对应不是一个双射。它是在单一整体底上的一个自对偶六函子几何上所取的迹在 π₀ 处的值。双射，不过是遗忘了
> 令其成立的一切之后的残余。*
> <br>— Preface

《The Arithmetic Topos — Foundations of a Trace-Theoretic Approach to the Langlands Programme》是一部五卷合一的专著
（正文为英文），共 2,001 页。它是 WiseMotif Monograph of Mathematical Intelligence 的第七部著作，属于
Grothendieckian Programme，但自成独立体系：它是该 Programme 的第五个研究课题——在一个问题上把 Programme 的方法，即
递归式数学发现（recursive mathematical discovery），完整地走一遍：提出结构，用答案已知的情形检验它，把经受住检验的
部分抽象出来，再在新的层次上重新提出问题，正如 Grothendieck 的"上涨的海"（rising sea）。

所选的问题是 Langlands 纲领。本书追问：**为什么 Langlands 对应在函数域上可以证明——在那里它对 GL<sub>n</sub> 是定理，对
每个约化群在"自守到 Galois"方向上也已证明——而在数域上总体仍未解决？什么样的对象能让函数域上那些取曲线上 Frobenius
迹的证明在 ℤ 上得以仿照？**

**除文献已证明的情形外，Langlands 纲领在数域上仍未解决。本书没有证明 Langlands 对应，书中也没有无条件地确立其主猜想
的任何一种情形**（命题 40.4）。本书给出的是：把方法毫不让步地用到底之后问题所处的状态——这条算术曲线会给出什么、需要
什么、每条通往它的路线停在哪里。

<table>
  <tr>
    <td align="center"><b>5</b><br><sub>卷，<br>合为一册</sub></td>
    <td align="center"><b>7 · 40</b><br><sub>部 ·<br>章</sub></td>
    <td align="center"><b>2,001</b><br><sub>页</sub></td>
    <td align="center"><b>1,609</b><br><sub>条编号陈述，<br>每条带状态标签</sub></td>
    <td align="center"><b>111 · 53</b><br><sub>台账项 ·<br>其中猜想</sub></td>
    <td align="center"><b>17 · 14</b><br><sub>项证伪测试 ·<br>个研究问题</sub></td>
    <td align="center"><b>120 · 280</b><br><sub>幅矢量 plate ·<br>条参考文献</sub></td>
  </tr>
</table>

## 核心思想：一个底，一个迹

在函数域上，Langlands 纲领有一个底。曲线就是曲线，它的 Frobenius 由域的算术给出，对应是通过在 shtuka 模空间上取
Frobenius 的迹而证明的；在几何情形，范畴形式的对应本身如今也已证明。在 ℤ 上没有底：Spec ℤ 不是任何东西上的曲线，
它没有 Frobenius，它的阿基米德位对层而言是看不见的。

第 1 章分离出四个障碍——缺失的底、缺失的迹、缺失的阿基米德位，以及上同调缺陷 ℓ₀（它使 Taylor–Wiles 方法对除一小类
群与域之外的情形都无法进行）——并论证**它们是同一个障碍：Spec ℤ 上缺少一个可对偶的迹论几何**（原则 1.22，即"单一障碍原则"，
标为设计而非定理）。

本书把这个几何规定出来。**整体算术曲线**（global arithmetic curve）𝔛<sub>ℤ</sub>（定义 10.15）由有限素数处的
syntomification（其局部理论已经确立）与一个阿基米德图卡沿一个 adelic 周期晕（period halo）粘合而成；阿基米德图卡由
Simpson 的 twistor 直线、Connes–Consani 的 scaling flow与 Deninger 的 Riemann 流构成。它带有一个以迹为原始数据的六函子形式，
以及一个绝对 Frobenius Φ，其迹应当算出自守谱。它的存在性（猜想 10.16，GC.1）、有效晕下降（猜想 10.13）与三次定向
（猜想 12.14）都是猜想。

| 方法 | 本书所做的 |
|---|---|
| **诊断** | 六十年来的定理及其各自止步之处；导子为 11 的曲线，在 ℚ 上与在函数域上；四个障碍归结为一个（第 1 章） |
| **奠基** | 把几何定义为带对偶与原始迹的六函子形式——chôra——由公理 KH.1–KH.28 给出，写成模态有向类型论 TT<sub>KH</sub>（Part I） |
| **规定底** | 有限图卡（prismatisation、F-gauge）、阿基米德图卡（twistor、scaling flow）、周期晕与粘合、绝对 Frobenius、三次定向（Part II） |
| **构造两侧** | 算术规范栈与谱栈、平移辛结构、缺陷 ℓ₀ 与 patching 的结构性失效、导出 Hecke 代数与 Koszul 对偶、奇异支集（Part III） |
| **提出猜想** | 主猜想及其三个等价与八个推论；cyclotomic 迹、范畴 Lefschetz 定理、谱作用、作为 Fourier 共轭的函子性（Part IV） |
| **分析** | Schwartz 范畴、作为粘合公理的 Poisson 求和、作为导出指标定理的迹公式、Beyond Endoscopy、L-函数与 Γ-因子、Eisenstein 级数（Part V） |
| **检验推论** | p-进与阿基米德局部对应、模性、Fontaine–Mazur、Ramanujan 与 Arthur、特殊值（Part VI） |
| **审计** | 本书的"宪法"、认证算法、证伪方案、评估与此后的研究纲领（Part VII） |

## 五卷

五卷与附录合为一册。下面每张封面把对应的卷放在 D₆ 蜂巢中心，并带有该格在全书封面上所写的公式。

<table>
  <tr>
    <td width="33%" valign="top" align="center">
      <a href="docs/contents/volume-i.md"><img src="assets/covers/volume-1.jpg" alt="第 I 卷封面——The Kernel and the Base" width="200"></a><br>
      <b>I · The Kernel and the Base</b><br>
      <sub>Part I–II · 12 章 · 第 1–466 页</sub><br><br>
      <sub>问题与论题；把几何定义为带对偶与原始迹的六函子形式，由公理 KH.1–KH.28 给出并写成类型论 TT<sub>KH</sub>；整体算术曲线：有限素数处的 syntomic 图卡、阿基米德图卡、把它们粘合起来的 adelic 晕、绝对 Frobenius 与三次定向。</sub><br><br>
      <a href="docs/contents/volume-i.md">目录</a> · <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf">PDF</a>
    </td>
    <td width="33%" valign="top" align="center">
      <a href="docs/contents/volume-ii.md"><img src="assets/covers/volume-2.jpg" alt="第 II 卷封面——Gauge and Spectral Stacks" width="200"></a><br>
      <b>II · Gauge and Spectral Stacks</b><br>
      <sub>Part III · 6 章 · 第 467–703 页</sub><br><br>
      <sub>作为曲线上之栈的对应两侧、它们的平移辛几何、缺陷 ℓ₀ 及其结构性解释、导出 Hecke 代数与 Koszul 对偶、奇异支集。</sub><br><br>
      <a href="docs/contents/volume-ii.md">目录</a> · <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf">PDF</a>
    </td>
    <td width="33%" valign="top" align="center">
      <a href="docs/contents/volume-iii.md"><img src="assets/covers/volume-3.jpg" alt="第 III 卷封面——The Trace Correspondence" width="200"></a><br>
      <b>III · The Trace Correspondence</b><br>
      <sub>Part IV · 6 章 · 第 704–962 页</sub><br><br>
      <sub>主猜想及其三个等价与八个推论、cyclotomic 迹、范畴 Lefschetz 定理、谱作用、场论表述，以及作为 Fourier 共轭的函子性。</sub><br><br>
      <a href="docs/contents/volume-iii.md">目录</a> · <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf">PDF</a>
    </td>
  </tr>
  <tr>
    <td width="33%" valign="top" align="center">
      <a href="docs/contents/volume-iv.md"><img src="assets/covers/volume-4.jpg" alt="第 IV 卷封面——Analysis and the Trace Formula" width="200"></a><br>
      <b>IV · Analysis and the Trace Formula</b><br>
      <sub>Part V · 6 章 · 第 963–1225 页</sub><br><br>
      <sub>Schwartz 范畴、作为粘合公理的 Poisson 求和、作为导出指标定理的迹公式、Beyond Endoscopy 与被删去的边界、L-函数与 Γ-因子、Eisenstein 级数与连续谱。</sub><br><br>
      <a href="docs/contents/volume-iv.md">目录</a> · <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf">PDF</a>
    </td>
    <td width="33%" valign="top" align="center">
      <a href="docs/contents/volume-v.md"><img src="assets/covers/volume-5.jpg" alt="第 V 卷封面——Consequences and the Programme" width="200"></a><br>
      <b>V · Consequences and the Programme</b><br>
      <sub>Part VI–VII · 10 章 · 第 1226–1621 页</sub><br><br>
      <sub>p-进与阿基米德局部对应、模性、Fontaine–Mazur、Ramanujan 与 Arthur、特殊值；然后是本书的"宪法"、认证算法、证伪方案，以及对已达成与未达成之事的评估和此后的研究纲领。</sub><br><br>
      <a href="docs/contents/volume-v.md">目录</a> · <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf">PDF</a>
    </td>
    <td width="33%" valign="top" align="center">
      <a href="docs/contents/appendices.md"><img src="assets/covers/volume-6.jpg" alt="附录封面——Appendices A–G" width="200"></a><br>
      <b>Appendices A–G</b><br>
      <sub>7 个附录 · 参考文献 · 两种索引 · 第 1622–1954 页</sub><br><br>
      <sub>高阶范畴、condensed 与解析数学、prismatic 与 syntomic 上同调及迹方法，以压缩但完整的形式给出；记号；陈述台账；参考实现；符号索引与陈述索引。</sub><br><br>
      <a href="docs/contents/appendices.md">目录</a> · <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf">PDF</a>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf"><img src="assets/covers/complete.jpg" alt="全书封面——环绕整体算术曲线的 D6 蜂巢" width="260"></a><br>
  <b>全书合卷</b> · 第 I–V 卷与附录 A–G · 2,001 页 · 85.5 MB
</p>

## 主要结果

每一项都带有书中印在它旁边的状态标签。

- **缺口等于缺陷（定理 16.14）*[ESTABLISHED]*，patching 结构性失效（定理 16.16）*[THEOREM]*。** 对数域上绝对不可约的
  ρ̄ 到 GL<sub>n</sub> 的极小 crystalline 形变问题（p > 2，实位处满足一个奇偶条件），生成元–关系缺口 g − r 等于 −ℓ₀。
  若 ℓ₀ > 0，则 patching 所得的环满足 dim R<sub>∞</sub> = dim S<sub>∞</sub> − ℓ₀，所得的模不是自由模，并且无论扩大 S、
  另选 Taylor–Wiles 素数，还是改变 p、ρ̄ 或水平，都无法修复这一论证。
- **主猜想（猜想 19.5）*[CONJECTURE]*。** 对数域上的连通约化群 G，在逐一列名的假设下，
  𝒜(G) ≃ TC(Φ ∣ Shv<sub>𝒩</sub>(Bun<sub>G</sub>(𝔛<sub>ℤ</sub>))) ≃ TC(Φ ∣ IndCoh<sub>𝒩</sub>(LocSys<sub>ᴸG</sub>(𝔛<sub>ℤ</sub>))) ≃ Γ(LocSys<sup>Φ</sup><sub>ᴸG</sub>, ω<sup>vir</sup>)：
  自守谱是规范栈上幂零层的 Frobenius 扭循环迹，也是谱栈上的这个迹，又是 Frobenius 不动点轨迹上的虚对偶层。三个箭头是
  三个独立的断言 MC1–MC3，各有各的否证条件。
- **八个推论，每个都写明所用假设（推论 19.17–19.24）*[CONJECTURE]*。** 互反律；作为 Fourier 核共轭的函子性；作为正则化
  行列式的阿基米德 Γ-因子；Ramanujan、纯性与 Arthur SL<sub>2</sub>；作为跨越 Hodge–Tate 除子之延拓的 Fontaine–Mazur；
  作为指标定理的 Arthur–Selberg 迹公式；局部–整体相容性；作为迹缺陷的特殊值。八个推论中有六个在其经典表述下是未解决的
  问题。
- **局部项是消没循环（定理 21.28，TR.8）*[THEOREM]*。** 迹的局部化数据把 Tr(Φ ∣ IndCoh<sub>𝒩</sub>(Y)) 按不动点轨迹的
  连通分支 β 分解，β 的贡献是 Γ(β, 𝒫<sub>β</sub>)，即消没循环反常层的整体截面；其 Euler 示性数是 Behrend 加权计数，
  在奇异与导出情形下它取代了 Atiyah–Bott 分母。
- **Poisson 求和即晕下降（定理 26.7）*[THEOREM]*。** 整体相容的局部 Fourier 数据在 adelic 晕上满足上闭链条件；若晕下降
  猜想 10.13 对这个覆盖成立，则它是有效的，下降所得的对合由 Σ f(α) = Σ (ℱf)(α)（α ∈ F）刻画。
- **作为 Fourier 共轭的函子性（猜想 24.20）*[CONJECTURE]*。** 对每个满足所述有限性与反常消去条件的 L-同态
  η: ᴸH → ᴸG，转移为 Lift<sub>η</sub> = ℱ<sup>−1</sup><sub>L,G</sub> ∘ Rη<sub>∗</sub> ∘ ℱ<sub>L,H</sub>。
- **致命三元组（推论 39.27）*[THEOREM]*。** 证伪方案中的测试 1、5、6 任何一项失败都否证主猜想；三者同时失败则什么也
  不剩。
- **更正后的计数（命题 40.3）与无无条件情形（命题 40.4）*[THEOREM]*。** 台账共 111 项，即 83 个条目与 28 条公理：猜想
  53、框架定理 24、既有结果 15、设计 25。不存在任何一对 (F, G)——连 F = ℚ、G = 𝔾<sub>m</sub> 也不例外——使本书构造出
  猜想 19.5 的全部三个箭头并解除全部假设。

## 本书是什么——不是什么

**本书是**一个框架：一个基础体系、该体系所需对象的构造、对应在其中的精确表述、一份需要证明之事的明确清单，以及一个
可望逐项解除这份清单的计算与形式验证纲领。每条编号陈述都带有五种标签之一，印在编号旁：**[ESTABLISHED]** 既有文献中的
定理，或在此由这类定理完整证明的结果；**[THEOREM]** 框架内的定理，在本书中由所述公理证明；**[CONJECTURE]** 无论在此
还是别处都未证明；**[DESIGN]** 定义、构造或设计原则，不带任何真值断言；**[FORMAL TARGET]** 写成证明助手可以检验的
形式，尚未经机器检验。1,609 条编号陈述中，既有结果 675、框架定理 234、猜想 207、设计 482、形式目标 11（Index of
Statements）。每一章至少有一个标为 *Caveat* 的段落，放在该章最弱而非最强之处。

**本书不是** Langlands 对应的证明。主猜想标为 [CONJECTURE]，书中任何地方都没有无条件地证明它的任何一种情形。本书没有
证明模性的任何新情形、函子性的任何新情形、Ramanujan 猜想的任何实例，也完全没有涉及任何 L-函数零点的位置。台账中的
24 个定理每一个都以至少一条公理或存在性猜想 GC.1 为条件；第 40 章列出四个即使框架整体崩塌也仍然成立的结果——形如
定理 21.28 的范畴 Lefschetz 定理、第 20 章的迹刚性定理、定理 9.27 背后阿基米德正则化行列式的计算，以及第 17 章汇集的
矩阵分解局部结构理论。软件中没有任何东西断言一个数学事实，Lean 4 语句骨架也尚未编译。

## 从哪里读起

第 1 章是整个架构的完整叙述；§1.5 与 §1.6 非正式地陈述主猜想，并列出本书主张什么、什么会证伪它。*How to Read This
Book* 给出四条路线。

| 路线 | 章节 |
|---|---|
| 怀疑者的路线（本书推荐） | 40，评估；附录 F，台账；39，证伪方案；然后 1 |
| 算术学者的路线 | 1；7；16；19；33–36；40 |
| 范畴论学者的路线 | 2–6；12、15、18；19–23；附录 A |
| 计算的路线 | 37；38；附录 G；然后是 aletheia 源代码 |

[预览版](https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Preview.pdf) 包含前置部分——Series Note、Abstract、Preface、
Acknowledgements、How to Read This Book、Notation and Conventions、目录与 plate 列表——以及整个 Part I（第 1–6 章）。

## 系列

本书是 WiseMotif Monograph of Mathematical Intelligence 的第七部（Series 07），自成独立体系，是 Grothendieckian Programme 的第五个研究课题。系列的前两部紧密相连。从第三部起，每一部都是围绕一个问题自成体系的著作，在这个问题上把 Programme 的方法——递归式数学发现——完整地走一遍。七部作品依次为：

<table>
  <tr>
    <td width="96" valign="top" align="center"><a href="https://github.com/AlienMuse/grothendieckian-machine"><img src="https://raw.githubusercontent.com/AlienMuse/grothendieckian-machine/main/assets/covers/complete.jpg" alt="《GAI-MUA: The Grothendieckian Machine》封面" width="80"></a></td>
    <td valign="top"><b>Series 01 · <a href="https://github.com/AlienMuse/grothendieckian-machine"><i>GAI-MUA: The Grothendieckian Machine</i></a></b><br>
      <sub><i>A Mathematical Universe Architecture for Verifiable and Self-Evolving Artificial Intelligence</i></sub><br>
      Programme 的核心部分：数学世界如何被构造、比较并从一个情境迁移到另一个情境，以及机器如何把它们作为有类型、有版本、可验证的对象来持有。<br>
      <sub>6 卷 · 14,905 页 · <a href="https://doi.org/10.5281/zenodo.23480696">doi:10.5281/zenodo.23480696</a></sub></td>
  </tr>
  <tr>
    <td width="96" valign="top" align="center"><a href="https://github.com/AlienMuse/topos-native-intelligence"><img src="https://raw.githubusercontent.com/AlienMuse/topos-native-intelligence/main/assets/covers/complete.jpg" alt="《GM-Omega-Infinity: Topos-Native Intelligence》封面" width="80"></a></td>
    <td valign="top"><b>Series 02 · <a href="https://github.com/AlienMuse/topos-native-intelligence"><i>GM-Omega-Infinity: Topos-Native Intelligence</i></a></b><br>
      <sub><i>A Sheaf-Theoretic Architecture for Verifiable Machine Intelligence</i></sub><br>
      元推理内核：一个智能系统若要在这些世界内部推理，其内部必须是什么。<br>
      <sub>5 卷 · 4,020 页 · <a href="https://doi.org/10.5281/zenodo.23538544">doi:10.5281/zenodo.23538544</a></sub></td>
  </tr>
  <tr>
    <td width="96" valign="top" align="center"><a href="https://github.com/AlienMuse/arithmetic-spectral-descent"><img src="https://raw.githubusercontent.com/AlienMuse/arithmetic-spectral-descent/main/assets/covers/complete.jpg" alt="《Arithmetic Spectral Descent》封面" width="80"></a></td>
    <td valign="top"><b>Series 03 · <a href="https://github.com/AlienMuse/arithmetic-spectral-descent"><i>Arithmetic Spectral Descent</i></a></b><br>
      <sub><i>Obstruction Theory, Hodge–Krein Realization, and a Falsifiable Architecture for the Riemann Hypothesis</i></sub><br>
      研究课题 1：黎曼猜想。<br>
      <sub>4 卷 · 1,549 页 · <a href="https://doi.org/10.5281/zenodo.23564898">doi:10.5281/zenodo.23564898</a></sub></td>
  </tr>
  <tr>
    <td width="96" valign="top" align="center"><a href="https://github.com/AlienMuse/fractured-adelic-geometry"><img src="https://raw.githubusercontent.com/AlienMuse/fractured-adelic-geometry/main/assets/covers/complete.jpg" alt="《Fractured Adelic Geometry》封面" width="80"></a></td>
    <td valign="top"><b>Series 04 · <a href="https://github.com/AlienMuse/fractured-adelic-geometry"><i>Fractured Adelic Geometry</i></a></b><br>
      <sub><i>A Foundational Framework for the Birch and Swinnerton-Dyer Conjecture</i></sub><br>
      研究课题 2：Birch–Swinnerton-Dyer 猜想（BSD 猜想）。<br>
      <sub>4 卷 · 571 页 · <a href="https://doi.org/10.5281/zenodo.23585887">doi:10.5281/zenodo.23585887</a></sub></td>
  </tr>
  <tr>
    <td width="96" valign="top" align="center"><a href="https://github.com/AlienMuse/the-archimedean-prism"><img src="https://raw.githubusercontent.com/AlienMuse/the-archimedean-prism/main/assets/covers/complete.jpg" alt="《The Archimedean Prism》封面" width="80"></a></td>
    <td valign="top"><b>Series 05 · <a href="https://github.com/AlienMuse/the-archimedean-prism"><i>The Archimedean Prism</i></a></b><br>
      <sub><i>Tame Period Geometry and the Hodge Conjecture</i></sub><br>
      研究课题 3：Hodge 猜想。<br>
      <sub>5 卷 · 1,309 页 · <a href="https://doi.org/10.5281/zenodo.23597954">doi:10.5281/zenodo.23597954</a></sub></td>
  </tr>
  <tr>
    <td width="96" valign="top" align="center"><a href="https://github.com/AlienMuse/strained-prismatic-geometry"><img src="https://raw.githubusercontent.com/AlienMuse/strained-prismatic-geometry/main/assets/covers/complete.jpg" alt="《Strained Prismatic Geometry》封面" width="80"></a></td>
    <td valign="top"><b>Series 06 · <a href="https://github.com/AlienMuse/strained-prismatic-geometry"><i>Strained Prismatic Geometry</i></a></b><br>
      <sub><i>Deformation over the Absolute Base and the abc Conjecture</i></sub><br>
      研究课题 4：abc 猜想。<br>
      <sub>5 卷 · 1,666 页 · <a href="https://doi.org/10.5281/zenodo.23610034">doi:10.5281/zenodo.23610034</a></sub></td>
  </tr>
  <tr>
    <td width="96" valign="top" align="center"><img src="assets/covers/complete.jpg" alt="本书封面" width="80"></td>
    <td valign="top"><b>Series 07 · <i>The Arithmetic Topos</i></b>（本书）<br>
      <sub><i>Foundations of a Trace-Theoretic Approach to the Langlands Programme</i></sub><br>
      研究课题 5：Langlands 纲领。<br>
      <sub>5 卷 · 2,001 页 · <a href="https://doi.org/10.5281/zenodo.23629681">doi:10.5281/zenodo.23629681</a></sub></td>
  </tr>
</table>

## 下载

| 文件 | 页数 | 大小 |
|---|---:|---:|
| [**全书合卷**](https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Complete.pdf)——第 I–V 卷与附录 A–G | 2,001 | 85.5 MB |
| [预览版](https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-Preview.pdf)——前置部分与 Part I | 283 | 72.9 MB |
| [随书代码](https://github.com/AlienMuse/the-arithmetic-topos/releases/download/v1.0.0/The-Arithmetic-Topos-v1.0.0-code.zip)——aletheia 与 Lean 4 语句骨架，Apache-2.0 | — | 93.7 KB |

相同文件（校验值相同）存档于 Zenodo：[doi:10.5281/zenodo.23629682](https://doi.org/10.5281/zenodo.23629682)。封面为 600 ppi 全出血；全部字体已嵌入；
PDF 已线性化，便于快速打开。

## 随书代码

[`code/`](code/) 是本书的随书代码，与 Release 中的代码包相同。

- **aletheia**（[`code/aletheia/`](code/aletheia/)），参考实现：Part VII 所述接口、有限算法与证据规范的工程模型——迹与权的
  有限核心、Satake 与 Hecke 数据、Galois 缺陷计数、Newton 与 Hodge 多边形、轨道和、证书、状态格与证据台账。它只用
  Python 标准库，21 项测试全部通过。它实现了一部分有限核心，书中其余对象只以元数据或接口表示；一次成功的计算只提供
  有限证据或一个经检验的有限恒等式，只有外部的数学证明或证明助手的内核才能确立一般定理。附录 G 记录了它做了什么、
  还没有做什么。
- **Lean 4 语句骨架**（[`code/lean/`](code/lean/)）：把形式目标写成 Lean 语句，含三十三个未填的占位（`sorry`）；尚未编译。

```sh
cd code
python -m pytest tests -q                               # 21 项测试（需要 pytest）
python -m aletheia selfcheck                            # 八项有限自检
python -m aletheia defect --group GL2 --field "Q(i)"    # 一个 Bianchi 群的缺陷 ℓ₀
python -m aletheia lfunction --curve 11a1 --terms 200   # 导子为 11 的曲线
```

`REPRODUCIBILITY.md` 把书中印出的数字与测试及数值验证脚本的输出逐一对照；`CODE-EDITS.md` 列出为出版所做的文档修改
（程序代码一行未改）。附录 G 与第 38 章描述的是 0.1.0 版一个较早的受审快照，其中证据台账模块有一个语法错误导致无法
导入，另有两项测试失败；本仓库发布的代码中这些缺陷已不存在，21 项测试全部通过。代码以 Apache License 2.0 授权
（[code/LICENSE](code/LICENSE)），书本身不是。

## 引用

> Liu, V. (2026). *The Arithmetic Topos — Foundations of a Trace-Theoretic Approach to the Langlands Programme*
> (Research Architecture Edition 1, version 1.0.0). Zenodo. https://doi.org/10.5281/zenodo.23629681

```bibtex
@book{liu2026arithmetictopos,
  author    = {Liu, Vincent},
  title     = {The Arithmetic Topos --- Foundations of a Trace-Theoretic Approach to the {Langlands} Programme},
  series    = {WiseMotif Monograph of Mathematical Intelligence, Series 07},
  edition   = {Research Architecture Edition 1},
  version   = {1.0.0},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23629681},
  url       = {https://doi.org/10.5281/zenodo.23629681}
}
```

GitHub 的 *Cite this repository* 按钮使用 [CITATION.cff](CITATION.cff)。概念 DOI 10.5281/zenodo.23629681 始终指向最新版本；引用这些
确切文件时请用版本 DOI 10.5281/zenodo.23629682。

## 真实性

Release 的每个文件都列在 `SHA256SUMS` 中，经 OpenPGP 签名，并有两重时间戳（RFC 3161 与比特币上的 OpenTimestamps）。
签名密钥与 Series 01–06 相同。

签名密钥指纹：`DA1A 1AEF D8B2 C17C FF3F 1D1B 3905 0F50 7A4F EC17`

本仓库的 GitHub Release 不可更改。从别处获得、与 `SHA256SUMS` 不符的副本不是真本。三级校验方法见 [VERIFY.md](VERIFY.md)。

## 许可与 AI 使用

本作品采用 [知识共享 署名-非商业性使用-禁止演绎 4.0 国际许可协议](LICENSE)（CC BY-NC-ND 4.0）：您可以在注明作者、
非商业使用的前提下分享未经修改的副本。翻译及其他用途需获得书面许可。如版权页所述，书中印出的代码清单与随书代码——
aletheia 参考实现与 Lean 4 语句骨架——另以 [Apache License 2.0](LICENSES/Apache-2.0.txt) 授权。详见
[NOTICE.md](NOTICE.md) 与 [TRADEMARKS.md](TRADEMARKS.md)。

**文本与数据挖掘权利依欧盟指令 2019/790 第 4(3) 条予以保留。** 未经书面许可，不得用本作品训练或微调机器学习模型。
个人读者可以使用 AI 工具阅读、检索、讲解或翻译本作品以供自学。完整政策见 [TDM-AND-AI-POLICY.md](TDM-AND-AI-POLICY.md)。

## 参与

第 40 章最后一节写给认为这个框架错了的读者：一次瞄准得当的反驳，对作者而言胜过十年同情的引申。它请读者攻击二十四个
定理与各处推导，而不是猜想——猜想未被证明这一点书中已明说，并未隐瞒。最重要的三类贡献：

- **反驳**——第 39 章证伪方案的十七项测试中的任何一项，每一项都写明它失败时哪些陈述随之失效。书中点名了最便宜的几项：
  猜想 12.14 的定向次数（问题 P1）、Bianchi 情形下用两种方法计算 ℓ₀（P3），以及证明阿基米德障碍是一个定理。
- **构造**——第 40 章十四个研究问题中的任何一个，或该章详细讨论的四个最难缺口之一：底的构造、ambidexterity 定理、
  阿基米德位处的六函子形式、大范畴上迹的基础。
- **复现**——用书中表格独立检验 aletheia，或用一条编译通过的 Lean 陈述替换三十三个占位中的一个。

状态标签可以降级，陈述可以撤回，公理可以被证明与另一条不相容：台账就是为了把这类修改当作正常操作来接受而设计的。
请通过 [勘误 issue](https://github.com/AlienMuse/the-arithmetic-topos/issues/new?template=errata.yml) 报告错误。被采纳的更正将在下一版中署名致谢（见 [ERRATA.md](ERRATA.md)）。

---

<p align="center"><sub>
  <a href="https://wisemotif.ai">WiseMotif Monograph of Mathematical Intelligence</a> · Series 07 · Mathematics and Artificial Intelligence<br>
  Series 01：<a href="https://github.com/AlienMuse/grothendieckian-machine"><i>GAI-MUA: The Grothendieckian Machine</i></a> ·
  Series 02：<a href="https://github.com/AlienMuse/topos-native-intelligence"><i>GM-Omega-Infinity: Topos-Native Intelligence</i></a> ·
  Series 03：<a href="https://github.com/AlienMuse/arithmetic-spectral-descent"><i>Arithmetic Spectral Descent</i></a> ·
  Series 04：<a href="https://github.com/AlienMuse/fractured-adelic-geometry"><i>Fractured Adelic Geometry</i></a> ·
  Series 05：<a href="https://github.com/AlienMuse/the-archimedean-prism"><i>The Archimedean Prism</i></a> ·
  Series 06：<a href="https://github.com/AlienMuse/strained-prismatic-geometry"><i>Strained Prismatic Geometry</i></a><br>
  © 2026 Vincent Liu
</sub></p>
