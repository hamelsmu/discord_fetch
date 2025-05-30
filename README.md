# Discord Fetch


<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This library provides a simple way to export Discord channel
conversations in both detailed and simplified formats, making it easy to
analyze or process Discord community discussions.

## Installation & Setup

Install from PyPI:

``` bash
pip install discord_fetch
```

Or install in development mode:

``` bash
git clone https://github.com/yourusername/discord_fetch.git
cd discord_fetch
pip install -e .
```

> [!NOTE]
>
> ### Discord Bot Setup
>
> Before using this tool, you need to create a Discord bot and obtain a
> token:
>
> ### 1. Create a Discord Application
>
> 1.  Go to the [Discord Developer
>     Portal](https://discord.com/developers/applications)
> 2.  Click “New Application” and give it a name
> 3.  Navigate to the “Bot” section in the sidebar
> 4.  Click “Add Bot”
> 5.  Under the “Token” section, click “Copy” to get your bot token
>
> ### 2. Required Bot Permissions
>
> Your bot needs the following permissions: - **View Channels** - To see
> the channels in the server - **Read Message History** - To fetch
> historical messages - **Read Messages/View Channels** - Basic read
> access
>
> ### 3. Bot Scopes and OAuth2
>
> When inviting your bot to a server, use these scopes: - `bot` - Basic
> bot permissions - `applications.commands` (optional) - If you plan to
> add slash commands
>
> ### 4. Invite the Bot to Your Server
>
> 1.  In the Discord Developer Portal, go to “OAuth2” \> “URL Generator”
> 2.  Select the `bot` scope
> 3.  Select the required permissions listed above
> 4.  Copy the generated URL and open it in your browser
> 5.  Select the server you want to add the bot to
>
> ### 5. Environment Setup
>
> Create this environment variable
>
> ``` env
> DISCORD_TOKEN=your_bot_token_here
> ```

### Getting Channel IDs

To fetch messages from a channel, you need its Channel ID:

1.  Enable Developer Mode in Discord:
    - Go to User Settings \> Advanced \> Developer Mode (toggle on)
2.  Right-click on any channel
3.  Select “Copy Channel ID”

The Channel ID will be a long number like `1369370266899185746`.

## CLI Usage

Once installed and configured, you can use the
[`fetch_discord_msgs`](https://hamelsmu.github.io/discord_fetch/core.html#fetch_discord_msgs)
command:

``` python
!fetch_discord_msgs --help
```

                                                                                    
     Usage: fetch_discord_msgs [OPTIONS] CHANNEL_ID                                 
                                                                                    
     Fetch all messages from a Discord channel including threads and reply          
     hierarchies.                                                                   
     By default, outputs simplified conversation data as JSON to stdout (suitable   
     for piping). Use --save-to-files to save both original and simplified data to  
     files with summary output.s                                                    
                                                                                    
    ╭─ Arguments ──────────────────────────────────────────────────────────────────╮
    │ *    channel_id      INTEGER  Discord channel ID to fetch messages from      │
    │                               [default: None]                                │
    │                               [required]                                     │
    ╰──────────────────────────────────────────────────────────────────────────────╯
    ╭─ Options ────────────────────────────────────────────────────────────────────╮
    │ --limit                INTEGER  Maximum number of messages to fetch          │
    │                                 [default: None]                              │
    │ --verbose                       Show detailed logs                           │
    │ --save-to-files                 Save both original and simplified data to    │
    │                                 files and print summary                      │
    │ --help                          Show this message and exit.                  │
    ╰──────────────────────────────────────────────────────────────────────────────╯

### Basic Usage Examples

``` bash
# Output simplified JSON to stdout (default behavior)
fetch_discord_msgs 1369370266899185746

# Save both original and simplified data to files with summary
fetch_discord_msgs 1369370266899185746 --save-to-files

# Show verbose output while saving to files
fetch_discord_msgs 1369370266899185746 --save-to-files --verbose

# Limit to last 100 messages and output to stdout
fetch_discord_msgs 1369370266899185746 --limit 100


fetch_discord_msgs 1369370266899185746 | jq '.conversations[0]'

# Save to files and process specific conversations
fetch_discord_msgs 1369370266899185746 --save-to-files | jq '.conversations[] | select(.replies | length > 5)'
```

**Live example**

``` python
# Pipe simplified data to another tool (like jq)
!fetch_discord_msgs 1369370266899185746 | jq '.conversations[0]'
```

    Connected as hamml#3190
    {
      "main_message": {
        "author": "davidh5633",
        "content": "Seems relevant to this course topic:\n\nEvaluation Driven Development for Agentic Systems\nhttps://www.newsletter.swirlai.com/p/evaluation-driven-development-for?utm_source=tldrai"
      },
      "replies": []
    }

## CLI Output Modes

The CLI tool has two main output modes:

### 1. Stdout Mode (Default)

- Outputs simplified JSON directly to stdout
- Perfect for piping to other tools (jq, etc.)
- Minimal stderr output (only connection/error messages)
- Use this for automation and data processing

### 2. File Save Mode (`--save-to-files`)

- Saves both original and simplified data to timestamped JSON files
- Prints detailed summary to stderr
- Use `--verbose` for additional logging details
- Use this for archival and detailed analysis

## Output Files

When using `--save-to-files`, the tool generates two types of JSON
files:

##### 1. Original Format (`discord_channel_*_TIMESTAMP.json`)

- Complete message metadata (IDs, timestamps, reactions, etc.)
- Full thread and reply hierarchies
- All Discord-specific data preserved
- Larger file size

##### 2. Simplified Format (`discord_simplified_*_TIMESTAMP.json`)

- Conversation-focused structure
- Removes metadata and IDs
- Groups messages with their replies
- ~75% smaller file size
- Ideal for LLM processing

## Python API

You can also use the library programmatically:

``` python
from discord_fetch.core import fetch_discord_msgs
```

``` python
channel_id = 1369370266899185746
original, simplified = await fetch_discord_msgs(
    channel_id, 
    save_original=False,    # Don't save raw discord messages to file
    save_simplified=False,  # Don't save simplified discord messages to file
    print_summary=False     # Don't print verbose logs
)

print(f"Fetched {len(simplified['conversations'])} conversations")
```

    Connected as hamml#3190

    Fetched 152 conversations

## Troubleshooting

### Common Issues

**“Channel not found or no access”** - Verify the Channel ID is
correct - Ensure your bot is a member of the server - Check that the bot
has “View Channels” permission

**“DISCORD_TOKEN env variable not found”** - Set your environment
variable `DISCORD_TOKEN=your_token`

**“Could not fetch archived threads”** - This is usually not critical -
some archived threads may not be accessible - The main channel messages
will still be fetched

### Rate Limiting

Discord has rate limits for API requests. For large channels: - The tool
automatically handles rate limiting - Very large channels (\>10k
messages) may take several minutes - Consider using the `--limit`
parameter for testing
