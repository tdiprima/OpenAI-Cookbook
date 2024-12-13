# OpenAI-recipes

This repository mainly follows examples and ideas from the [OpenAI Dashboard](https://platform.openai.com/chat-completions) and the [Playground](https://platform.openai.com/playground/chat?models=gpt-4o).

## Notes

- Most markdown files were generated with the help of LLMs.
- This project is being updated to align with changes introduced in newer versions of the OpenAI Python SDK. These updates ensure compatibility with the latest API endpoints, take advantage of new features, and follow best practices recommended by OpenAI.

### Migration Details

While following the [OpenAI Python migration guide](https://github.com/openai/openai-python/discussions/742), I encountered an issue:

  - The `openai migrate` command didn't work as expected and pointed to an incorrect URL.

### Steps I used to resolve the migration issue:

1. Install Grit by running:

   ```sh
   curl -fsSL https://docs.grit.io/install | bash
   ```

2. Use Grit to apply the [OpenAI migration](https://github.com/openai/openai-python/issues/1838#issuecomment-2457972838):

   ```sh
   source $HOME/.grit/bin/env
   grit apply openai
   ```

These steps successfully resolved the migration issue.

<br>
