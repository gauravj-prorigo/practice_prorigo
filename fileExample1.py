# Step 1: Write initial content
with open("Pratice.txt", "w") as f:
    f.write("Hi my name is gaurav\n doing internship java at prorigo\n as a SDE\nI love Java programming")

# Step 2: Read the content
with open("Pratice.txt", "r") as f:
    data = f.read()

# Step 3: Replace "Java" with "python"
new_data = data.replace("Java", "python")

# Step 4: Write the updated content back
with open("Pratice.txt", "w") as f:
    f.write(new_data)
