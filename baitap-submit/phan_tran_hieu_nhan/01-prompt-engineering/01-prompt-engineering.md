- Prompt 1
```
As a teacher, you know how to create the multiple choice exercise from the lesson.
Help me write [question_quantity] multiple choice questions for exercise from the below lesson content.
The questions should be with [levels] levels and the exercise purpose is [purpose].
The questions should have [choice_quantity] choices and have format like this
"""
Question #[Number]: [Question]
Choices:
[ ] 1. [Option 1]
[ ] 2. [Option 2]
[x] 3. [Option 3] (Correct Answer)
[ ] 4. [Option 4]
"""
Lesson content:
[lesson content]
```

- Prompt 2
```
As a writer, you help me analyze the below paragraph and write more with [word_numbers] word numbers.
Paragraph:
[paragraph]
```

- Prompt 3
```
As a social media manager, you help me classify which comment are positive or negative and summarize and count and present like below format.

- Positive ([count]):
    + "[comment_1]"
    + "[comment_2]"
- Negative ([count]):
    + "[comment_3]"
    + "[comment_4]"
- Summary: [summary]
```

- Prompt 4
```
As a software engineer, you help me find the bug and comment to explain the below code.
[code]
```
- Prompt 5
```
As a tour guy, you help me suggest the attractions, activities, famous foods, visiting times in [location] and on [time to visit] and present like below csv format.
attractions,activities,famous foods,visiting times
```

- Prompt 6
```
As a reader, you help me summarize ([number_word] words) the below book as a file, and list the character in it and present the response follow this format.
Response:
- Summary: [summary]
- Characters:
    + Character 1
    + Character 2
```
