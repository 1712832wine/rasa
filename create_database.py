import sqlite3
# con = sqlite3.connect('database.sqlite3')
# cur = con.cursor()

# # Create table
# cur.execute(
#     '''CREATE TABLE medical_records(user_name, user_gender, user_age, password, diagnoses, date)''')


# # Save (commit) the changes
# con.commit()

# # We can also close the connection if we are done with it.
# # Just be sure any changes have been committed or they will be lost.
# con.close()


con = sqlite3.connect('database.sqlite3')
cur = con.cursor()

# Create table
cur.execute(
    'DELETE FROM medical_records')


# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
