-- Synthetic SQLite review inputs. Execute only in an isolated in-memory database.
-- Contract: business_no is unique within a tenant; another tenant may reuse it.
-- amount is a synthetic integer quantity, not a real currency / precision policy.
CREATE TABLE protected_orders (
    id INTEGER PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    business_no TEXT NOT NULL,
    amount INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    UNIQUE (tenant_id, business_no)
);

INSERT INTO protected_orders VALUES
    (1, 7, 'ORDER-001', 100, 20),
    (2, 7, 'ORDER-002', 200, 20),
    (3, 8, 'ORDER-001', 300, 20),
    (4, 7, 'ORDER-003', 50, 10);

-- Positive example: id itself is the only confirmed business identity here.
-- PRIMARY KEY covers that identity; adding UNIQUE(id) would be redundant.
-- This says nothing about idempotency of two requests creating different ids.
CREATE TABLE primary_identity_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payload TEXT NOT NULL
);
INSERT INTO primary_identity_orders (payload) VALUES ('synthetic order');
SELECT payload FROM primary_identity_orders WHERE id = 1;
-- A second INSERT with id=1 must fail under the existing PRIMARY KEY alone.

-- Counterexample: a surrogate id does not protect a DIFFERENT business key.
CREATE TABLE unprotected_orders (
    id INTEGER PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    business_no TEXT NOT NULL,
    amount INTEGER NOT NULL
);
CREATE INDEX idx_unprotected_business
    ON unprotected_orders (tenant_id, business_no);
INSERT INTO unprotected_orders VALUES
    (1, 7, 'ORDER-001', 100),
    (2, 7, 'ORDER-001', 100),
    (3, 8, 'ORDER-001', 300);

-- Valid primary-key / unique-key lookup: no ORDER BY or LIMIT required.
SELECT amount FROM protected_orders WHERE id = 1;
SELECT amount FROM protected_orders
    WHERE tenant_id = 7 AND business_no = 'ORDER-001';

-- Invalid uniqueness reasoning: LIMIT 1 hides duplicates and missing tenant scope.
-- A separate, explicitly defined "latest order" operation is a different contract.
SELECT amount FROM unprotected_orders WHERE business_no = 'ORDER-001' LIMIT 1;

-- Single-row aggregate: its scan cost still depends on scope and data volume.
SELECT COUNT(*) AS order_count, SUM(amount) AS amount_sum
    FROM protected_orders WHERE tenant_id = 7;

-- GROUP BY is multi-row; whether it needs paging depends on actual output bounds.
SELECT tenant_id, SUM(amount) AS amount_sum
    FROM protected_orders GROUP BY tenant_id;

-- Valid stable order for this static-data fixture, including equal timestamps.
SELECT id FROM protected_orders WHERE tenant_id = 7
    ORDER BY created_at DESC, id DESC LIMIT 2;
SELECT id FROM protected_orders
    WHERE tenant_id = 7 AND (created_at < 20 OR (created_at = 20 AND id < 1))
    ORDER BY created_at DESC, id DESC LIMIT 2;

-- Counterexample: same correct total order, WRONG continuation condition.
-- Last position is (created_at=20,id=1). id-only filtering loses older row id=4.
SELECT id FROM protected_orders WHERE tenant_id = 7 AND id < 1
    ORDER BY created_at DESC, id DESC LIMIT 2;

-- Counterexample: equal timestamps do not define a stable order between rows.
SELECT id FROM protected_orders WHERE tenant_id = 7
    ORDER BY created_at DESC LIMIT 2;
