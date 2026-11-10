# Cheat sheet: choosing storage and databases

Use when a learner asks where to store data, or a question hinges on that choice. Verify any detail you cite against the linked page.

## Decision order

1. **Unstructured files, backups, media, data lake?** → **Cloud Storage**, then pick a class by access frequency.
2. **Disk for a VM?** → **Persistent Disk / Hyperdisk** (zonal; regional for synchronous replication across two zones). Shared POSIX file system for several VMs or GKE Pods → **Filestore**.
3. **Relational and transactional (OLTP)?**
   - Regional, standard MySQL / PostgreSQL / SQL Server → **Cloud SQL**.
   - PostgreSQL-compatible with higher performance and analytics on live data → **AlloyDB**.
   - Global scale, horizontal scaling, strong consistency, very high availability → **Spanner**.
4. **NoSQL?**
   - Documents for web and mobile apps, offline sync, serverless → **Firestore**.
   - Very high throughput, low-latency key/wide-column (time series, IoT, ad tech), large volumes → **Bigtable**.
5. **Analytics with SQL over large datasets (OLAP)?** → **BigQuery**.
6. **In-memory cache or session store?** → **Memorystore**.

## Cloud Storage classes

| Class | Use for |
|---|---|
| Standard | Frequently accessed ("hot") data |
| Nearline | Accessed about once a month or less |
| Coldline | Accessed about once a quarter or less |
| Archive | Accessed less than once a year; long-term retention |

Minimum storage durations per class are in [facts.md](facts.md).

Colder classes cost less to store and more to retrieve. Use **Object Lifecycle Management** to move or delete objects by age, and **Autoclass** to let Cloud Storage manage classes automatically.

## Common traps

- BigQuery is not a transactional database; Cloud SQL is not a petabyte analytics engine.
- "Global" plus "relational" plus "strong consistency" points to Spanner, not Cloud SQL with replicas.
- Bigtable is not a fit for small datasets or ad hoc SQL joins.
- Read replicas scale reads; **high availability** (regional) configuration is what gives automatic failover in Cloud SQL.
- Regional Persistent Disk protects against a zone failure, not against accidental deletion: you still need snapshots.

## Documentation

- Cloud Storage classes: https://docs.cloud.google.com/storage/docs/storage-classes
- Disks for Compute Engine: https://docs.cloud.google.com/compute/docs/disks
- Filestore: https://docs.cloud.google.com/filestore/docs/overview
- Cloud SQL: https://docs.cloud.google.com/sql/docs/introduction
- AlloyDB: https://docs.cloud.google.com/alloydb/docs/overview
- Spanner: https://docs.cloud.google.com/spanner/docs
- Firestore: https://docs.cloud.google.com/firestore/native/docs/overview
- Bigtable: https://docs.cloud.google.com/bigtable/docs/overview
- BigQuery: https://docs.cloud.google.com/bigquery/docs/introduction
- Memorystore for Redis: https://docs.cloud.google.com/memorystore/docs/redis/memorystore-for-redis-overview
- Storage and database options (Architecture Center): https://docs.cloud.google.com/architecture/storage-advisor
