# Schema & Relational Guide — Olist

This document details the file structures, primary and foreign keys, and relevant columns needed to perform analytics queries.

---

## 1. Table Schema Summary

| Logical Table | CSV File | Primary Key | Relevant Foreign Keys | Primary Usage |
|---|---|---|---|---|
| **Orders** | `pedido.csv` | `idPedido` | `idCliente` -> `cliente.idCliente` | Order status (`descSituacao`), order date (`dtPedido`) |
| **Customers** | `cliente.csv` | `idCliente` | — | Customer state (`descUF`), city (`descCidade`) |
| **Order Items** | `item_pedido.csv` | (`idPedido`, `idPedidoItem`) | `idPedido` -> `pedido.idPedido`, `idProduto`, `idVendedor` | Item price (`vlPreco`), freight (`vlFrete`) |
| **Payments** | `pagamento_pedido.csv` | (`idPedido`, `numSequencial`) | `idPedido` -> `pedido.idPedido` | Payment type, installments, payment value (`vlPagamento`) |
| **Reviews** | `avaliacao_pedido.csv` | `idAvaliacao` | `idPedido` -> `pedido.idPedido` | Score (`vlNota`), review timestamps |
| **Products** | `produto.csv` | `idProduto` | — | Product category (`descCategoria`) |
| **Sellers** | `vendedor.csv` | `idVendedor` | — | Seller state, city |

---

## 2. Cardinalities & Join Rules

```
pedido (idPedido) [1] ───< [N] item_pedido (idPedido)
pedido (idPedido) [1] ───< [N] pagamento_pedido (idPedido)
pedido (idCliente) [N] >─── [1] cliente (idCliente)
```

- **Order to Customer:** Many-to-One. Each order has exactly one customer purchase record (`idCliente`).
- **Order to Items:** One-to-Many. An order may contain one or multiple items.
- **Order to Payments:** One-to-Many. An order may use multiple vouchers or credit cards.
