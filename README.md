# book-reviews

A repository for storing book reviews in structured markdown files, submitted via GitHub issues.

## How to Submit a Book Review

1. **Create a new issue** using the "Book Review" template
2. **Fill out the form** with:
   - Book title
   - Author
   - Rating (1-5)
   - Your review
   - What you liked
   - What you disliked
   - Any additional notes

3. **Submit the issue** - The system will automatically:
   - Post instructions for @copilot to process the review
   - Copilot will then:
     - Parse your review
     - **Improve grammar and clarity** using AI
     - Create a structured markdown file in the `reviews/` directory
     - Create a pull request with the new file
     - Close the issue after the PR is created

## Review Storage

All book reviews are stored as markdown files in the `reviews/` directory. Each review includes:
- Book title and author
- Rating
- Review date
- Your review text
- Likes and dislikes
- Additional notes
- Link back to the original issue

## Copilot-Powered Processing

When you submit a book review issue, the workflow automatically posts instructions for GitHub Copilot to process your review. Copilot will:
- Improve grammar and sentence structure
- Enhance clarity while preserving your original meaning and tone
- Create a structured markdown file
- Submit the file as a pull request for your review

This approach allows you to review the changes before they're merged, giving you full control over what gets added to your book reviews collection.

Don't worry about writing perfectly - just focus on capturing your thoughts, and Copilot will polish the text for you!

## Using Reviews with AI

The markdown files in the `reviews/` directory are structured to be easily consumed by AI assistants like GitHub Copilot or ChatGPT. You can:
- Share the entire `reviews/` directory as context
- Reference specific reviews when discussing books
- Use them as a knowledge base for book recommendations

## Directory Structure

```
book-reviews/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── book-review.yml          # Issue template for submitting reviews
│   └── workflows/
│       └── create-review.yml        # GitHub Action to assign reviews to Copilot
├── reviews/                         # All book reviews stored here
│   └── .gitkeep
├── LICENSE
└── README.md
```