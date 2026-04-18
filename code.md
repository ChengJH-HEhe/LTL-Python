# 代码模块说明

**约定**：输入格式、输出顺序与含义以仓库根目录 **`README.md`** 为准（与 **`Input_Format.pdf`** 一致）。本文说明实现与模块分工；TS 行块为 **`S T`、初态、`A` 动作、`P` 原子命题、`T` 条 `(i,k,j)`、`S` 行标签（`-1` 表示 \(L(s_i)=\emptyset\)）。

---

## 目录结构（核心代码）

| 路径 | 类型 | 作用摘要 |
|------|------|----------|
| `grammars/LTL.g4` | ANTLR 语法 | LTL 公式；与 README「公式语言」一致（`/\\`、`\\/`、`->`、`!`、`G`/`F`/`X`/`U`、小写命题等）。 |
| `ltl_formula/` | Python 包 | AST、`parse_ltl`、TS/benchmark 读入。 |
| `tools/generate_antlr_parser.sh` | Shell | `java -jar` 从 `LTL.g4` 生成 `ltl_formula/generated/*.py`；可用环境变量 **`ANTLR_JAR`**（`run.sh` 会导出默认值）。 |
| `tools/gen_antlr.sh` | Shell | 若存在，可与上者二选一（以本仓库实际脚本为准）。 |
| `requirements.txt` | 依赖 | `antlr4-python3-runtime`（与 ANTLR4.13.x jar 主版本一致）。 |
| `project_benchmark/` | 样例 | README 第四节 **`TS.txt`、`benchmark.txt`** 等。 |
| `src/GNBA.py` | LTL → GNBA → NBA | 初等集、**`to_nba()`**、**`NBA`**。 |
| `src/main.py` | 可执行pipe | 读 **`TS.txt`** 与 **`benchmark.txt`**，按 README 第三节逐行输出 **`1`/`0`**（先 `A` 条全局，再 `B` 条按状态）。 |
| `run.sh` | Shell | 调用 `src/main.py`；**`./run.sh --gen-antlr`** 转调 `generate_antlr_parser.sh`。 |

---

## 与 README 的对应关系

| README 章节 | 实现 |
|-------------|------|
| 一、`TS.txt` | `ltl_formula.ts_io`：`load_ts_file` / `parse_ts_text` → **`TransitionSystem`** |
| 二、`benchmark.txt` | `ltl_formula.benchmark_io`：`load_benchmark_file` / `parse_benchmark_text` → **`BenchmarkSpec`** |
| 三、程序输出 | `src/main.py`：对 **`A+B`** 条任务按序各输出一行 **`1` 或 `0`**（仅 stdout，无额外调试输出） |
| 作业条目 2–5（GNBA、NBA、乘积、Algorithm 8） | `GNBA.py` + `main.py` 中乘积与 **Nested DFS** 判 Büchi 非空（见下） |

---

## `src/main.py`（判满足流程）

1. **`parse_ltl`**：ANTLR + **`intern_formula`** 得 AST。  
2. **反例自动机**：对公式 **¬φ** 构造 **GNBA → NBA**；若 **TS × NBA(¬φ)** 语言**非空**，则存在违反 φ 的路径，输出 **`0`**；否则 **`1`**。  
3. **任务起点**（与 README 语义一致）：  
   - 前 **`A`** 条全局公式：乘积初态为 **`ts.initial_states`** × NBA 初态；  
   - 后 **`B`** 条 **`i φ`**：乘积初态为 **`{i}`** × NBA 初态。  

**AP 同步**：在公式字母表上，TS 状态标签（经 `ap_names`）须与 NBA 状态对应初等集 **`ap_labels`** 一致；迁移进入的目标 TS 状态与目标 NBA 状态一起校验。

**乘积状态**：`(s, q)` 扁平为 **`s * |Q| + q`**；Büchi 接受为 NBA **`accept`** 在乘积上的提升。

**`buchi_language_nonempty`**：Nested DFS（外层 cyan/blue，内层找回到栈上结点的环），在初态正向可达子图上判定，对应教材 **Algorithm 8** 的判空思路。

**命令行**（与 README 评测一致）：

```bash
python src/main.py [TS.txt] [benchmark.txt]
```

默认：`project_benchmark/TS.txt`、`project_benchmark/benchmark.txt`。

**调试指标（stderr）**：设置环境变量 **`LTL_MC_VERBOSE=1`** 时，每条任务会打印一行统计：`φ`、初等集个数、NBA 状态数、乘积结点数、乘积初态数、乘积可达结点数、接受集大小、**`TS×A(¬φ)` 语言是否非空**（非空 ⇒ 存在违反 `φ` 的路径 ⇒ **`satisfies_phi=false`** 对应输出 **`0`**）。

**实现注意**：当前 GNBA 的 Büchi 接受族**仅对 `Until` 子式** degeneralize；若 `¬φ` 的闭包中**没有** `Until`（例如 `¬φ` 仅为 `Not(Globally …)` 而 AST 未表成 `Until`），则 `to_nba()` 走 **`m=0`** 分支（**全体状态接受**），Büchi 语义会**过弱**，可能对 **`G`、纯 `F`** 等公式产生**假反例**（例如结构上应满足 `G(a\\/b)` 的 TS 仍得到 **`0`**）。调试时务必看 **`nonempty_TSxA_not_phi`** 与公式结构是否涉及上述退化。

---

## `src/GNBA.py`（摘要）

- **闭包 / 初等集 / `edges`**：Next 同步与 Until 义务；**`ap_labels`**、**`ap_alphabet`**。  
- **`initial_states`**：全公式 ∈初等集。  
- **`accept_families`**：每个 **Until** 子式一条 Büchi 族；无 Until 时 **`to_nba()`** 约定全体状态接受。  
- **`GNBA.to_nba()`** → **`NBA`**：广义 Büchi 用相位 tracker 退化为单 Büchi 族；**`gnba_state_for_nba_state`** 供乘积时取标签。

详见 `GNBA.py` 内注释与表格字段。

---

## `ltl_formula` 包（摘要）

| 模块 | 作用 |
|------|------|
| `__init__.py` | 导出 `parse_ltl`、`load_ts_file`、`load_benchmark_file`、`TransitionSystem`、`BenchmarkSpec` 等 |
| `ast.py` | `Formula` 树、`intern_formula`、`format_formula` |
| `ts_io.py` | `TS.txt` 解析与校验 |
| `benchmark_io.py` | `benchmark.txt`：`A B`、全局行、`i φ` |
| `antlr_parse.py` / `antlr_visitor_impl.py` | ANTLR 解析；依赖 **`ltl_formula/generated/`** |
| `util.py` | `strip_state_prefix`（手写行处理时可用；完整文件请用 `benchmark_io`） |

生成解析器：在仓库根执行 **`bash tools/generate_antlr_parser.sh`** 或 **`./run.sh --gen-antlr`**（需 Java 与 jar）。

---

## 文法

- **`grammars/LTL.g4`**：顶层 **`formula`** 为 **`untilExpr EOF`**；括号内为 **`untilExpr`**，避免误用需 `EOF` 的 `formula` 规则。  
- 命题 **`ID`**：`[a-z][a-z0-9_]*`，与 README 中小写原子及 TS 中 `a b c` 一类名字一致。

---

若评测数据与 README / `Input_Format.pdf` 有新字段或边界情况，以官方说明为准，再扩展 `ts_io` / `benchmark_io` / `LTL.g4`。
