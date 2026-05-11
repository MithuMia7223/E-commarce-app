# Web Developer Freelancer Bot

A Telegram bot for web development freelancers to manage clients, showcase portfolio, and automate client communication.

## Features

### 🎯 Core Features
- **Portfolio Showcase**: Display your web development projects
- **Service Management**: List your web development services with pricing
- **Client Management**: Track client information and projects
- **Quote Requests**: Automated quote request system
- **Project Tracking**: Monitor project status and deadlines
- **Contact Information**: Easy access to your contact details

### 🤖 Bot Commands
- `/start` - Welcome message and main menu
- `/services` - View available web development services
- `/portfolio` - showcase your portfolio projects
- `/quote` - Request a custom quote
- `/contact` - Get contact information
- `/projects` - View your projects (for registered clients)
- `/help` - Show help message

### 💼 Services Included
- Static Website Development
- Dynamic Website Development
- E-commerce Platform
- Web Application Development
- Website Maintenance

## Installation

1. **Clone or download the bot files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Telegram Bot Token**:
   - Talk to @BotFather on Telegram
   - Create a new bot
   - Copy the bot token

4. **Configure the bot**:
   - Open `freelancer_bot.py`
   - Replace `YOUR_BOT_TOKEN_HERE` with your actual bot token
   - Update your contact information in the `contact_command` method

5. **Run the bot**:
   ```bash
   python freelancer_bot.py
   ```

## Database

The bot uses SQLite database with the following tables:
- `clients`: Store client information
- `projects`: Track project details
- `portfolio`: Your portfolio items
- `services`: Your service offerings

## Customization

### Update Your Information
Edit these sections in `freelancer_bot.py`:

1. **Contact Information** (in `contact_command` method):
   ```python
   📧 Email: your-email@example.com
   📱 Phone: +8801234567890
   💬 Telegram: @your-username
   🌐 Website: https://your-website.com
   ```

2. **Portfolio Items** (in `add_sample_data` method):
   ```python
   portfolio_items = [
       ("Your Project Title", "Project description", "Tech stack", "Image URL", "Live URL", "GitHub URL")
   ]
   ```

3. **Services** (in `add_sample_data` method):
   ```python
   services = [
       ("Service Title", "Service description", price, "Delivery time")
   ]
   ```

## Usage Examples

### Client Interaction
1. Client starts the bot with `/start`
2. Bot shows welcome message with menu options
3. Client can view services, portfolio, or request quotes
4. Bot saves client information for future reference

### Quote Request Process
1. Client uses `/quote` command
2. Bot requests project details
3. Client provides project information
4. Bot saves the request and sends acknowledgment

## Deployment

### Local Development
```bash
python freelancer_bot.py
```

### Production Deployment
Consider using:
- **Heroku**: Easy deployment with free tier
- **PythonAnywhere**: Simple Python hosting
- **VPS**: Full control over your environment
- **Docker**: Containerized deployment

## Security Notes

- Keep your bot token secure
- Use environment variables for sensitive data
- Regular backup of your SQLite database
- Implement rate limiting for production use

## Support

For issues and questions:
- Check the bot logs for errors
- Verify your bot token is correct
- Ensure all dependencies are installed
- Test with a small group first

## Future Enhancements

- Payment integration
- File sharing capabilities
- Advanced analytics
- Multi-language support
- Web dashboard for management
# E-commarce-app
