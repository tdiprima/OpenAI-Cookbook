Alright, let's level up the calculator by adding the `do_math` tool! I'll weave it into the main code and explain how the agent knows when to use it. The tool will handle the actual math, and the agent will decide when to call it based on its instructions.

Here's the updated code with the tool baked in:

### Calculator Agent with Tool

[calculator1.py](calculator1.py)

### What Changed?

**Added the Tool:** The `do_math` function is now a `@function_tool`. It takes operation, num1, and num2, does the math, and returns a string (or "Error" if something's off—like division by zero).

**Agent Instructions:** Updated to tell CalcBot to use the `do_math` tool instead of figuring out the math itself.

**Tool Attached:** The `tools=[do_math]` line hooks the tool up to the agent.

### How Does It Know When to Call the Tool?
Here's the fun part:

**Instructions Rule:** The agent reads its instructions: "Use the `do_math` tool to calculate the result." It's like a lightbulb—whenever it sees an input like "add 5 3", it knows it's math time and looks for a tool to help.

**Pattern Matching:** The agent (thanks to the `openai-agents` magic) parses the input (e.g., "multiply 6 2") into operation="multiply", num1=6, num2=2. It's smart enough to spot the format we told it to expect.

**Tool Trigger:** Since we gave it the `do_math` tool and said "use it," the agent automatically calls `do_math(operation, num1, num2)` when it needs to compute something. It's not guessing—it's following the playbook!

**No Tool, No Go:** If the input's junk (like "bad input here"), the agent might try the tool, but `do_math` will return "Error" because it can't match the operation or numbers.

This all happens behind the scenes with `Runner.run`—it's like the agent's brain saying, "Tool time!" based on the instructions.

### When Does It Call the Tool?

**Good Input:** For stuff like "add 5 3

<br>
