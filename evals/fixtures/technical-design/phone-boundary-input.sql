-- Synthetic identity-query inputs only, not a migration or production uniqueness policy.
-- Phone strings illustrate matching boundaries, not real-number format/ownership validation.
CREATE TABLE identity_candidates (
    user_id TEXT PRIMARY KEY,
    scope_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    dial_code TEXT NOT NULL,
    national_number TEXT NOT NULL
);
INSERT INTO identity_candidates VALUES
    ('user-A', 'tenant-A', 'site-A', '+1',  '5550100'),
    ('user-B', 'tenant-A', 'site-A', '+44', '5550100'),
    ('user-C', 'tenant-A', 'site-B', '+1',  '5550100'),
    ('user-D', 'tenant-B', 'site-A', '+1',  '5550100'),
    ('user-E', 'tenant-A', 'site-A', '+1',  '5550101'),
    ('user-F', 'tenant-A', 'site-A', '+1',  '5550101');

-- Incomplete legacy lookup: two candidates despite the same trusted scope/source.
SELECT user_id FROM identity_candidates
WHERE scope_id = 'tenant-A' AND source_id = 'site-A' AND national_number = '5550100';

-- Full confirmed lookup boundary: user-B only, not the same national number under +1.
SELECT user_id FROM identity_candidates
WHERE scope_id = 'tenant-A' AND source_id = 'site-A'
    AND dial_code = '+44' AND national_number = '5550100';

-- Dial code alone does not replace the trusted tenant/source boundary: three candidates.
SELECT user_id FROM identity_candidates
WHERE dial_code = '+1' AND national_number = '5550100';

-- No candidate: this is not an existing-user success; follow the confirmed registration path.
SELECT user_id FROM identity_candidates
WHERE scope_id = 'tenant-A' AND source_id = 'site-A'
    AND dial_code = '+1' AND national_number = '5550199';

-- Even all expected filters do not prove data is unique or ownership verified.
SELECT user_id FROM identity_candidates
WHERE scope_id = 'tenant-A' AND source_id = 'site-A'
    AND dial_code = '+1' AND national_number = '5550101';
