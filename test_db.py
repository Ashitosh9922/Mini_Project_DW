from db.db_manager import DatabaseConnection


print("===== DATABASE CONNECTION TEST =====")

db1 = DatabaseConnection()
db2 = DatabaseConnection()

print("Same object:", db1 is db2)

conn = db1.connect()

if conn:
    print("Database connection: SUCCESS")
else:
    print("Database connection: FAILED")

db1.close()

print("===== DATABASE TEST COMPLETE =====")