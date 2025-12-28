import asyncio
from apify import Actor
import firebase_admin
from firebase_admin import credentials, db
import random
import time

# --- CONFIGURATION ---
DATABASE_URL = 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'

async def main():
    async with Actor:
        # 1. Pull the JSON data from the Apify UI
        actor_input = await Actor.get_input() or {}
        firebase_key_dict = actor_input.get("firebase_key")
        
        # 2. Safety Check: If the box is empty, stop and warn the user
        if not firebase_key_dict:
            Actor.log.error("CRITICAL: 'firebase_key' field is empty in the Input tab!")
            Actor.log.info("Please paste your key.json contents into the box.")
            return

        try:
            # 3. Initialize Firebase using the Dictionary (No file path needed!)
            if not firebase_admin._apps:
                cred = credentials.Certificate(firebase_key_dict)
                firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})
            
            ref = db.reference('/')
            current_cycles = actor_input.get("start_cycles", 469244)

            Actor.log.info("--- CHAKA ENGINE: CONVERGENCE TRIGGERED ---")

            while True:
                current_cycles += random.randint(100, 369)
                new_sig = "%016x" % random.getrandbits(64)

                # Sync to Firebase
                ref.update({
                    "total_cycles_verified": current_cycles,
                    "security_signature": new_sig,
                    "overall_status": "CHAKA_LOCKED",
                    "last_sync": time.strftime("%H:%M:%S")
                })

                Actor.log.info(f"VORTEX UPDATE: {current_cycles} Cycles | Status: LOCKED")
                await asyncio.sleep(1)

        except Exception as e:
            Actor.log.error(f"ENGINE ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())