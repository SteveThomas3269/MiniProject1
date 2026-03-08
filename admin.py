# admin.py

def menu(adminUID, conn):
    while True:
        print("\n-----------Admin Menu-----------")
        print("1. Platform Statistics")
        print("2. Log Out")
        print("--------------------------------")
        
        usrInput = input("Number: ")
        if not usrInput.isdigit():
            print("\nInvalid option, try again!\n")
            continue
        
        option = int(usrInput)
        match option:
            case 1:
                platformStats(conn)
            case 2:
                break
            case _:
                print("\nInvalid option, try again!")


def platformStats(conn):
    cursor = conn.cursor()

    # 1: Top 5 courses by active enrollment (with ties at position 5) 
    cursor.execute("""
        SELECT cid, title, active_enrollment
        FROM (
            SELECT 
                c.cid, 
                c.title,
                COUNT(e.uid) AS active_enrollment,
                RANK() OVER (ORDER BY COUNT(e.uid) DESC) AS rnk
            FROM courses c
            LEFT JOIN enrollments e 
                ON c.cid = e.cid
                AND e.role = 'Student'
                AND CURRENT_TIMESTAMP BETWEEN e.start_ts AND e.end_ts
            GROUP BY c.cid, c.title
        )
        WHERE rnk <= 5
        ORDER BY active_enrollment DESC;
    """)
    top5 = cursor.fetchall()

    print("\n--- Top 5 Courses by Active Enrollment ---")
    if not top5:
        print("No data available.")
    else:
        print(f"{'cid':<6} {'title':<30} {'active_enrollment'}")
        print("-" * 50)
        for row in top5:
            print(f"{row[0]:<6} {row[1]:<30} {row[2]}")

    # 2: Payment counts per course
    cursor.execute("""
        SELECT 
            c.cid, 
            c.title, 
            COUNT(p.ts) AS payment_count
        FROM courses c
        LEFT JOIN payments p ON c.cid = p.cid
        GROUP BY c.cid, c.title
        ORDER BY payment_count DESC;
    """)
    payments = cursor.fetchall()

    print("\n--- Payment Counts per Course ---")
    if not payments:
        print("No data available.")
    else:
        print(f"{'cid':<6} {'title':<30} {'payment_count'}")
        print("-" * 50)
        for row in payments:
            print(f"{row[0]:<6} {row[1]:<30} {row[2]}")

    cursor.close()

    input("\nPress Enter to return to menu...")
