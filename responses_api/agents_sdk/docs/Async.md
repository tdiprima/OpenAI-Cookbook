### Question: Async—Should It Be Used All the Time Since We're Waiting? When Shouldn't It Be Used?
**Short Answer**: Not always! `Async` is great when you're waiting for something slow (like an LLM response), but you don't *need* it for fast, simple stuff. Use it when waiting matters; skip it when it's instant.

**Why Async?**:

- **Waiting Game**: When the agent talks to the LLM (or a tool that hits the web), it takes time—maybe a second or two. `Async` lets your program do other things while waiting instead of freezing. Think of it like texting a friend and cooking dinner—you don't just stare at your phone till they reply!
- **Your Code**: In the calculator, `Runner.run` is `async` because it's probably chatting with the LLM over the internet. `asyncio.run(main())` runs that async task smoothly.

**When to Use It**:

- **Slow Stuff**: Use `async` when calling the agent, hitting APIs, or doing anything that waits (like `await Runner.run(...)`).
- **Multiple Tasks**: If you want to run *lots* of calculations at once (e.g., 10 inputs in parallel), `async` shines—fire them all off and collect answers as they roll in.

**When *Not* to Use It**:

- **Fast Stuff**: If the task is instant (like `5 + 3` in pure Python with no LLM), `async` is overkill—it adds complexity for no gain. Example: `Runner.run_sync` (from your haiku snippet) is fine for one-off, quick jobs.
- **Simple Scripts**: If you're just testing one thing and don't care about waiting (like "gimme a haiku"), sync is easier—no `async`/`await` dance.
- **No Waiting**: If the agent *didn't* use an LLM and just ran `do_math` locally (unlikely here, but possible), sync would work fine—it's instant.

**Should It Always Be Async?**: Nope! Use `async` when you're dealing with delays (LLM, network, etc.) or multitasking. For quick, local, one-and-done stuff, sync is simpler and just as good.

---

### **Quick Recap**

**Async?**: Use it for slow/waiting stuff (like LLM calls). Skip it for fast, simple tasks where waiting's not a big deal.

---

### **Fun Example to Test It**
Try this sync vs. async tweak:

- **Sync**: `result = Runner.run_sync(calc_agent, "add 5 3")`—blocks till it's done, fine for one quick calc.
- **Async**: `result = await Runner.run(calc_agent, "add 5 3")`—lets you do other stuff while waiting, great for big batches.

<br>
