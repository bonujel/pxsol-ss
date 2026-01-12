# pxsol-ss 项目指令

## 项目简介

Solana 链上数据存储器程序（纯 Rust 实现）

---

## Solana 程序设计哲学

### 核心理念

> **链上程序 = 状态机**
>
> 功能取决于你如何解释数据

```
当前状态 (Account Data) + 输入 (Instruction) → 程序 → 新状态 (Account Data)
```

### 三步设计法

#### 步骤 1：设计数据格式

先定义账户中存储什么数据：

```rust
// 简单设计：原样存储
PDA Data = 任意字节序列

// 复杂设计：结构化数据
#[derive(BorshSerialize, BorshDeserialize)]
struct UserProfile {
    name: String,
    balance: u64,
    is_active: bool,
}
```

#### 步骤 2：设计指令

定义程序支持的操作：

```rust
// 简单设计：单一指令，通过状态判断行为
if account.lamports == 0 { create } else { update }

// 复杂设计：枚举指令类型
enum Instruction {
    Initialize,
    Update { data: Vec<u8> },
    Delete,
}
```

#### 步骤 3：明确账户列表

确定每个指令需要的账户及权限：

```rust
// 账户权限标记
// s = signer (签名者)
// w = writable (可写)
// r = readonly (只读)

// pxsol-ss 账户列表
accounts[0] = user        // sw - 付款、授权
accounts[1] = pda         // w  - 存储数据
accounts[2] = system      // r  - CPI 调用
accounts[3] = rent        // r  - 获取租金信息
```

### 设计原则

| 原则 | 说明 |
|------|------|
| 数据即状态 | 账户数据 = 程序的全部状态 |
| 解释即功能 | 同样的字节，不同解释 = 不同功能 |
| 显式优于隐式 | 所有账户依赖必须明确传入 |

---

## 代码风格

### 1. 账户获取方式

**必须使用迭代器方式：**
```rust
let accounts_iter = &mut accounts.iter();
let account_user = solana_program::account_info::next_account_info(accounts_iter)?;
```

**禁止直接索引：**
```rust
// ❌ 不要这样写
let account_user = &accounts[0];
```

### 2. 类型注解

**避免不必要的显式类型注解：**
```rust
// ✅ 推荐：让编译器推断
let account_user = next_account_info(accounts_iter)?;

// ❌ 避免：冗余的类型注解
let account_user: &AccountInfo<'_> = next_account_info(accounts_iter)?;
```

只在编译器无法推断时才显式注解。

### 3. 错误处理

- 使用 `?` 操作符传播错误
- 避免 `unwrap()`，除非绝对确定不会失败
- 优先返回有意义的错误类型

### 4. 命名规范

- 账户变量：`account_` 前缀（`account_user`, `account_data`）
- PDA 相关：`bump_seed`, `pda_address`
- 常量：大写蛇形命名 `SEED_PREFIX`

### 5. 注释语言

- 代码注释使用英文
- 保持与现有代码库一致

---

## 项目结构

```
pxsol-ss/
├── Cargo.toml              # 项目配置
├── src/
│   └── lib.rs              # 链上程序入口
├── tests/
│   ├── config.py           # 网络配置（支持 localhost/devnet 切换）
│   ├── test_write.py       # 写入测试
│   ├── test_read_pda.py    # 读取测试
│   ├── test_update_pda.py  # 更新测试
│   └── test_upgrade.py     # 升级测试
└── target/deploy/          # 编译产物 (.so)
```

## 常用命令

```bash
# 编译程序
cargo build-sbf

# 部署程序
solana program deploy target/deploy/pxsol_ss.so

# 运行测试 (需要 pxsol-py311 环境)
conda activate pxsol-py311

# 本地网络测试（默认）
python tests/test_write.py

# Devnet 测试
SOLANA_NETWORK=devnet python tests/test_write.py
SOLANA_NETWORK=devnet python tests/test_read_pda.py
```

## 部署信息

| 环境 | Program ID |
|------|------------|
| Localhost | `84Jd3TkNgmw3ibXArJW6DLj3qVATqp7pmeTkpBsVdT8U` |
| Devnet | `84Jd3TkNgmw3ibXArJW6DLj3qVATqp7pmeTkpBsVdT8U` |
