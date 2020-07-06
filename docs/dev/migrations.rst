Database Migrations
===================

The database management interface is available on the command line:

..

    SETTINGS=$PWD/usr/conf/dev.conf src/scripts/gthnk db

New Migration
-------------

To create a new Migration:

1. Drop the dev database.  We need to start fresh.
2. Upgrade from blank to the latest migration state.
3. Build the new migration, which is based on how current object state differs from the previous migration.
4. Edit the 

..

    make drop_db
    make upgradedb
    make migratedb

Edit the file created in src/gthnk/migrations/versions.

SQLite3 does not support ALTER TABLE ... DROP COLUMN.  So, comment out the following:

- op.drop_column
- op.drop_constraint
- op.alter_column

In addition, edit downgrade() to remove any corresponding commands - even if they are supported (like add column).

