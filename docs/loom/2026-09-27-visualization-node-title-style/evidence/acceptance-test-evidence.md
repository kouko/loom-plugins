# Acceptance Test Evidence for 2026-09-27-visualization-node-title-style

## Acceptance Line #1: Generator output with structured nodes

### Flow generator with dict-form structured nodes
```
┌────────────────┐
│ 收到訂單       │
├────────────────┤
│ 確認付款狀態   │
│ 檢查庫存可用性 │
└────────────────┘
         │
         ▼
┌────────────────┐
│ 處理付款       │
├────────────────┤
│ 驗證信用卡     │
│ 完成扣款       │
│ 發送確認郵件   │
└────────────────┘
         │
         ▼
┌────────────────┐
│ 出貨           │
├────────────────┤
│ 打包商品       │
│ 安排物流       │
│ 更新追蹤編號   │
└────────────────┘
```
Alignment check: ✓ no drift

### Flow generator with long prose wrapping (width=40)
```
┌──────────────────────────────────────────┐
│ Order Received                           │
├──────────────────────────────────────────┤
│ This is a very long description that     │
│ should wrap inside the box at the width  │
│ budget rather than extending the box     │
│ width infinitely.                        │
└──────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────┐
│ Payment Processing                       │
├──────────────────────────────────────────┤
│ Validate credit card information with the│
│ payment gateway                          │
│ Complete the fund transfer               │
│ Send confirmation email to customer      │
└──────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────┐
│ Shipping                                 │
├──────────────────────────────────────────┤
│ Package the items securely               │
│ Arrange logistics with carrier           │
│ Update tracking number in system         │
└──────────────────────────────────────────┘
```
Alignment check: ✓ no drift

### Architecture generator with structured layer names
```
┌─────────────────────────────────┐
│ Presentation Layer              │
├─────────────────────────────────┤
│ Web App                         │
│ Mobile App                      │
│ Desktop App                     │
├──────────────┬──────────────────┤
│ Frontend     │ API Gateway      │
└──────────────┴──────────────────┘
┌─────────────────────────────────┐
│ Business Logic                  │
├─────────────────────────────────┤
│ Order Service                   │
│ Payment Service                 │
│ Inventory Service               │
├───────────────┬─────────────────┤
│ Service Mesh  │ Message Queue   │
└───────────────┴─────────────────┘
┌─────────────────────────────────┐
│ Data Layer                      │
├─────────────────────────────────┤
│ PostgreSQL                      │
│ Redis Cache                     │
│ S3 Storage                      │
├──────────┬───────┬──────────────┤
│ Database │ Cache │ Object Store │
└──────────┴───────┴──────────────┘
```
Alignment check: ✓ no drift

### Tree generator with structured nodes
```
訂單系統
核心業務系統
處理客戶訂單的主要服務
├─ 訂單服務
│  建立訂單
│  更新狀態
│  處理付款
│  ├─ 訂單建立
│  │  驗證商品
│  │  計算總價
│  │  寫入資料庫
│  └─ 狀態更新
│     接收事件
│     更新記錄
│     觸發通知
└─ 庫存サービス
   在庫管理
   商品の在庫数を追跡するサービス
   ├─ 在庫追跡
   │  商品の受領
   │  出荷処理
   │  在庫調整
   └─ 在庫調整
      棚卸し
      實績との差異
      修正処理
```
Alignment check: ✓ no drift

### String input with \n treated as structured node
```
┌────────────────┐
│ 收到訂單       │
├────────────────┤
│ 確認付款狀態   │
│ 檢查庫存可用性 │
└────────────────┘
         │
         ▼
┌────────────────┐
│ 處理付款       │
├────────────────┤
│ 驗證信用卡     │
│ 完成扣款       │
│ 發送確認郵件   │
└────────────────┘
         │
         ▼
┌────────────────┐
│ 出貨           │
├────────────────┤
│ 打包商品       │
│ 安排物流       │
│ 更新追蹤編號   │
└────────────────┘
```
Alignment check: ✓ no drift

## Acceptance Line #2: Templates adopt node structure

All Mermaid examples in templates validate successfully:
- templates/01-option-comparison.md:53 - OK
- templates/02-linear-steps.md:60 - OK
- templates/03-branching-decision.md:53 - OK
- templates/04-reasoning-chain.md:68 - OK
- templates/05-state-lifecycle.md:48 - OK
- templates/06-actor-sequence.md:53 - OK
- templates/07-hierarchy.md:46 - OK
- templates/08-system-architecture.md:62 - OK
- templates/09-data-model.md:31 - OK
- templates/10-timeline.md:41 - OK
- templates/11-quantity.md:45 - OK

## Acceptance Line #3: Node-structure rule documentation and verification

### Node structure documented in references/node-structure.md
- Structure: Title line, in-box separator row, body
- Body forms: Wrapped prose, bullet lines
- Separator and bullet marks: ASCII separator `├───┤`, bullets `* `
- Left alignment: Title and body left-aligned
- Container/content rule: One-word node expanded or removed, never empty separator
- Width budget: Wraps at width budget (default 40) or explicit width
- Scope A: Applies to box-drawn nodes (flow, arch, tree, hierarchy)
- Mermaid counterpart: Uses page-mode div-label convention

### Verify flow flags deviations

**Unstructured multi-line box (multiple content lines without separator):**
```
┌────────────────┐
│ Line 1         │
│ Line 2         │
│ Line 3         │
└────────────────┘
```
Issues detected:
- line 3: col 1: box interior with two or more content lines in title part and no separator row between them
- line 4: col 1: box interior with two or more content lines in title part and no separator row between them

**Empty separator (separator immediately followed by bottom border):**
```
┌────────────────┐
│ Title          │
├────────────────┤
└────────────────┘
```
Issue detected:
- line 3: col 0: separator row with no content line after it before box's bottom border

## Acceptance Line #4: Non-box text slots stay single-line

### Seq generator rejects multi-line input
- Participant name with line break: `ValueError: line break not supported in participant name: 'Step 1\nLine 2'`
- Message label with line break: `ValueError: line break not supported in message label: 'test\nline2'`

### Bar generator rejects multi-line input
- Bar label with line break: `ValueError: bar label must be single-line, got line break in 'Bar 1\nLine 2'`

### Single-line strings still render centered (not structured)
```
┌──────────────────┐
│ Single line step │
└──────────────────┘
          │
          ▼
┌──────────────────┐
│   Another step   │
└──────────────────┘
```
Alignment check: ✓ no drift

## Acceptance Line #5: Repository package test suite passes

```
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID

Results: 2402 passed, 2 skipped in 77.92s
...
Summary: All test suites pass
```

All tests pass across all loom-family packages (loom-code, loom-design, loom-workflow).