"""import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

query = 
SELECT
    email AS AFTER_EMAIL
FROM
    users
WHERE
    Id = 20

cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row[0])  # Access the first (and only) column in the row

# Close the cursor and the database connection
cursor.close()
conn.close()
"""
