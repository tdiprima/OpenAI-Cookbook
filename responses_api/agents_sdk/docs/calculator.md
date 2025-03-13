Alright, let's whip up a quick calculator using `openai-agents` style! We'll make an agent that can add, subtract, multiply, or divide two numbers based on what you tell it. I'll keep it short, clear, and fun. Since I don't have the exact `openai-agents` library, I'll mimic the structure from your examples and assume it's a framework where agents process inputs based on instructions.

Here's the plan: one agent, clear instructions, and a simple input format. Let's go!

---

### **Calculator Agent Code**

[calculator.py](calculator.py)

### **What's Going On?**
- **Agent Setup**: We made `CalcBot`, a little math whiz. Its instructions tell it how to read your input (like "add 5 3") and what to do with it.
- **Input Format**: You give it `[operation] [number1] [number2]`—super simple, like "multiply 6 2".
- **Output**: It spits out just the number (e.g., `12`) or `Error` if something's funky (like dividing by zero).
- **Runner Magic**: The `Runner.run` part sends your input to the agent and gets the answer back. We're using `async` to keep it snappy.

---

### **Sample Output**
If this works like your examples, you'd see something like:

```
Input: add 5 3 -> Result: 8
Input: subtract 10 4 -> Result: 6
Input: multiply 6 2 -> Result: 12
Input: divide 8 2 -> Result: 4
Input: divide 5 0 -> Result: Error
Input: bad input here -> Result: Error
```

---

### **How to Play With It**
1. **Run It**: Copy-paste this into a Python file (assuming you have the `agents` library). Run it and watch the magic!
2. **Test Your Own**: Change the `inputs` list to stuff like `"add 100 50"` or `"multiply 3 7"`.
3. **Break It**: Try weird inputs like `"divide 10 0"` or `"hello world"`—it'll say `Error`.

---

### **Why This Rocks**
- **Simple**: No messy code—just an agent with a job.
- **Flexible**: You could tweak the instructions to add more operations (like "power" or "mod") later.
- **Fast**: The agent does the thinking, and you get clean answers.

---

### **Level Up (Optional)**
Wanna make it fancier? Add a tool like this:

```python
@function_tool
def do_math(operation: str, num1: float, num2: float) -> str:
    if operation == "add":
        return str(num1 + num2)
    elif operation == "subtract":
        return str(num1 - num2)
    # Add more operations here!
    return "Error"

calc_agent.tools = [do_math]
```

This would let the agent use a custom function instead of relying on its own logic—but for now, the instructions alone should work fine.

<br>
