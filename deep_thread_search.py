#!/usr/bin/env python3
"""Deep search for intellectronica's message in all threads"""

import discord
import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1369370266899185746

async def deep_thread_search():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.guild_messages = True
    client = discord.Client(intents=intents)
    
    all_messages_found = []
    thread_messages_found = []
    
    @client.event
    async def on_ready():
        print(f'Connected as {client.user}')
        
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            print("Channel not found!")
            await client.close()
            return
            
        print(f"Channel: #{channel.name}")
        
        # First, let's find ALL messages that mention "slack support" or "data you are indexing"
        print("\n🔍 Stage 1: Searching ALL channel messages for relevant content...")
        
        message_count = 0
        async for message in channel.history(limit=None):
            message_count += 1
            content_lower = message.content.lower()
            
            # Look for various patterns
            if any(phrase in content_lower for phrase in [
                'slack support channel',
                'data you are indexing',
                'generate queries',
                'ground truth answers',
                'converting the support channel'
            ]):
                all_messages_found.append({
                    'id': str(message.id),
                    'author': str(message.author),
                    'content': message.content[:300],
                    'created_at': message.created_at.isoformat(),
                    'has_thread': hasattr(message, 'thread') and message.thread is not None,
                    'is_reply': message.reference is not None
                })
                print(f"\n📌 Found relevant message by {message.author}:")
                print(f"   {message.content[:150]}...")
        
        print(f"\n✓ Scanned {message_count} channel messages")
        print(f"✓ Found {len(all_messages_found)} relevant messages")
        
        # Now search ALL threads exhaustively
        print("\n🔍 Stage 2: Deep searching ALL threads...")
        
        thread_count = 0
        total_thread_messages = 0
        
        # Get active threads
        print("\n  Checking active threads...")
        for thread in channel.threads:
            thread_count += 1
            print(f"\n  Thread: {thread.name}")
            try:
                async for tmsg in thread.history(limit=None):
                    total_thread_messages += 1
                    content_lower = tmsg.content.lower()
                    
                    if any(phrase in content_lower for phrase in [
                        'data you are indexing',
                        'generate queries',
                        'ground truth answers',
                        'slack support'
                    ]):
                        thread_messages_found.append({
                            'thread_name': thread.name,
                            'thread_id': str(thread.id),
                            'parent_id': str(thread.parent_id),
                            'message_id': str(tmsg.id),
                            'author': str(tmsg.author),
                            'content': tmsg.content[:500],
                            'created_at': tmsg.created_at.isoformat()
                        })
                        print(f"    ✅ Found message by {tmsg.author}")
                        print(f"       {tmsg.content[:150]}...")
            except Exception as e:
                print(f"    ❌ Error reading thread: {e}")
        
        # Get archived threads
        print("\n  Checking archived threads...")
        async for thread in channel.archived_threads(limit=None):
            thread_count += 1
            print(f"\n  Archived thread: {thread.name}")
            try:
                async for tmsg in thread.history(limit=None):
                    total_thread_messages += 1
                    content_lower = tmsg.content.lower()
                    
                    if any(phrase in content_lower for phrase in [
                        'data you are indexing',
                        'generate queries',
                        'ground truth answers',
                        'slack support'
                    ]):
                        thread_messages_found.append({
                            'thread_name': thread.name,
                            'thread_id': str(thread.id),
                            'parent_id': str(thread.parent_id),
                            'archived': True,
                            'message_id': str(tmsg.id),
                            'author': str(tmsg.author),
                            'content': tmsg.content[:500],
                            'created_at': tmsg.created_at.isoformat()
                        })
                        print(f"    ✅ Found message by {tmsg.author}")
                        print(f"       {tmsg.content[:150]}...")
            except Exception as e:
                print(f"    ❌ Error reading archived thread: {e}")
        
        print(f"\n✓ Checked {thread_count} threads")
        print(f"✓ Scanned {total_thread_messages} thread messages")
        print(f"✓ Found {len(thread_messages_found)} relevant thread messages")
        
        # Save all findings
        findings = {
            'channel_messages': all_messages_found,
            'thread_messages': thread_messages_found,
            'summary': {
                'total_channel_messages': message_count,
                'total_threads': thread_count,
                'total_thread_messages': total_thread_messages,
                'relevant_channel_messages': len(all_messages_found),
                'relevant_thread_messages': len(thread_messages_found)
            }
        }
        
        with open('deep_search_results.json', 'w', encoding='utf-8') as f:
            json.dump(findings, f, indent=2, ensure_ascii=False)
        
        print("\n💾 Saved detailed findings to deep_search_results.json")
        
        # Specific search for intellectronica
        print("\n🔍 Stage 3: Specific search for intellectronica...")
        intel_messages = [
            msg for msg in all_messages_found 
            if 'intellectronica' in msg['author']
        ]
        intel_thread_messages = [
            msg for msg in thread_messages_found
            if 'intellectronica' in msg['author']
        ]
        
        print(f"\nFound {len(intel_messages)} channel messages by intellectronica")
        print(f"Found {len(intel_thread_messages)} thread messages by intellectronica")
        
        if intel_thread_messages:
            print("\n✅ intellectronica's thread messages:")
            for msg in intel_thread_messages:
                print(f"\n  Thread: {msg['thread_name']}")
                print(f"  Content: {msg['content'][:200]}...")
        
        await client.close()
    
    await client.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(deep_thread_search())