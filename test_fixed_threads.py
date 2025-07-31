#!/usr/bin/env python3
"""Test the fixed thread fetching"""

import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from discord_fetch.core import fetch_discord_msgs

CHANNEL_ID = 1369370266899185746

async def test_fixed_threads():
    print("Testing fixed thread fetching...")
    
    # Fetch with thread structure
    original, thread_data = await fetch_discord_msgs(
        CHANNEL_ID,
        limit=None,
        save_original=False,
        save_simplified=False,
        print_summary=False,
        emit_to_stdout=False,
        use_thread_structure=True
    )
    
    if not thread_data or not original:
        print("❌ Failed to fetch data")
        return
    
    print(f"✓ Fetched {len(thread_data['conversations'])} conversations")
    print(f"✓ Found {len(original['threads'])} threads")
    
    # Look for the specific thread
    novice_msg_id = '1400192229334712452'
    
    # Check in threads
    if novice_msg_id in original['threads']:
        thread = original['threads'][novice_msg_id]
        print(f"\n✅ Found thread with ID matching noviceai's message!")
        print(f"Thread name: {thread['name']}")
        print(f"Parent message ID: {thread['parent_message_id']}")
        print(f"Messages in thread: {len(thread['messages'])}")
        
        # Look for intellectronica
        for msg in thread['messages']:
            if 'intellectronica' in msg['author']['name']:
                print(f"\n✅ Found intellectronica's reply in thread!")
                print(f"Author: {msg['author']['name']}")
                print(f"Content: {msg['content'][:300]}...")
                
                # Now check if it's in the organized data
                for conv in thread_data['conversations']:
                    if 'noviceai' in conv['question']['author'] and 'slack support' in conv['question']['content']:
                        print(f"\n✅ Found conversation in organized data!")
                        print(f"Question by: {conv['question']['author']}")
                        print(f"Has thread: {'thread' in conv}")
                        if 'thread' in conv:
                            print(f"Thread messages: {len(conv['thread'])}")
                            for tmsg in conv['thread']:
                                if 'intellectronica' in tmsg['author']:
                                    print(f"✅ intellectronica's reply is properly in thread array!")
                        break
                break
    else:
        print(f"\n❌ Thread {novice_msg_id} not found in threads")
        print("\nChecking all thread IDs...")
        for tid in list(original['threads'].keys())[:10]:
            print(f"  {tid}")

if __name__ == "__main__":
    asyncio.run(test_fixed_threads())