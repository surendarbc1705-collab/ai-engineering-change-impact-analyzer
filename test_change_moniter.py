from app.change_monitor import get_customers, detect_changes


before = get_customers()

print("Current database:")
print(before)


print("\nNow change Ravi K to Naveen K in the database.")


input("\nPress ENTER after making the database change...")


after = get_customers()

changes = detect_changes(before, after)


print("\nDetected Changes:")

for change in changes:
    print(change)