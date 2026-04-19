# OctoPi — Baseline Evaluation
**Model:** llama-3.3-70b-versatile (via Groq)  
**Notes used:** DSA short text (see test_set.md)

---

## Instructions
Run OctoPi with the DSA notes from test_set.md and fill in the results below.
Be honest — this is your benchmark to improve against on Days 4 and 5.

---

## 1. Flashcard Quality

Generate 8 flashcards and check how many cover topics from the test set.

| Metric | Result |
|--------|--------|
| Cards generated | 8 / 8 | 
| Cards directly relevant to notes | 8 / 8 | 
| Cards with accurate answers | ___ / 8 |
| Cards that felt too vague or off-topic | ___ |
| **Overall score** | ___ / 8 |

**Notes / observations:**
> _(e.g. "Card 3 was about sorting but answer was wrong", "missed Hash Tables entirely")_

---

## 2. Quiz Accuracy (Multiple Choice)

Run a 5-question MC quiz. Compare answers to Section B of test_set.md.

| Question | OctoPi Answer | Expected | Correct? |
|----------|--------------|----------|----------|
| Q1 | | | ✅ / ❌ |
| Q2 | | | ✅ / ❌ |
| Q3 | | | ✅ / ❌ |
| Q4 | | | ✅ / ❌ |
| Q5 | | | ✅ / ❌ |

**MC Accuracy:** 5 / 5

---

## 3. Quiz Accuracy (True / False)

Run a 5-question T/F quiz. Compare to Section C.

| Question | OctoPi Answer | Expected | Correct? |
|----------|--------------|----------|----------|
| Q1 | | | ✅ / ❌ |
| Q2 | | | ✅ / ❌ |
| Q3 | | | ✅ / ❌ |
| Q4 | | | ✅ / ❌ |
| Q5 | | | ✅ / ❌ |

**T/F Accuracy:** 5 / 5

---

## 4. Chat Quality

Ask these 3 questions and rate the response (1–5):

| Question | Rating (1–5) | Notes |
|----------|-------------|-------|
| "What is the difference between BFS and DFS?" | | |
| "Explain Big O notation simply" | | |
| "What are the main operations of a stack?" | | |

**Average chat quality:** 5 / 5

**Notes / observations:**
> _(Octo gave very detailed explanations here is an example for the second question on Big O notation: 
    Big O Notation is like a secret code that helps us understand how fast an algorithm (or a recipe for solving a problem) can work. It's all about measuring how long it takes for an algorithm to finish, compared to the size of the problem it's trying to solve.
    Think of it like cooking a meal for a party. If you're cooking for 10 people, it might take 30 minutes. But if you're cooking for 100 people, it might take much longer! Big O Notation helps us understand how much longer it will take.

    Here's a simple way to think about it:

        - O(1) is like making a sandwich. It takes the same amount of     time, no matter how many people you're making sandwiches for.
        - O(n) is like making a sandwich for each person. If you have 10 people, it takes 10 times as long. If you have 100 people, it takes 100 times as long.
        - O(n²) is like making a sandwich for each person, and then making another sandwich for each pair of people. It gets really slow, really fast!

The lower the Big O Notation, the faster the algorithm. So, O(1) is super fast, while O(n²) is much slower.

As an octopus, I like to think of it like swimming through a school of fish. If I can find a fish in O(1) time, I can catch it quickly! But if it takes O(n) time, I have to swim through the whole school to find it.

Does that make sense?)_


---

## 5. PDF Upload Test

Upload a PDF and confirm the content is being read correctly.

| Test | Result |
|------|--------|
| PDF uploaded successfully | ✅ / ❌ |
| Text extracted from PDF | ✅ / ❌ |
| Chat answers based on PDF content | ✅ / ❌ |
| Flashcards generated from PDF | ✅ / ❌ |

---

## Summary

| Feature | Score |
|---------|-------|
| Flashcard relevance | 8 / 8 |
| MC quiz accuracy | 5 / 5 |
| T/F quiz accuracy | 5 / 5 |
| Chat quality | 5 / 5 |
| PDF pipeline | 0 / 4 |
| **Total** | ___ / 27 |

**Target for Day 5:** 22+ / 27

---

## Known Issues (Day 3)
- [ ] _(fill in any bugs you noticed during testing)_
- [ ] _(The overall UI and layout of all the components of the app need improvement)_
- [ ] _(Haven't found a pdf yet for testing)_
- [ ] _(The quiz mode has an error, where the slider does not allow greater than four cards and only after the type of question is unselected or the slider is clicked again does it geenrate the cards)_
- [ ] _(Possible to either include an option to determine how many flashcards can be generated or change the hard coded value)_
- [ ] _(For now the model is doing well with the chat flashcards and quiz features, but there is room for improvement especially with the UI)_
- [ ] _(color match and contrast issue with the light and dark theme toggle, as well consistency between the app,py toggle and the study.py toggle)_
- [ ] _(A better idea would be to remove the light/dark theme toggle entirely and just have a consistent dark theme to match the sea theme - this gives better consistency across both pages and eradicates the issue of contrast issues when switching to light mode for certain elements across the pages, additionally a dark theme is considered easier on the eyes and slighly more appealing to an audience especially given the ocean vibes theme of the OctoPi app)_
- [ ] _(The sidebar needs a better layout, when collapsed it is to show the icons of the different modes or just show arrow so it can be reopened, and the overall layoout of it requires improvement)_
- [ ] _(The sizes of the element boxes like the chat boxes, flashcard boxes and quiz question boxes needs to be refined and a smooth transitioning between pages needs to be implemented)_
- [ ] _(Each page title needs better positioning and sizes of the buttons needs to be adjusted as well as the color of certain buttons)_
- [ ] _(Octopus image of mascot needs to be reworked, right now on the landing page and the sidebar it looks out of place - either replaced with a 2d version or removed and replaced with a formatted logo or some other idea)_