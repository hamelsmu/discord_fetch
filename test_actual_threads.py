#!/usr/bin/env python3
"""Test with actual thread data from the channel"""

import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from discord_fetch.core import fetch_discord_msgs

CHANNEL_ID = 1369370266899185746

async def test_actual_threads():
    print("Testing thread-aware structure with actual channel data...")
    
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
    
    if not thread_data:
        print("❌ Failed to fetch data")
        return
    
    print(f"✓ Fetched {len(thread_data['conversations'])} conversations")
    
    # Find conversations with threads
    conversations_with_threads = [
        conv for conv in thread_data['conversations'] 
        if 'thread' in conv and conv['thread']
    ]
    
    print(f"\n📊 Statistics:")
    print(f"  Total conversations: {len(thread_data['conversations'])}")
    print(f"  Conversations with threads: {len(conversations_with_threads)}")
    
    if conversations_with_threads:
        print(f"\n✅ Showing first 3 conversations with threads:")
        
        for i, conv in enumerate(conversations_with_threads[:3], 1):
            print(f"\n--- Example {i} ---")
            print(f"Parent message by {conv['question']['author']}:")
            print(f"  {conv['question']['content'][:150]}...")
            
            print(f"\nThread has {len(conv['thread'])} messages:")
            for j, thread_msg in enumerate(conv['thread'][:3], 1):
                print(f"  {j}. {thread_msg['author']}: {thread_msg['content'][:100]}...")
        
        # Save examples
        examples = {
            "description": "Examples of conversations with Discord threads",
            "total_conversations": len(thread_data['conversations']),
            "conversations_with_threads": len(conversations_with_threads),
            "examples": conversations_with_threads[:3]
        }
        
        with open('thread_examples.json', 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)
        
        print("\n💾 Saved examples to thread_examples.json")
    else:
        print("\n❌ No conversations with threads found in this channel")
    
    # Also check for conversations with direct replies
    conversations_with_replies = [
        conv for conv in thread_data['conversations']
        if 'replies' in conv and conv['replies']
    ]
    
    print(f"\n📊 Conversations with direct replies: {len(conversations_with_replies)}")
    
    if conversations_with_replies:
        print("\nExample of direct reply:")
        example = conversations_with_replies[0]
        print(f"Parent: {example['question']['author']}: {example['question']['content'][:100]}...")
        print(f"Reply: {example['replies'][0]['author']}: {example['replies'][0]['content'][:100]}...")

if __name__ == "__main__":
    asyncio.run(test_actual_threads())