# pxsol-ss 项目指令

## 项目简介

Solana 链上数据存储器程序（纯 Rust 实现）

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

## 项目结构

```
pxsol-ss/
├── Cargo.toml          # 项目配置
├── src/
│   └── lib.rs          # 链上程序入口
└── target/deploy/      # 编译产物 (.so)
```

## 编译命令

```bash
cargo build-sbf
```
