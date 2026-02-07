# Verb-End Torture Chamber

A web-based German grammar trainer focused on mastering verb placement in subordinate clauses (Nebensatze). Built as a full-stack Flask application with a mobile-first, dark-themed UI.

## Idea & Concept

**Idea by Tatiana Sorokina**

Learning German verb placement in subordinate clauses is one of the most challenging aspects of German grammar. Native English speakers struggle with the rule that conjugated verbs move to the end of subordinate clauses, and that multiple verbs stack in a specific order. This app drills that skill through interactive exercises ranging from A2 to C1 level.

## How It Works

### Full-Sentence Reconstruction

The user is presented with a scrambled German sentence and must reconstruct it by placing all words in the correct order. This tests not just verb placement knowledge, but full comprehension of German sentence structure.

**Interaction modes:**

- **Tap**: Tap any word chip to place it in the next available slot
- **Drag & Drop**: Drag a word chip to a specific slot position (works on both desktop and mobile)
- **Long-press for Dictionary**: Press and hold any word to see its definition from the Duden dictionary (in German), with an option to save it to your vocabulary list

### Difficulty Levels

| Level | CEFR | Focus |
|-------|------|-------|
| Grundlagen | A2 | Simple subordinate clauses: dass, weil, wenn, obwohl, als, ob, bevor, damit, wahrend |
| Aufbau | B1 | Perfekt in Nebensatz, modal verbs, separable verbs, relative clauses |
| Vertiefung | B2 | Nested clauses, passive constructions, Konjunktiv, complex structures |
| Meisterklasse | C1 | Triple nesting, double infinitive (Ersatzinfinitiv), deeply embedded relative clauses |

### Error Analysis

When the user makes a mistake, the app provides detailed feedback:

- Identifies the specific type of verb placement error (wrong order, auxiliary before participle, modal before infinitive, etc.)
- Explains the grammar rule that applies
- Provides practical tips for remembering the correct pattern
- Shows the correct sentence for comparison

### Spaced Repetition

Failed exercises are automatically scheduled for retry after 2 days, implementing a basic spaced repetition system to reinforce learning.

## Duden Dictionary Integration

During exercises, users can long-press (hold) any word to see its definition from the Duden dictionary. The popup shows:

- Word type (Wortart)
- Definition(s) in German
- Example sentences
- A link to the full Duden.de entry
- A button to save the word to your personal vocabulary list

## Vocabulary Export

Words saved during exercises appear in the Dashboard under "Saved Words". Once enough words are collected, users can export them for further study:

- **Anki Export**: Downloads a TSV (tab-separated values) file that can be directly imported into Anki. Each card has the German word on the front and the Duden definition with examples on the back.
- **Quizlet Export**: Downloads a text file formatted for Quizlet's import feature. Create a new set in Quizlet, click "Import", and paste the file contents.

## Dashboard

The dashboard provides:

- Total attempts and accuracy statistics
- Current streak tracking
- Saved vocabulary words with export options
- Most frequent error categories with visual bar charts
- Accuracy trend over the last 30 days
- Recent attempt history

## Tech Stack

- **Backend**: Python / Flask
- **Database**: SQLite with WAL mode
- **Frontend**: Vanilla JavaScript (no framework), CSS custom properties
- **Deployment**: Gunicorn on Render.com
- **Dictionary**: Duden.de integration for word definitions

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

The app runs on `http://localhost:5000` by default.

## Project Structure

```
german_learning_app/
├── app.py              # Flask routes and API endpoints
├── sentences.py        # 156 sentence templates (A2-C1) and exercise preparation
├── database.py         # SQLite database layer
├── error_analyzer.py   # Error classification and grammar explanations
├── notification.py     # Daily notification system
├── mcp_server.py       # Claude MCP integration
├── requirements.txt    # Python dependencies
├── render.yaml         # Render.com deployment config
├── static/
│   ├── css/style.css   # Mobile-first dark theme
│   └── js/app.js       # Full-sentence drag & drop exercise engine
└── templates/
    ├── base.html       # Base template with navigation
    ├── index.html      # Home page with difficulty levels
    ├── exercise.html   # Exercise page
    ├── dashboard.html  # Statistics, saved words, and export
    └── no_exercises.html
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/check` | POST | Check user's sentence reconstruction |
| `/api/exercise` | GET | Get a random exercise |
| `/api/duden/<word>` | GET | Look up a word in Duden dictionary |
| `/api/words` | GET/POST | Get or save vocabulary words |
| `/api/words/<id>` | DELETE | Remove a saved word |
| `/api/words/export/anki` | GET | Download Anki-compatible TSV |
| `/api/words/export/quizlet` | GET | Download Quizlet-compatible text |
| `/api/stats` | GET | Get user statistics |
| `/api/daily` | GET | Daily sentence for notifications |

## Credits

- **Concept & Idea**: Tatiana Sorokina
- **Grammar Content**: 156 carefully crafted German sentences covering subordinate clause verb placement from A2 to C1 level
