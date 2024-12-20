import tkinter as tk
import difflib

# Load words from the file and remove duplicates
def load_dictionary(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = {line.strip() for line in file}  # Using a set to automatically remove duplicates
    return sorted(words)

# Auto-correct function using difflib
def auto_correct(word, dictionary):
    match = difflib.get_close_matches(word, dictionary, n=1, cutoff=0.8)
    return match[0] if match else word

class TypingApp:
    def __init__(self, root, dictionary):
        self.root = root
        self.dictionary = dictionary
        self.text_input = tk.Text(root, font=("Helvetica", 15), width=40, height=6)
        self.text_input.pack(pady=20)

        # To store the last word typed and the corrected word
        self.last_word = ""
        self.corrected_word = ""
        self.is_corrected = False
        
        self.text_input.bind("<space>", self.on_space_press)
        self.text_input.bind("<BackSpace>", self.on_backspace_press)
        self.text_input.bind("<KeyRelease>", self.on_key_release)  # Handle key release event

    def get_last_word(self, text):
        """Extract the last word from the given text."""
        words = text.strip().split()
        return words[-1] if words else ""

    def on_space_press(self, event):
        """Handle space press for auto-correction."""
        current_text = self.text_input.get("1.0", tk.END).strip()  # Get full text from the Text widget
        last_word = self.get_last_word(current_text)

        if last_word:
            corrected_word = auto_correct(last_word, self.dictionary)

            if corrected_word != last_word:
                self.last_word = last_word
                self.corrected_word = corrected_word
                self.is_corrected = True

                # Update the text input with the corrected word and a space
                self.text_input.delete("1.0", tk.END)  # Clear current text
                updated_text = current_text[:-len(last_word)] + corrected_word + " "
                self.text_input.insert(tk.END, updated_text)
                return "break"  # Prevent the space from being inserted directly
        
        # Allow normal space if no correction is made
        return None

    def on_backspace_press(self, event):
        """Handle backspace to undo the correction."""
        current_text = self.text_input.get("1.0", tk.END).strip()

        if self.is_corrected:
            # Check if the last word is the corrected word and revert to the original word
            last_word = self.get_last_word(current_text)

            if last_word == self.corrected_word:
                # Revert to the original word and add a space
                updated_text = current_text[:-len(last_word)] + self.last_word + " "
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert(tk.END, updated_text)
                self.is_corrected = False  # Reset correction state
                return "break"  # Prevent the backspace from being handled normally

        # Allow the backspace event to work as usual
        return None

    def on_key_release(self, event):
        """Handle any key release events to update text."""
        # If the backspace key or any other key is pressed, update cursor position
        pass

def main():
    file_path = "all_words.txt"  # Replace with your actual file path
    dictionary = load_dictionary(file_path)

    root = tk.Tk()
    root.title("Hausa Word Typing & Correction")

    app = TypingApp(root, dictionary)

    root.mainloop()

if __name__ == "__main__":
    main()
