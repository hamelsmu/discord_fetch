#!/usr/bin/env python3
"""Deep investigation of thread fetching"""

import discord
import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1369370266899185746

async def debug_thread_fetching():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.guild_messages = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'Connected as {client.user}')
        
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            print("Channel not found!")
            await client.close()
            return
            
        print(f"Channel: #{channel.name}")
        
        # Find the noviceai message
        novice_msg = None
        print("\n🔍 Searching for noviceai's message...")
        
        async for message in channel.history(limit=None):
            if ('noviceai' in str(message.author) and 
                'slack support channel' in message.content and
                'converting the support channel into a ai chatbot' in message.content.lower()):
                novice_msg = message
                print(f"\n✅ Found noviceai's message!")
                print(f"  ID: {message.id}")
                print(f"  Content: {message.content[:100]}...")
                print(f"  Created at: {message.created_at}")
                print(f"  Has thread: {hasattr(message, 'thread') and message.thread is not None}")
                
                # Check for thread
                if hasattr(message, 'thread') and message.thread:
                    thread = message.thread
                    print(f"\n📌 Thread found!")
                    print(f"  Thread name: {thread.name}")
                    print(f"  Thread ID: {thread.id}")
                    print(f"  Archived: {thread.archived}")
                    print(f"  Archive timestamp: {thread.archive_timestamp}")
                    
                    # Fetch thread messages
                    print("\n  Fetching thread messages...")
                    thread_messages = []
                    async for tmsg in thread.history(limit=None):
                        thread_messages.append({
                            "author": str(tmsg.author),
                            "content": tmsg.content[:200],
                            "timestamp": tmsg.created_at.isoformat()
                        })
                    
                    print(f"  Found {len(thread_messages)} messages in thread")
                    
                    # Look for intellectronica
                    for tmsg in thread_messages:
                        if 'intellectronica' in tmsg['author']:
                            print(f"\n  ✅ Found intellectronica in thread!")
                            print(f"    Content: {tmsg['content']}...")
                else:
                    print("\n❌ No thread attached to this message")
                    
                    # Try to find threads that started from this message
                    print("\n🔍 Searching all threads in channel...")
                    thread_count = 0
                    
                    # Get all threads
                    for thread in channel.threads:
                        thread_count += 1
                        if thread.parent_id == message.id:
                            print(f"\n✅ Found thread with parent_id matching!")
                            print(f"  Thread: {thread.name}")
                            break
                    
                    # Also check archived threads
                    print("\n🔍 Checking archived threads...")
                    async for thread in channel.archived_threads(limit=100):
                        thread_count += 1
                        print(f"  Checking thread: {thread.name} (parent_id: {thread.parent_id})")
                        if thread.parent_id == message.id:
                            print(f"\n✅ Found archived thread!")
                            print(f"  Thread: {thread.name}")
                            print(f"  Thread ID: {thread.id}")
                            
                            # Fetch messages
                            async for tmsg in thread.history(limit=None):
                                if 'intellectronica' in str(tmsg.author):
                                    print(f"\n  ✅ Found intellectronica's reply!")
                                    print(f"    Content: {tmsg.content[:200]}...")
                            break
                    
                    print(f"\n  Total threads checked: {thread_count}")
                
                # Let's also search ALL messages for intellectronica's reply
                print("\n🔍 Searching all messages for intellectronica's reply about 'data you are indexing'...")
                found_intel = False
                async for msg in channel.history(limit=None):
                    if ('intellectronica' in str(msg.author) and 
                        'data you are indexing is real' in msg.content):
                        found_intel = True
                        print(f"\n✅ Found intellectronica's message!")
                        print(f"  ID: {msg.id}")
                        print(f"  Content: {msg.content[:300]}...")
                        print(f"  Created at: {msg.created_at}")
                        print(f"  Is reply: {msg.reference is not None}")
                        if msg.reference:
                            print(f"  Reply to message ID: {msg.reference.message_id}")
                            print(f"  Reply to channel ID: {msg.reference.channel_id}")
                        break
                
                if not found_intel:
                    print("  ❌ intellectronica's reply not found in channel messages")
                
                break
        
        if not novice_msg:
            print("❌ Could not find noviceai's message")
        
        await client.close()
    
    await client.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(debug_thread_fetching())