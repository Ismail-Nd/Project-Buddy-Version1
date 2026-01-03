import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import queue
import threading
import numpy as np
import time
from command_handler import CommandManager

# ---------------- Config ----------------
WAKE_WORD = "hey pc"
WAKE_WORD_ALIASES = ["hey pc", "apc", "hey c", "hey d c", "hp c", "hey he", "hey please", "abc", "hey see"]
SAMPLE_RATE = 16000
BLOCKSIZE = 4000          # Smaller block for faster streaming
COMMAND_TIMEOUT = 4        # Max wait time for a command
SILENCE_THRESHOLD = 1.2    # Seconds of silence to consider command finished
ENERGY_THRESHOLD = 0     # Adjust to your mic/environment
SESSION_TIMEOUT = 20       # Seconds after which the assistant goes back to sleep

# ---------------- Globals ----------------
q = queue.Queue()
active = False
command_buffer = ""
command_start = 0
last_speech_time = 0
model = Model("models/vosk")
command_manager = CommandManager()

# ---------------- Audio Callback ----------------
def audio_callback(indata, frames, time_info, status):
    if status:
        print("Audio Status:", status)

    audio_data = np.frombuffer(indata, dtype=np.int16)
    energy = np.sqrt(np.mean(audio_data**2))

    if energy < ENERGY_THRESHOLD:
        return  # Ignore low-level noise

    q.put(bytes(indata))  # Only valid audio gets sent to recognizer

# ---------------- Command Handler ----------------
# Command logic moved to command_handler.py


# ---------------- Recognition Thread ----------------
def recognition_loop():
    global active, command_buffer, command_start, last_speech_time, model

    # Removed redundant model loading
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    recognizer.SetWords(False)

    print("Recognition started. Listening for wake word...")

    while True:
        try:
            data = q.get(timeout=0.1)  # get audio from queue
        except queue.Empty:
            # handle command timeout
            if active:
                now = time.time()
                silence_exceeded = (now - last_speech_time) >= SILENCE_THRESHOLD
                session_exceeded = (now - command_start) >= SESSION_TIMEOUT

                if session_exceeded:
                    print("Session timed out. Returning to idle...")
                    active = False
                    command_buffer = ""
                elif silence_exceeded and command_buffer.strip():
                    final_command = command_buffer.strip()
                    print("Processing command from buffer:", final_command)
                    result = command_manager.execute_command(final_command)
                    if result == "SLEEP":
                        active = False
                    # Stay active for next command!
                    command_buffer = ""
                    command_start = time.time() # Reset session clock on command
            continue  # go back to queue

        # Feed audio to recognizer
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").lower().strip()
            
            # If we were active and got a final result, try to process it
            if active and text:
                 print("Final result received:", text)
                 result = command_manager.execute_command(text)
                 if result == "SLEEP":
                     active = False
                     command_buffer = ""
                     print("Returning to idle...")
                 else:
                     # Stay active! 
                     command_buffer = ""
                     command_start = time.time() # Reset session clock
                     print("Command processed. Still listening...")
            elif text:
                 print("Final (inactive):", text)
                 # Check for wake word in final result too just in case
                 if any(alias in text for alias in WAKE_WORD_ALIASES):
                     # If the phrase ENDS with the wake word or is JUST the wake word, we wake up.
                     # But sometimes it's "hey pc open notepad" all in one.
                     # Let's try to split.
                     
                     # Simple check: if wake word found, activate
                     print("Wake word detected in Final result.")
                     active = True
                     # usage: "hey pc open notepad" -> active=True, process "open notepad" immediate?
                     # For now, let's just set active and wait for next, OR process remainder if present.
                     # Simplified: Just activate and let the user speak command if it was just wake word.
                     # But if text is "apc open notepad", we should execute.
                     
                     # Find which alias matched
                     matched_alias = next((alias for alias in WAKE_WORD_ALIASES if alias in text), None)
                     if matched_alias:
                         remainder = text.split(matched_alias, 1)[-1].strip()
                         if remainder:
                             print(f"Command included with wake word: {remainder}")
                             result = command_manager.execute_command(remainder)
                             if result == "SLEEP":
                                 active = False
                             else:
                                 # Stay active
                                 command_start = time.time()
                         else:
                             print("Wake word detected. Listening for command...")
                             command_start = time.time()
                             last_speech_time = time.time()

        else:
            partial = json.loads(recognizer.PartialResult())
            partial_text = partial.get("partial", "").lower().strip()
            
            if partial_text:
                print("Heard:", partial_text)
                last_speech_time = time.time()

                # Wake word detection
                if not active:
                    # Check against all aliases
                    if any(alias in partial_text for alias in WAKE_WORD_ALIASES):
                        active = True
                        command_buffer = ""
                        command_start = time.time()
                        print("Wake word detected. Listening for command...")
                        
                        # Optimization: if the partial text is JUST the wake word, we wait.
                        # If it has more, we start buffering.
                        # Need to remove the matched alias
                        matched_alias = next((alias for alias in WAKE_WORD_ALIASES if alias in partial_text), None)
                        remainder = partial_text.replace(matched_alias, "").strip() if matched_alias else partial_text
                        
                        if remainder:
                            command_buffer = remainder
                else:
                    # If active, accumulate/update command buffer
                    # Note: partial_text usually contains the WHOLE phrase since silence
                    # so we don't just append, we replace.
                    # We might want to strip the wake word if it's still in there
                    # Try to strip any alias
                    cleaned_text = partial_text
                    for alias in WAKE_WORD_ALIASES:
                        cleaned_text = cleaned_text.replace(alias, "")
                    command_buffer = cleaned_text.strip()

# ---------------- Main ----------------
def main():
    # Start audio stream
    with sd.RawInputStream(samplerate=SAMPLE_RATE,
                           blocksize=BLOCKSIZE,
                           dtype="int16",
                           channels=1,
                           callback=audio_callback):
        # Start recognition in a separate thread
        threading.Thread(target=recognition_loop, daemon=True).start()
        print("Voice assistant running. Say 'Hey PC' (or 'apc', 'hey c', etc) to activate.")
        # Keep main thread alive
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()
