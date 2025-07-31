#!/usr/bin/env python3
"""Debug script to find the thread issue"""

import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from discord_fetch.core import fetch_channel_complete_history

CHANNEL_ID = 1369370266899185746

async def debug_threads():
    print("Fetching raw channel data...")
    
    # Get raw data
    raw_data = await fetch_channel_complete_history(
        CHANNEL_ID,
        limit=None,
        save_to_file=False,
        print_summary=False
    )
    
    if not raw_data:
        print("Failed to fetch data")
        return
    
    print(f"Total messages: {len(raw_data['messages'])}")
    print(f"Total threads: {len(raw_data['threads'])}")
    
    # Find noviceai's message
    novice_msg = None
    for msg in raw_data['messages']:
        if ('noviceai' in msg['author']['name'] and 
            'slack support channel' in msg['content'] and
            'converting the support channel into a ai chatbot' in msg['content'].lower()):
            novice_msg = msg
            print(f"\n✅ Found noviceai's message:")
            print(f"  ID: {msg['id']}")
            print(f"  Content: {msg['content'][:100]}...")
            break
    
    if not novice_msg:
        print("❌ Could not find noviceai's message")
        return
    
    # Check if this message has a thread
    thread_found = False
    for thread_id, thread_info in raw_data['threads'].items():
        if thread_info['parent_message_id'] == novice_msg['id']:
            thread_found = True
            print(f"\n✅ Found thread for this message!")
            print(f"  Thread ID: {thread_id}")
            print(f"  Thread name: {thread_info['name']}")
            print(f"  Messages in thread: {len(thread_info['messages'])}")
            
            # Show thread messages
            for i, tmsg in enumerate(thread_info['messages'][:5]):
                print(f"\n  Message {i+1}:")
                print(f"    Author: {tmsg['author']['name']}")
                print(f"    Content: {tmsg['content'][:150]}...")
            break
    
    if not thread_found:
        print("\n❌ No thread found for noviceai's message")
        
        # Let's check if there are any threads that mention the same content
        print("\n🔍 Searching all threads for related content...")
        for thread_id, thread_info in raw_data['threads'].items():
            for tmsg in thread_info['messages']:
                if 'intellectronica' in tmsg['author']['name'] and 'data you are indexing' in tmsg['content']:
                    print(f"\n✅ Found intellectronica's reply in thread {thread_id}!")
                    print(f"  Thread name: {thread_info['name']}")
                    print(f"  Parent message ID: {thread_info['parent_message_id']}")
                    
                    # Find parent message
                    for msg in raw_data['messages']:
                        if msg['id'] == thread_info['parent_message_id']:
                            print(f"  Parent message by: {msg['author']['name']}")
                            print(f"  Parent content: {msg['content'][:100]}...")
                            break
                    
                    return
    
    # Also check for direct replies
    print("\n🔍 Checking for direct replies to noviceai's message...")
    reply_count = 0
    for msg in raw_data['messages']:
        if msg.get('reply_to') and msg['reply_to'].get('message_id') == novice_msg['id']:
            reply_count += 1
            print(f"\nDirect reply {reply_count} by {msg['author']['name']}:")
            print(f"  {msg['content'][:100]}...")
    
    if reply_count == 0:
        print("  No direct replies found")
    
    # Search for intellectronica's message in all messages
    print("\n🔍 Searching for intellectronica's message in all messages...")
    found_intel = False
    for msg in raw_data['messages']:
        if 'intellectronica' in msg['author']['name'] and 'data you are indexing' in msg['content']:
            found_intel = True
            print(f"\n✅ Found intellectronica's message!")
            print(f"  ID: {msg['id']}")
            print(f"  Content: {msg['content'][:200]}...")
            print(f"  Timestamp: {msg['timestamp']}")
            
            # Check if it's a reply
            if msg.get('reply_to'):
                print(f"  Is a reply to message ID: {msg['reply_to']['message_id']}")
                # Find what it's replying to
                for orig in raw_data['messages']:
                    if orig['id'] == msg['reply_to']['message_id']:
                        print(f"  Replying to {orig['author']['name']}: {orig['content'][:100]}...")
                        break
            else:
                print("  Not a reply to any message")
            
            # Check timestamp proximity
            from datetime import datetime
            novice_time = datetime.fromisoformat(novice_msg['timestamp'].replace('Z', '+00:00'))
            intel_time = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
            time_diff = (intel_time - novice_time).total_seconds() / 60
            print(f"  Time difference: {time_diff:.1f} minutes after noviceai's message")
            break
    
    if not found_intel:
        print("  ❌ intellectronica's message not found in this channel")
        
        # Show all authors who have messages
        print("\n📊 Message authors in this channel:")
        authors = {}
        for msg in raw_data['messages']:
            author = msg['author']['name']
            authors[author] = authors.get(author, 0) + 1
        
        # Sort by message count
        sorted_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
        for author, count in sorted_authors[:20]:
            print(f"  {author}: {count} messages")
            
        if 'intellectronica' in authors:
            print(f"\n  intellectronica has {authors['intellectronica']} messages in this channel")
            
            # Show all of intellectronica's messages
            print("\n📝 All intellectronica messages:")
            for i, msg in enumerate(raw_data['messages']):
                if 'intellectronica' in msg['author']['name']:
                    print(f"\n  Message {i+1}:")
                    print(f"    Content: {msg['content'][:200]}...")
                    print(f"    Timestamp: {msg['timestamp']}")
                    if msg.get('reply_to'):
                        print(f"    Reply to: {msg['reply_to']['message_id']}")
        else:
            print("\n  intellectronica has no messages in this channel")

if __name__ == "__main__":
    asyncio.run(debug_threads())