#!/usr/bin/env python3
"""Verify the GenAIRocks/intellectronica conversation structure"""

import asyncio
import json
from dotenv import load_dotenv
load_dotenv()

from discord_fetch.core import fetch_discord_msgs

CHANNEL_ID = 1369370266899185746

async def verify_structure():
    print("Verifying the conversation structure...\n")
    
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
    
    # Find the conversation
    for conv in thread_data['conversations']:
        if 'noviceai' in conv['question']['author'] and 'slack support' in conv['question']['content']:
            print("✅ Found the conversation!")
            print("\nStructure:")
            print(json.dumps(conv, indent=2))
            
            # Verify it matches the expected structure
            print("\n✅ Verification:")
            print(f"- Parent message by: {conv['question']['author']} (shown as GenAIRocks in Discord)")
            print(f"- Parent content: {conv['question']['content'][:100]}...")
            
            if 'thread' in conv and conv['thread']:
                print(f"- Thread has {len(conv['thread'])} messages")
                for i, msg in enumerate(conv['thread']):
                    if 'intellectronica' in msg['author']:
                        print(f"- Message {i+1} is intellectronica's reply ✅")
                        print(f"  Content preview: {msg['content'][:150]}...")
            
            # Save the verified structure
            with open('verified_conversation_structure.json', 'w') as f:
                json.dump({
                    "description": "GenAIRocks/noviceai conversation with intellectronica's thread reply",
                    "conversation": conv
                }, f, indent=2)
            
            print("\n💾 Saved verified structure to verified_conversation_structure.json")
            break

if __name__ == "__main__":
    asyncio.run(verify_structure())