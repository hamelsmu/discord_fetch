#!/usr/bin/env python3
"""Test script to verify GenAIRocks thread example"""

import asyncio
import json
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Direct imports from notebook code
import sys
sys.path.insert(0, '.')

from discord_fetch.core import fetch_discord_msgs

CHANNEL_ID = 1369370266899185746  # The channel ID from the notebook

async def test_genairocks_example():
    print("Fetching Discord data with thread-aware structure...")
    
    # Fetch data
    original, thread_data = await fetch_discord_msgs(
        CHANNEL_ID,
        limit=None,  # Get all messages to ensure we find the example
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
    
    # Search for the GenAIRocks example - try different variations
    found = False
    for i, conv in enumerate(thread_data['conversations']):
        # More flexible search
        author_lower = conv['question']['author'].lower()
        content_lower = conv['question']['content'].lower()
        
        # Look for the exact message content
        if ('slack support channel' in content_lower and
            'we are working on converting the support channel into a ai chatbot' in content_lower):
            
            found = True
            print(f"\n✅ Found the example at conversation #{i+1}!")
            print("\n📝 PARENT MESSAGE:")
            print(f"Author: {conv['question']['author']}")
            print(f"Content: {conv['question']['content']}")
            
            if 'thread' in conv and conv['thread']:
                print(f"\n💬 THREAD REPLIES ({len(conv['thread'])} messages):")
                for j, reply in enumerate(conv['thread'], 1):
                    print(f"\n{j}. {reply['author']}:")
                    print(f"   {reply['content'][:150]}...")
                    
                    if 'intellectronica' in reply['author']:
                        print("   ✅ This is intellectronica's reply - correctly in thread array!")
            else:
                print("\n❌ No thread found for this message")
            
            if 'replies' in conv and conv['replies']:
                print(f"\n📎 DIRECT REPLIES (not in thread): {len(conv['replies'])}")
                for reply in conv['replies']:
                    print(f"  - {reply['author']}: {reply['content'][:50]}...")
            
            # Save the example
            with open('genairocks_thread_example.json', 'w', encoding='utf-8') as f:
                json.dump({
                    "description": "GenAIRocks example with intellectronica's thread reply",
                    "conversation": conv
                }, f, indent=2, ensure_ascii=False)
            
            print("\n💾 Saved example to genairocks_thread_example.json")
            
            # Also search for intellectronica's message
            print("\n🔍 Searching for intellectronica's reply...")
            for j, other_conv in enumerate(thread_data['conversations']):
                if 'intellectronica' in other_conv['question']['author'] and 'data you are indexing' in other_conv['question']['content']:
                    print(f"\nFound intellectronica's message as conversation #{j+1}:")
                    print(f"Content: {other_conv['question']['content'][:200]}...")
                    break
            
            break
    
    if not found:
        print("\n❌ GenAIRocks example not found!")
        print("\nSearching for similar content...")
        
        # Try broader search
        for conv in thread_data['conversations']:
            content_lower = conv['question']['content'].lower()
            if 'slack support channel' in content_lower and 'converting' in content_lower:
                print(f"\nFound possible match by {conv['question']['author']}:")
                print(f"  {conv['question']['content'][:200]}...")
                if 'thread' in conv:
                    print(f"  Has {len(conv['thread'])} thread replies")
                    # Show thread authors
                    print("  Thread authors:", [msg['author'] for msg in conv['thread'][:3]])

if __name__ == "__main__":
    asyncio.run(test_genairocks_example())