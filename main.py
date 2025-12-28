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
        # 1. Fetch input from Apify UI
        actor_input = await Actor.get_input() or {}
        
        # Pull the JSON key from the Input field named "firebase_key"
        firebase_key_json = actor_input.get("firebase_key")
        target_valuation = actor_input.get("target_valuation", "$10,000")
        start_cycles = actor_input.get("start_cycles", 469244)

        # 2. Safety Check: If the key isn't in the Input tab, stop here
        if not firebase_key_json:
            Actor.log.error("CRITICAL: Firebase key missing in Input tab! Please paste the JSON there.")
            return

        try:
            # 3. Initialize Firebase using the JSON object directly
            if not firebase_admin._apps:
                cred = credentials.Certificate(firebase_key_json)
                firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})
            
            ref = db.reference('/')
            current_cycles = start_cycles
            Actor.log.info("--- CHAKA ENGINE: CONVERGENCE TRIGGERED ---")

            while True:
                current_cycles += random.randint(100, 369)
                new_sig = "%016x" % random.getrandbits(64)

                # Sync to Firebase
                ref.update({
                    "total_cycles_verified": current_cycles,
                    "security_signature": new_sig,
                    "current_valuation": target_valuation,
                    "last_sync": time.strftime("%H:%M:%S"),
                    "overall_status": "CHAKA_LOCKED"
                })

                # Push to Apify Dataset
                await Actor.push_data({"cycle": current_cycles, "signature": new_sig})
                Actor.log.info(f"UPDATE: {current_cycles} Cycles | Status: LOCKED")
                
                await asyncio.sleep(1)

        except Exception as e:
            Actor.log.error(f"ENGINE ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())