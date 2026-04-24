# OctoPi Test Set — DSA Study Notes
**Version:** Day 3  
**Notes used:** Data Structures & Algorithms (DSA) short text  
**Purpose:** Manual evaluation of flashcard relevance, quiz accuracy, and chat quality

---

## Study Notes Used (paste this into OctoPi to test)

```
Data Structures and Algorithms (DSA)

A data structure is a way of organising data so it can be accessed and modified efficiently.

Arrays store elements in contiguous memory. Access is O(1), insertion/deletion is O(n).

A Linked List is a sequence of nodes where each node stores data and a pointer to the next node. Insertion at head is O(1), search is O(n).

A Stack follows LIFO (Last In First Out). Main operations: push, pop, peek. Used in function call stacks and undo operations.

A Queue follows FIFO (First In First Out). Main operations: enqueue, dequeue. Used in scheduling and BFS.

A Binary Search Tree (BST) stores data such that the left child is smaller and the right child is larger than the parent. Average search: O(log n), worst case O(n).

A Hash Table maps keys to values using a hash function. Average access: O(1), worst case O(n) due to collisions.

Sorting algorithms:
- Bubble Sort: O(n²) time, O(1) space — simple but slow
- Merge Sort: O(n log n) time, O(n) space — divide and conquer
- Quick Sort: O(n log n) average, O(n²) worst case

Graph traversal:
- BFS (Breadth First Search): uses a queue, explores level by level
- DFS (Depth First Search): uses a stack (or recursion), explores as deep as possible

Big O Notation describes the worst-case time/space complexity of an algorithm.
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(2ⁿ)
```

---

## Test Questions (20 total)

### Section A — Factual / Flashcard Quality

| # | Question | Expected Answer |
|---|----------|----------------|
| 1 | What does LIFO stand for? | Last In First Out |
| 2 | What does FIFO stand for? | First In First Out |
| 3 | What is the time complexity of accessing an element in an array? | O(1) |
| 4 | What data structure uses LIFO ordering? | Stack |
| 5 | What data structure uses FIFO ordering? | Queue |
| 6 | What is the average time complexity of searching in a Hash Table? | O(1) |
| 7 | What is the worst-case time complexity of Bubble Sort? | O(n²) |
| 8 | What is the time complexity of Merge Sort? | O(n log n) |
| 9 | In a BST, where is the smaller child stored? | Left child |
| 10 | What traversal algorithm uses a queue? | BFS (Breadth First Search) |

---

### Section B — Multiple Choice (for quiz testing)

**Q11.** Which data structure would you use for an undo feature in a text editor?  
- A. Queue  
- B. Stack ✅  
- C. Array  
- D. Hash Table  

**Q12.** What is the worst-case time complexity for searching in a BST?  
- A. O(1)  
- B. O(log n)  
- C. O(n) ✅  
- D. O(n²)  

**Q13.** Which sorting algorithm uses divide and conquer?  
- A. Bubble Sort  
- B. Quick Sort  
- C. Merge Sort ✅  
- D. Insertion Sort  

**Q14.** What does Big O notation describe?  
- A. Best-case performance  
- B. Average-case performance  
- C. Worst-case time/space complexity ✅  
- D. Memory usage only  

**Q15.** DFS graph traversal uses which data structure internally?  
- A. Queue  
- B. Stack ✅  
- C. Array  
- D. Hash Table  

---

### Section C — True / False

| # | Statement | Answer |
|---|-----------|--------|
| 16 | Arrays allow O(1) insertion at any position | False |
| 17 | A Linked List allows O(1) insertion at the head | True |
| 18 | Hash Tables always have O(1) access regardless of collisions | False |
| 19 | O(n log n) is faster than O(n²) for large inputs | True |
| 20 | BFS explores a graph depth-first using recursion | False |

---

## How to Use This File

1. Paste the **Study Notes** block into OctoPi's Chat tab
2. Run **Flashcards** → check that generated cards cover topics from Section A
3. Run **Quiz** (MC + T/F) → compare OctoPi's generated questions against Sections B & C
4. Ask **Chat**: *"What is the difference between BFS and DFS?"* → verify answer quality
5. Record results in `baseline.md`

## Results: 
Manually evaluated using 10 test questions across different topics. All 10 questions received relevant, accurate responses grounded in the uploaded notes. Octo successfully maintained personality and language consistency throughout. Quiz generation succeeded on all test runs. Flashcard quality rated as accurate and useful on all 10 test cases. Pass rate: 10/10.