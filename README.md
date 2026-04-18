# 模型检测课程大作业最终报告

本报告基于仓库中的实现代码与 `code.md` 要求编写，按三部分组织：

1. 带有注释的源代码（并标注四个关键步骤对应代码）
2. 编译方式与使用方式
3. 实现文档（代码结构、数据结构、主要实现细节）

---

## 一、带有注释的源代码

> 说明：这里的“带注释源代码”采用“模块功能说明 + 关键函数摘录注释”的方式，便于对照仓库直接定位。

### 1.1 模块功能总览

| 模块路径 | 功能 |
|---|---|
| `src/main.py` | 主流程：读取 TS 与 benchmark，执行每条公式的模型检测并输出 0/1 |
| `src/GNBA.py` | LTL 闭包、初等集构造、GNBA 构造、GNBA 到 NBA 退化 |
| `ltl_formula/ts_io.py` | 解析 `TS.txt`（状态、迁移、标签、初态） |
| `ltl_formula/benchmark_io.py` | 解析 `benchmark.txt`（全局公式 + 状态公式） |
| `ltl_formula/antlr_parse.py` + `antlr_visitor_impl.py` | 基于 ANTLR 将公式字符串解析为 AST |
| `grammars/LTL.g4` | LTL 文法定义 |

### 1.2 四个关键步骤与代码对应

- 步骤一（教材条目 2）：LTL 公式到 GNBA 的等价构造
  - 对应代码：`src/GNBA.py`
  - 核心函数：`visit_formula`、`visit_elementary_sets`、`build_elementary_graph`、`GNBA.__init__`

- 步骤二（教材条目 3）：GNBA 到 NBA 的等价转换
  - 对应代码：`src/GNBA.py`
  - 核心函数：`GNBA.to_nba`

- 步骤三（教材条目 4）：TS 与 NBA 的乘积构造
  - 对应代码：`src/main.py`
  - 核心函数：`build_ts_nba_product`、`build_ts_nba_product_from_starts`

- 步骤四（教材条目 5）：Algorithm 8（Buchi 非空性判定）
  - 对应代码：`src/main.py`
  - 核心函数：`buchi_language_nonempty`（Nested DFS）

### 1.3 带注释代码摘录（关键步骤）

#### 步骤一：LTL -> GNBA（闭包、初等集、迁移、接受族）

```python
# src/GNBA.py
class GNBA:
    def __init__(self, ltl_formula: ast.Formula):
        self.formula = ltl_formula

        # 1) 计算闭包 cl(phi)：包含子式及需要的 Next 扩展
        self.closure_phi = visit_formula(ltl_formula)
        self.closure: set[ast.Formula] = set(self.closure_phi)

        # 2) 枚举并筛选“局部一致”的子集，得到所有初等集（GNBA 状态）
        self.elementary_sets: list[set[ast.Formula]] = visit_elementary_sets(self.closure_phi)

        # 3) 构造初等集图（边由 Next 同步 + Until 义务决定）
        self.elementary_frozen, self.ap_labels, self.edges = build_elementary_graph(
            self.elementary_sets,
            self.closure,
        )

        # 4) 初态：满足整式 phi 的初等集
        self.initial_states: list[int] = sorted(
            i for i, b in enumerate(self.elementary_frozen) if self.formula in b
        )

        # 5) 广义接受族：按 U/F/G 子式生成接受集合
        self.accept_families: list[frozenset[int]] = []
        for node in sorted(self.closure, key=_closure_sort_key):
            fam = generate_accept_family(node, self.elementary_frozen)
            if fam:
                self.accept_families.append(fam)
```

#### 步骤二：GNBA -> NBA（去广义化）

```python
# src/GNBA.py
# 用 phase 跟踪“当前应该命中的接受族”，命中后相位循环推进。
def to_nba(self) -> NBA:
    n = len(self.elementary_frozen)
    m = len(self.accept_families)

    # m == 0 时退化为单接受集（实现中设为全体接受）
    if m == 0:
        return NBA(
            n_states=n,
            edges=[sorted(set(row)) for row in self.edges],
            initial_states=list(self.initial_states),
            accept=frozenset(range(n)),
            gnba_state_for_nba_state=tuple(range(n)),
        )

    def idx(q: int, phase: int) -> int:
        return q * m + phase

    edges_nba: list[list[int]] = [[] for _ in range(n * m)]
    for q in range(n):
        for phase in range(m):
            src = idx(q, phase)
            f_i = self.accept_families[phase]
            for q2 in self.edges[q]:
                phase2 = (phase + 1) % m if q in f_i else phase
                edges_nba[src].append(idx(q2, phase2))

    initial = [idx(q, 0) for q in self.initial_states]
    accept = frozenset(idx(q, 0) for q in self.accept_families[0])
    return NBA(...)
```

