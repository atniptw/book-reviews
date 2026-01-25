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
   - Parse your review
   - Create a structured markdown file in the `reviews/` directory
   - Comment on the issue with a link to the created file
   - Close the issue

## Review Storage

All book reviews are stored as markdown files in the `reviews/` directory. Each review includes:
- Book title and author
- Rating
- Review date
- Your review text
- Likes and dislikes
- Additional notes
- Link back to the original issue

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
│       └── create-review.yml        # GitHub Action to process reviews
├── reviews/                         # All book reviews stored here
│   └── .gitkeep
├── LICENSE
└── README.md
```