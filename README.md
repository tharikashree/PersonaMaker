# Reddit Persona Bot

A Python-based tool that analyzes Reddit users' posts and comments to generate comprehensive user personas using AI. The bot scrapes user content, processes it with Google's Gemini AI, and creates beautiful PDF reports with avatars.

## 🌟 Features

- **Reddit Content Scraping**: Extracts posts and comments from Reddit user profiles
- **AI-Powered Analysis**: Uses Google Gemini AI to analyze user behavior and generate detailed personas
- **Avatar Generation**: Creates custom avatars based on persona descriptions using AI image generation
- **PDF Report Generation**: Creates professional-looking PDF reports with personality visualizations
- **Personality Metrics**: Visual representation of personality traits and tech savviness
- **Structured Data**: Organizes persona data into categories like demographics, interests, values, and motivations

## 📁 Project Structure

```
persona_bot/
├── main.py                    # Main entry point for the application
├── scrape_reddit.py          # Reddit content scraping functionality
├── generate_persona.py       # AI persona generation and image creation
├── generate_pdf.py           # PDF report generation
├── requirements.txt          # Python dependencies
├── templates/
│   └── persona_template.html # HTML template for PDF generation
├── persona_outputs/          # Generated personas and avatars
│   ├── [username]_persona.txt
│   ├── [username]_persona.pdf
│   └── [username]_avatar.png
└── .env                      # Environment variables (create this file)
```

## � Installation

### Prerequisites

1. **Python 3.8+** - Make sure Python is installed on your system
2. **wkhtmltopdf** - Required for PDF generation
   - Windows: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
   - Install to `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`
3. **Reddit API Access** - Create a Reddit app at [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
4. **Google Gemini API Key** - Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
5. **Image Generation API** - Get Claid.ai API key for avatar generation

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd persona_bot
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**
   Create a `.env` file in the project root with the following variables:
   ```env
   # Reddit API Credentials
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=PersonaBot/1.0 by YourUsername

   # Google Gemini AI API Key
   GEMINI_API_KEY=your_gemini_api_key

   # Image Generation API (Claid.ai)
   IMAGE_API_KEY=your_claid_api_key
   ```

4. **Verify wkhtmltopdf installation**
   - Ensure wkhtmltopdf is installed at `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`
   - Or update the path in `generate_pdf.py` if installed elsewhere

## 🎯 Usage

### Basic Usage

Run the main script to analyze predefined Reddit users:

```bash
python main.py
```

### Analyze Specific Users

Edit the `reddit_urls` list in `main.py` to target specific Reddit users:

```python
reddit_urls = [
    "https://www.reddit.com/user/your_target_user/",
    "https://www.reddit.com/user/another_user/",
]
```

### Generate PDF Reports

After generating a persona, create a PDF report:

```bash
python generate_pdf.py
```

### Individual Components

- **Scrape Reddit data only**:
  ```python
  from scrape_reddit import get_user_content
  posts, comments = get_user_content("username")
  ```

- **Generate persona from existing data**:
  ```python
  from generate_persona import generate_user_persona
  persona = generate_user_persona(posts, comments, "username")
  ```

## 📊 Output Examples

### Generated Files

For each analyzed user, the bot creates:

1. **Text Persona** (`username_persona.txt`): Detailed analysis including:
   - Demographics (hypothetical)
   - Interests and hobbies
   - Personality traits
   - Values and motivations
   - Tech savviness level
   - Communication tone
   - Opinions and perspectives

2. **PDF Report** (`username_persona.pdf`): Professional visual report with:
   - User avatar
   - Personality trait bars
   - Tech savviness circular chart
   - Organized sections for easy reading

3. **Avatar Image** (`username_avatar.png`): AI-generated profile picture

### Sample Persona Structure

```
## User Persona: Alex

**1. Demographics (Hypothetical):**
* Age: 30-35
* Gender: Male
* Location: New York City
* Occupation: Software Engineer

**2. Interests:**
* Technology and Apple products
* Video games
* Japanese culture
* Environmental sustainability

**3. Personality:**
Curious, analytical, tech-savvy, introspective, socially aware

**4. Tech Savviness:**
High - Comfortable with advanced technology and development tools
```

## ⚙️ Configuration

### Customizing Analysis

Edit prompts in `generate_persona.py` to change analysis focus:

- Modify the persona generation prompt for different analysis styles
- Adjust post/comment limits in `scrape_reddit.py`
- Update personality traits in `generate_pdf.py`

### PDF Styling

Customize the visual appearance in `templates/persona_template.html`:

- Modify CSS styles for colors, fonts, and layout
- Add new sections or remove existing ones
- Change personality trait categories

## 🔧 Troubleshooting

### Common Issues

1. **wkhtmltopdf not found**
   - Ensure wkhtmltopdf is properly installed
   - Update the path in `generate_pdf.py` line 59

2. **Reddit API errors**
   - Verify your Reddit API credentials in `.env`
   - Check if the target user's profile is public
   - Ensure you're not hitting rate limits

3. **Gemini API errors**
   - Verify your Gemini API key is valid
   - Check your API quota and billing status

4. **Missing dependencies**
   - Run `pip install -r requirements.txt` again
   - Use a virtual environment to avoid conflicts

### Debug Mode

Enable detailed logging by modifying the logging level in `scrape_reddit.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📋 Dependencies

- `requests` - HTTP requests
- `google-generativeai` - Google Gemini AI integration
- `python-dotenv` - Environment variable management
- `Pillow` - Image processing
- `jinja2` - Template rendering
- `pdfkit` - PDF generation
- `praw` - Reddit API wrapper

## 🔐 Privacy & Ethics

### Important Considerations

- **Public Data Only**: This tool only accesses publicly available Reddit content
- **Hypothetical Analysis**: Generated personas are AI interpretations, not factual profiles

## 📝 License

This project is for educational and research purposes. Please use responsibly and in accordance with Reddit's terms of service and API usage guidelines.

---

**Note**: This tool analyzes public Reddit content and generates hypothetical personas for educational purposes. Always use responsibly and respect user privacy.