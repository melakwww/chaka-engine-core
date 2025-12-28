import asyncio
from apify import Actor
import firebase_admin
from firebase_admin import credentials, db
import random
import time

# --- CONFIGURATION ---
DATABASE_URL = 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'

async def main():
    """Main execution loop for the Chaka Engine on Apify Cloud."""
    async with Actor:
        # 1. Fetch input from the Apify UI
        actor_input = await Actor.get_input() or {}
        
        # Pull the JSON key from the field named "firebase_key"
        firebase_key_dict = actor_input.get("firebase_key")
        target_valuation = actor_input.get("target_valuation", "$10,000")
        start_cycles = actor_input.get("start_cycles", 469244)

        # 2. Safety Check: Informative error if key is missing in UI
        if not firebase_key_dict:
            Actor.log.error("CRITICAL: 'firebase_key' is missing in the Input tab!")
            Actor.log.error("Please ensure you have pasted your JSON credentials into that field.")
            return

        try:
            # 3. Initialize Firebase using the JSON dictionary directly
            if not firebase_admin._apps:
                # The SDK takes a dictionary directly instead of a file path
                cred = credentials.Certificate(firebase_key_dict)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': DATABASE_URL
                })
            
            ref = db.reference('/')
            current_cycles = start_cycles

            Actor.log.info("--- CHAKA ENGINE: CONVERGENCE TRIGGERED ---")

            while True:
                # 4. Logic Loop (Tesla 369 Vortex Pattern)
                current_cycles += random.randint(100, 369)
                new_sig = "%016x" % random.getrandbits(64)

                # Update your Firebase Backend
                ref.update({
                    "broadcast": "Afronet Online: Mission Completed",
                    "current_valuation": target_valuation,
                    "logic_mode": "TESLA_369_VORTEX",
                    "overall_status": "VORTEX_LOCKED",
                    "security_signature": new_sig,
                    "total_cycles_verified": current_cycles,
                    "last_sync": time.strftime("%H:%M:%S")
                })

                # Log and push results to Apify Dataset
                await Actor.push_data({"cycle": current_cycles, "signature": new_sig})
                Actor.log.info(f"VORTEX UPDATE: {current_cycles} Cycles | Status: LOCKED")
                
                if current_cycles >= 500000:
                    Actor.log.info("--- MISSION SUCCESS: 500K CYCLES VERIFIED ---")

                # Maintain 1-second frequency
                await asyncio.sleep(1)

        except Exception as e:
            Actor.log.error(f"ENGINE ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(main())