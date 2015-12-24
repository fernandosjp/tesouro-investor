import sqlite3

sqlite_file = 'alertInvest.sqlite'    # name of the sqlite database file

# Table with Bonds
#table_bonds = 'bonds'  # name of the table to be created
#new_field = 'my_1st_column' # name of the column

# Table with log of monitoring tasks
table_job_log = 'job_logs'  # name of the table to be created
columns = 'id INTEGER PRIMARY KEY AUTOINCREMENT, date_task TEXT, emailSent BOOLEAN' # name of the column

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 1 column
c.execute('CREATE TABLE {tn} ({nf})'\
        .format(tn=table_job_log, nf=columns))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()