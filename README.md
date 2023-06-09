# CapstoneProject
Final capstone project to manage an ETL process for a Loan Application dataset and a Credit Card dataset using Python (Pandas, advanced modules, Matplotlib), SQL, Apache Spark (Spark Core, Spark SQL),
and Python Visualization and Analytics libraries.

Challenges:
The mysql.connector I was using did not work properly work with Pandas and after researching the issues, I found out that 
using the sqlalchemy engine worked better with Pandas. Making that switch resolved the connection issues and eliminated the warning messages
that were constantly being generated. 