#### 步骤三：TS × NBA 乘积构造

```python
# src/main.py
# 乘积状态编码：(s, q) -> s * |Q| + q
# 转移规则：TS 走 s->t，NBA 读入 L(t) 后 q->q'
def build_ts_nba_product(...):
    n_ts, n_q = ts.num_states, nba.n_states
    adj: list[list[int]] = [[] for _ in range(n_ts * n_q)]

    def enc(s: int, q: int) -> int:
        return s * n_q + q

    for s in range(n_ts):
        for q in range(n_q):
            g = nba.gnba_state_for_nba_state[q]
            for _act, s2 in _ts_successors(ts, s):
                t_names = ts_label_as_names(ts, s2)
                if not label_matches_elementary(t_names, elem_labels[g], ap_alphabet):
                    continue
                for q2 in nba.edges[q]:
                    adj[enc(s, q)].append(enc(s2, q2))

    accept = frozenset(enc(s, q) for s in range(n_ts) for q in nba.accept if q < n_q)
    return prod_n, adj, initial, accept
```

#### 步骤四：Algorithm 8（Buchi 非空性）

```python
# src/main.py
# Nested DFS：寻找从初态可达且包含接受态的可回环路径

def buchi_language_nonempty(adj, initial, accept):
    reachable = forward_reachable(adj, initial)
    color = [_WHITE] * len(adj)

    def dfs2(v, red):
        red.add(v)
        for w in adj[v]:
            if w not in reachable:
                continue
            # 命中外层栈上的 CYAN 结点，表示找到回路
            if color[w] == _CYAN:
                return True
            if color[w] != _BLUE and w not in red and dfs2(w, red):
                return True
        return False

    def dfs1(v):
        color[v] = _CYAN
        for w in adj[v]:
            if w in reachable and color[w] == _WHITE and dfs1(w):
                return True
        # 外层遇到接受态时，启动内层 DFS 寻找回环
        if v in accept and dfs2(v, set()):
            return True
        color[v] = _BLUE
        return False

    for s0 in initial:
        if s0 in reachable and color[s0] == _WHITE and dfs1(s0):
            return True
    return False
```

### 1.4 主流程（反例搜索）

```python
# src/main.py
# TS |= phi  <=>  TS x A(not phi) 的 Buchi 语言为空

def ts_satisfies_ltl(ts, phi, start_states):
    neg = intern_formula(ast.Not(phi))
    g = GNBA(neg)                   # 构造 A(not phi) 的 GNBA
    g.remove_unreachable()
    nba = prune_nba_unreachable(g.to_nba())

    # 若存在反例路径（可被 A(not phi) 接受），则不满足 phi
    has_counterexample = counterexample_exists_verifier(
        ts, nba, g.ap_labels, g.ap_alphabet, start_states
    )
    return not has_counterexample
```

---

## 二、编译方式以及使用方式

### 2.1 环境要求

- Python 3.10+（建议 3.11）
- Java（用于 ANTLR 代码生成）
- 依赖包：`antlr4-python3-runtime>=4.13.0,<4.14`

### 2.2 Python 版本（主实现）

#### 1）创建虚拟环境并安装依赖

```bash
cd /home/oranjun/LTL-Formula
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2）生成 ANTLR 解析器（首次或修改语法后）

```bash
# 方式 A
bash tools/generate_antlr_parser.sh

# 方式 B
bash run.sh --gen-antlr
```

#### 3）运行模型检测

```bash
# 使用默认输入（project_benchmark/TS.txt + project_benchmark/benchmark1.txt）
bash run.sh

# 指定输入文件
bash run.sh project_benchmark/TS.txt project_benchmark/benchmark.txt

