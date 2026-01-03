import difflib
import web_skills
import gemini_engine

class CommandManager:
    def __init__(self):
        self.commands_map = {
            "open chrome": "chrome",
            "open notepad": "notepad",
            "open calculator": "calc",
            "open editor": "notepad",
            "open browser": "chrome",
            "open youtube": "https://www.youtube.com",
            "open inbox": "https://mail.google.com",
            "whats in my inbox": "https://mail.google.com",
            "check email": "https://mail.google.com",
            "go to sleep": "SLEEP",
            "stop listening": "SLEEP",
            "goodbye": "SLEEP"
        }

    def execute_command(self, command):
        command = command.lower().strip()
        print(f"Processing command: '{command}'")

        # Special internal commands
        if "go to sleep" in command or "stop listening" in command or "goodbye" in command:
             print("Assistant going to sleep. Say 'Hey PC' to wake me.")
             return "SLEEP"

        # 0. Check for explicit "Search for..." intent
        # This is a basic rule-based way to handle search until we have AI
        if command.startswith("search for") or command.startswith("google"):
            query = command.replace("search for", "").replace("google", "").strip()
            if query:
                web_skills.search_google(query)
                return
            
        target = None
        
        # 1. Direct exact match
        if command in self.commands_map:
            target = self.commands_map[command]
        
        # 2. Keyword fallback (simple search)
        if not target:
            if "chrome" in command: target = "chrome"
            elif "notepad" in command: target = "notepad"
            elif "calculator" in command: target = "calc"
            elif "youtube" in command: target = "https://www.youtube.com"
            elif "inbox" in command or "email" in command: target = "https://mail.google.com"

        # 3. Fuzzy match fallback
        if not target:
            possible_commands = list(self.commands_map.keys())
            matches = difflib.get_close_matches(command, possible_commands, n=1, cutoff=0.5)
            if matches:
                best_match = matches[0]
                print(f"Fuzzy matched '{command}' to '{best_match}'")
                target = self.commands_map[best_match]

        # Execute
        if target:
            if target.startswith("http"):
                web_skills.open_url(target)
            else:
                import subprocess
                subprocess.Popen(target)
                print(f"Opening System App: {target}")
        else:
            # 4. Gemini AI Fallback
            print("No direct/fuzzy match found. Consulting Gemini AI...")
            ai_intent = gemini_engine.get_intent_ai(command)
            
            if ai_intent.get("type") == "OPEN_APP":
                target = ai_intent.get("target", "").lower()
                print(f"Gemini suggests Opening App: {target}")
                # Recurse once with the corrected target name or just execute
                # To be safe, we check if the AI target is in our known map
                if target in self.commands_map:
                    resolved = self.commands_map[target]
                    if resolved.startswith("http"): web_skills.open_url(resolved)
                    else: 
                        import subprocess
                        subprocess.Popen(resolved)
                else:
                    # AI suggested something not in our map (e.g. "itunes" or "spotify")
                    # We can try to run it directly if it sounds like an app
                    try:
                        import subprocess
                        subprocess.Popen(target)
                    except:
                        print(f"Could not open AI-suggested app: {target}")

            elif ai_intent.get("type") == "SEARCH":
                query = ai_intent.get("target")
                print(f"Gemini suggests Web Search: {query}")
                web_skills.search_google(query)
            
            elif ai_intent.get("type") == "ERROR":
                print(f"Gemini Error: {ai_intent.get('target')}")
                if "API Key" in ai_intent.get("target"):
                    print("Please set your GEMINI_API_KEY environment variable.")
            else:
                print("Command not recognized by manager or AI.")

