The ERD represents the database structure used to manage mobile money transactions, users, transaction categories, system logs, and the relationships between them.

The database is designed to efficiently store, query, and analyze transactions while maintaining data integrity and supporting future scalability.

## Entities
# 1. Users

Stores customer information.

user_id (PK)

phone_number

full_name

email

registration_date

account_status

created_at, updated_at

# 2. Transaction_Categories

Stores types of transactions such as Send, Receive, Deposit, Withdraw, and Payment.

category_id (PK)

category_name

description

is_active

created_at

# 3. Transactions

Stores individual transaction records.

transaction_id (PK)

reference

sender_id (FK → Users)

receiver_id (FK → Users)

category_id (FK → Transaction_Categories)

amount

currency

status

transaction_date

description

created_at, updated_at

# 4. System_Logs

Tracks system activity and errors.

log_id (PK)

log_level

log_message

event_type

source_module

error_code

stack_trace

created_at

# 5. User_Logs

Junction table representing the many-to-many relationship between Users and System_Logs.

user_log_id (PK)

user_id (FK → Users)

log_id (FK → System_Logs)

user_action

created_at

Relationships

Users → Transactions:
A user can send or receive many transactions (1:M relationship).

Transaction_Categories → Transactions:
Each transaction belongs to one category (1:M relationship).

Users ↔ System_Logs:
Many-to-many relationship via User_Logs (M:N), representing which users are associated with which logs.