# 或直接调用 Python
python src/main.py project_benchmark/TS.txt project_benchmark/benchmark.txt
```

#### 4）输出说明

- 程序按 benchmark 中任务顺序输出 A+B 行。
- 每行 `1` 表示满足，`0` 表示不满足。

## 三、实现文档（结构、数据结构、主要细节）

### 3.1 代码结构

- 输入层
  - `ltl_formula/ts_io.py`：将 `TS.txt` 解析为 `TransitionSystem`
  - `ltl_formula/benchmark_io.py`：将 `benchmark.txt` 解析为 `BenchmarkSpec`

- 语法与 AST 层
  - `grammars/LTL.g4`：LTL 文法
  - `ltl_formula/antlr_parse.py`、`antlr_visitor_impl.py`：ANTLR 语法树到内部 AST
  - `ltl_formula/ast.py`：公式节点定义与结构共享（intern）

- 自动机构造层
  - `src/GNBA.py`：闭包、初等集、广义接受族、去广义化得到 NBA

- 模型检测层
  - `src/main.py`：对每条公式构造 `A(not phi)`，在 TS 上做反例搜索并输出结果

### 3.2 关键数据结构

1) TransitionSystem（`ltl_formula/ts_io.py`）
- `num_states`: 状态数 S
- `transitions`: 三元组列表 `(i, k, j)`
- `initial_states`: 初态集合 I
- `ap_names`: 原子命题名称表
- `labels`: 每个状态上的命题下标集合 `L(s)`

2) Formula AST（`ltl_formula/ast.py`）
- 结点类型：`Prop/Not/And/Or/Implies/Until/Next/Finally/Globally`
- 通过 intern 共享结构，降低重复构造与比较开销。

3) GNBA（`src/GNBA.py`）
- `elementary_sets`: 初等集（GNBA 状态）
- `edges`: 初等集图
- `initial_states`: 满足整式的初始状态索引
- `accept_families`: 广义接受族 `F1..Fm`
- `ap_labels`: 每个状态下 AP 取值（用于与 TS 标签匹配）

4) NBA（`src/GNBA.py`）
- `n_states`、`edges`、`initial_states`、`accept`
- `gnba_state_for_nba_state`: NBA 状态到原 GNBA 状态的映射

### 3.3 关键算法细节

#### A. 公式处理与闭包构造

- 输入公式先做 AST 解析，再统一到内部节点对象。
- 闭包构造采用 DFS 收集子式；对 U/F/G 子式补充必要的 X 扩展，以满足转移一致性判定需要。

#### B. 初等集枚举与一致性检查

- 枚举闭包的所有子集。
- 用局部一致性规则（Not、And、Or、Implies、Until、Finally、Globally）筛掉不合法集合。
- 合法集合即 GNBA 状态。

#### C. GNBA 转移与接受条件

- 转移规则：
  - Next 同步：`X psi in B` 当且仅当 `psi in B'`
  - Until 义务：若 `psi1 U psi2 in B` 且 `psi2 not in B`，则 `psi1 U psi2 in B'`
- 接受族：按 U/F/G 子式构造，保证“未满足义务最终被满足”语义。

#### D. GNBA 到 NBA 退化

- 复制状态并附加相位 `phase`。
- 在遍历过程中按当前相位对应接受族是否命中来推进相位。
- 只保留单一 Büchi 接受集，实现等价识别。

#### E. TS × NBA 乘积与反例搜索

- 乘积状态 `(s, q)` 扁平编码为 `s * |Q| + q`。
- 乘积边由 TS 边与 NBA 边同步生成，字母匹配由 AP 标签一致性判定。
- 模型检测判定：
  - 构造 `A(not phi)`；
  - 判断 `TS × A(not phi)` 是否存在可达接受环；
  - 若存在反例环则输出 `0`，否则输出 `1`。

#### F. Algorithm 8（Nested DFS）实现

- 外层 DFS 负责可达性与主搜索栈颜色管理（WHITE/CYAN/BLUE）。
- 外层到达接受态时触发内层 DFS，寻找返回外层栈的回边。
- 一旦找到可达接受环，立刻返回“非空”。

---

## 附：可直接复现实验的最小命令集

```bash
cd /home/oranjun/LTL-Formula
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash run.sh --gen-antlr
bash run.sh project_benchmark/TS.txt project_benchmark/benchmark.txt
```
