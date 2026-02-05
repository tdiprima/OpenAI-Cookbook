// https://www.npmjs.com/package/openai/v/4.8.0
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: process.env["OPENAI_API_KEY"]
});

async function main() {
  const completion = await openai.chat.completions.create({
    messages: [{ role: 'user', content: 'Write a haiku about AI' }],
    model: 'gpt-5.2' // gpt-5.2
  });

  console.log(completion.choices);
}

main();

// Artificial mind
// Learning and adapting fast
// Future now in hand