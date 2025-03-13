Let's mash the "Level Up" tool into the calculator code and figure out how it knows when to use it! I'll keep it short and clear—big picture first, then the details. The tool will handle the math, and the agent will decide when to call it based on the input. Here's the updated code, followed by the "how it knows" explanation.

---

### **Updated Calculator with Tool**

[calculator1.py](calculator1.py)

### **What Changed?**
- **Tool Added**: We slapped `do_math` into the code with `@function_tool` and gave it the full math logic (add, subtract, multiply, divide, plus error handling for division by zero).
- **Agent Instructions Updated**: Told `CalcBot` to use `do_math` by passing the operation and numbers from the input.
- **Tools List**: Added `tools=[do_math]` so the agent knows it has this superpower.

---

### **How/When Does It Know to Call the Tool?**
Here's the fun part! The agent doesn't just randomly use the tool—it's smart about it. Think of it like this:

1. **Input Comes In**: You say "add 5 3". The agent reads it and sees the format: `[operation] [number1] [number2]`.
2. **Instructions Kick In**: The agent's brain (its instructions) says, "Oh, I need to calculate this! I've got a `do_math` tool for that."
3. **Tool Trigger**: The agent decides to call `do_math` because:
   - The instructions explicitly say "use the `do_math` tool" for calculations.
   - The input matches the pattern it's expecting (operation + two numbers).
   - The `openai-agents` framework is built to recognize when an agent's instructions mention a tool and the task fits (this is usually handled behind the scenes by the library—magic!).
4. **Tool Runs**: It sends `operation="add"`, `num1=5`, `num2=3` to `do_math`, gets `8` back, and returns it.
5. **No Match, No Tool**: If you say "bad input here", the agent can't parse it into the right format, so it skips the tool and returns "Error" (based on the instructions).

---

### **When Does It *Not* Use the Tool?**
- If the input's garbage (e.g., "hello world"), the agent won't even try `do_math`—it'll see the mismatch and bail with "Error".
- If the operation isn't supported (e.g., "power 2 3"), `do_math` itself returns "Error".

---

### **Why This Rocks**
- **Agent Smarts**: The agent decides when to use the tool based on its instructions—no extra code needed to force it.
- **Tool Power**: `do_math` handles the nitty-gritty math and errors, keeping the agent focused on "what" not "how".
- **Clean Output**: You still get just the number or "Error"—no fluff.

---

### **Test It Out**
Run this bad boy, and it'll handle all the inputs like a champ. Wanna add "power" or "mod"? Just tweak `do_math` and update the instructions—boom, instant upgrade!

<br>
