# Setup Guide: AI Question Generation with OpenRouter

## ⚠️ IMPORTANT: Protect Your API Key!

Your OpenRouter API key was shared publicly. **You must:**
1. Go to https://openrouter.ai/keys
2. Delete the exposed key
3. Generate a new key
4. Follow the secure setup below

---

## Setup Instructions

### 1. Create a `.env` file
In the root directory of your project (c:\Users\Admin\Desktop\kalki\), create a file named `.env`:

```bash
# Windows PowerShell
New-Item -Path "c:\Users\Admin\Desktop\kalki\.env" -ItemType File
```

### 2. Add Your API Key to `.env`

Open the `.env` file and add (replace with your NEW API key):
```
OPENROUTER_API_KEY=sk-or-v1-your-new-key-here
OPENROUTER_MODEL=openai/gpt-4o-mini
```

### 3. Install Python-dotenv

```bash
pip install python-dotenv
```

### 4. Update your `config.py`

The config.py already reads from environment variables, so it should work once you have the `.env` file.

---

## How to Use AI Question Generation

### For Teachers:

1. **Login as Teacher**
2. **Go to a Quiz** → Click "Edit Quiz"
3. **Click "🤖 Generate with AI" button**
4. **Step 1:** Enter a topic (e.g., "Photosynthesis", "World War 2", "Algebra")
5. **Step 2:** Specify:
   - Number of questions (1-20)
   - Marks per question (1-10)
6. **Step 3:** Review generated questions
   - **Check/Uncheck** questions to select which ones to add
   - Questions show the correct answer marked in green
7. **Click "✅ Add Selected to Quiz"**
8. **Publish the quiz** and students can take it

---

## Features

✅ **Multi-step workflow** - Topic → Quantity → Review & Select
✅ **AI-powered** - Uses OpenRouter API (Claude/GPT-4)
✅ **Preview before adding** - Review questions before adding to quiz
✅ **Selective import** - Choose which questions to add
✅ **Error handling** - Validates API responses
✅ **Secure** - API key stored in `.env`, not in code

---

## Troubleshooting

### Issue: "OPENROUTER_API_KEY is not configured"
**Solution:** 
- Create `.env` file in project root
- Add `OPENROUTER_API_KEY=your-key-here`
- Restart Flask app

### Issue: "API Request failed"
**Solution:**
- Verify your API key is valid
- Check you have OpenRouter credits
- Check internet connection
- Try generating fewer questions (5-10)

### Issue: "Failed to parse AI response"
**Solution:**
- This means the API returned invalid format
- Try a simpler topic (e.g., "Biology" instead of very complex topics)
- Try generating fewer questions

### Issue: Generation takes very long
**Solution:**
- Generating questions can take 10-30 seconds
- Large numbers of questions take longer
- Try with 3-5 questions first

---

## Cost

OpenRouter charges per token used. Typical costs:
- 5 MCQ questions: ~$0.01-0.02
- 10 MCQ questions: ~$0.02-0.05
- 20 MCQ questions: ~$0.05-0.10

Monitor your usage at https://openrouter.ai/usage

---

## Next Steps

Once configured:
1. Test with a sample quiz
2. Generate a few test questions
3. Review and add them
4. Publish and let students take the quiz

Questions are imported as **Multiple Choice (MCQ)** with 4 options each.
Teachers can still manually add or edit questions as needed.
