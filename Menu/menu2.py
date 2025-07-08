import re
import json
import os
import subprocess
import google.generativeai as genai

# === CONFIG ===
COMMAND_DB_PATH = "commands.json"
genai.configure(api_key="")  # <-- Replace this

model = genai.GenerativeModel("gemini-2.5-pro")  # Use the appropriate model

# === Load and Save Cache ===

def load_command_cache():
    if not os.path.exists(COMMAND_DB_PATH):
        return {}
    with open(COMMAND_DB_PATH, "r") as f:
        return json.load(f)

def save_command_cache(cache):
    with open(COMMAND_DB_PATH, "w") as f:
        json.dump(cache, f, indent=2)

# === Generate New Command via Gemini ===

def generate_command_template(user_input):
    prompt = f"""Convert the following user request into a Linux shell command using placeholders in angle brackets.

⚠️ IMPORTANT: Do NOT wrap any part of the command in single (') or double (") quotes.
Only return raw shell commands with placeholder variables like <folder_name>, <hostname>, etc.

Examples:
User: I want to create a folder
Command: mkdir <folder_name>

User: I want to list all files in a folder
Command: ls <folder_path>

User: I want to SSH and run docker ps
Command: ssh <user>@<hostname_or_ip> docker ps -a

Now generate the command:
User: {user_input}
Command:"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return None


# === Handle Placeholder Input ===

def extract_placeholders(command_template):
    return re.findall(r'<(.*?)>', command_template)

def fill_placeholders(command_template):
    placeholders = extract_placeholders(command_template)
    filled_command = command_template
    for placeholder in placeholders:
        value = input(f"Enter value for '{placeholder}': ").strip()
        filled_command = filled_command.replace(f"<{placeholder}>", value)
    return filled_command

# === Run Command ===

def run_shell_command(command_str):
    try:
        print(f"\n📟 Running: {command_str}")
        result = subprocess.run(command_str.split(), text=True, capture_output=True)
        print("\n✅ Output:")
        print(result.stdout if result.stdout else "[No Output]")
        if result.stderr:
            print("\n⚠️ Error:")
            print(result.stderr)
    except Exception as e:
        print(f"\n❌ Error executing command: {e}")

# === Main Interaction ===

def run_new_command(command_cache):
    user_input = input("\n💬 What do you want to do? ").strip()
    if user_input in command_cache:
        print("✅ Command template already known.")
        command_template = command_cache[user_input]
    else:
        command_template = generate_command_template(user_input)
        if command_template:
            command_cache[user_input] = command_template
            save_command_cache(command_cache)
        else:
            print("⚠️ Could not generate command.")
            return

    print(f"\n🔧 Command Template: {command_template}")
    final_cmd = fill_placeholders(command_template)
    run_shell_command(final_cmd)

def run_from_cache(command_cache):
    if not command_cache:
        print("📭 No cached commands yet.")
        return
    print("\n🗂️  Previous Commands:")
    for i, key in enumerate(command_cache.keys(), start=1):
        print(f"{i}. {key}  →  {command_cache[key]}")
    try:
        choice = int(input("Select a command by number: "))
        selected_key = list(command_cache.keys())[choice - 1]
        command_template = command_cache[selected_key]
        print(f"\n🔧 Command Template: {command_template}")
        final_cmd = fill_placeholders(command_template)
        run_shell_command(final_cmd)
    except (ValueError, IndexError):
        print("⚠️ Invalid selection.")

def main():
    command_cache = load_command_cache()

    while True:
        print("\n🧠 Gemini Linux Assistant with Memory")
        print("1. Run a new command from natural language")
        print("2. Choose from previously generated commands")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            run_new_command(command_cache)
        elif choice == '2':
            run_from_cache(command_cache)
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
