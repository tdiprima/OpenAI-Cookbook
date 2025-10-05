## [Evaluating model performance](https://platform.openai.com/docs/guides/evals)

## **Evaluations**
This section helps you compare model outputs or evaluate their quality against defined metrics.

#### How to Use:
- Define a dataset of prompts and expected responses.
- Use the evaluation API or CLI to score the responses.

#### Example Evaluation Dataset:
```json
[
  {
    "input": "What is 2 + 2?",
    "expected": "4",
    "metadata": {"category": "math"}
  },
  {
    "input": "Explain gravity.",
    "expected": "Gravity is the force by which a planet or other body draws objects toward its center.",
    "metadata": {"category": "physics"}
  }
]
```

#### Evaluation Script:
```python
from openai.evaluation import compare

result = compare(
    model="gpt-4",
    inputs=[
        {"input": "What is 2 + 2?", "expected": "4"},
        {"input": "Explain gravity.", "expected": "Gravity is the force..."}
    ]
)

print(result)
```

<br>
