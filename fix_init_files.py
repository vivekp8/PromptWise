import os

module_dirs = [
    "Chat_Session_Management",
    "Export_Integration_System",
    "Prompt_Engine",
    "Security_Access_Control"
]

for module in module_dirs:
    init_path = os.path.join(module, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            f.write("# Package initializer")
        print(f"✅ Created: {init_path}")
    else:
        print(f"✔️ Already exists: {init_path}")