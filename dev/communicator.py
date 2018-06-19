from pyhive import hive

#očitaj ip iz datoteke
with open('ip_value.txt', 'r') as myfile:
    ip=myfile.read().replace('\n', '')

#spoji se na hive
conn = hive.Connection(host=str(ip), port=10000, username="hadoop")

while True:
    #Unos upita 
    query = raw_input("Enter HiveQL query")

    #izvršavanje upita
    cursor = conn.cursor()
    cursor.execute(query)
    
    #ispis podataka
    for result in cursor.fetchall():
        print str(result)
    print("\n\n\n---------------------------------------------\n\n\n")