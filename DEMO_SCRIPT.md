# ResolveMind Demo Script (2 Minutes)

**[0:00 - 0:15] Introduction (Screen: ResolveMind UI, empty state)**
"Welcome to ResolveMind. Today, I'll show you how we solve the 'Goldfish Memory' problem in customer support. Traditional AI agents forget what happened yesterday. ResolveMind uses Vectorize Hindsight to remember everything."

**[0:15 - 0:45] The Problem - Stateless Mode (Screen: Toggle set to Stateless)**
"Let's look at Priya Nair. She's a Pro customer who has had invoice sync failures twice this week. Let's see what happens if she complains again in a standard, stateless agent."
*(Action: Click 'Run Demo' with Stateless toggled ON)*
"The agent apologizes and suggests reconnecting QuickBooks and clearing the cache. The problem? Priya already tried both of those in her last two tickets. She's going to be furious."

**[0:45 - 1:30] The Solution - Hindsight Mode (Screen: Toggle set to Hindsight Memory)**
"Now, let's turn on Hindsight Memory and send the exact same message."
*(Action: Toggle to Hindsight, Click 'Run Demo')*
"Notice the Agent Brain panel on the right. Hindsight immediately recalled her past two tickets. It sees that the reconnect and cache clear *failed*. So, instead of repeating those, it skips them, acknowledges the repeated failure, and automatically escalates to a human tier-2 agent, drafting an email because she prefers email."

**[1:30 - 2:00] The Engine (Screen: Agent Brain Panel)**
"How does this work? It's not just a raw transcript dump. After every chat, ResolveMind uses an extraction step to pull concise, structured facts and stores them in Hindsight using the `retain` API. When a new chat starts, it uses the `recall` API to fetch only the top relevant facts. This keeps the prompt clean, cheap, and highly effective. Thank you!"
