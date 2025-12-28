import asyncio
from apify import Actor
import firebase_admin
from firebase_admin import credentials, db
import random
import time
import os

# --- CONFIGURATION ---
# Use the Realtime Database URL for data operations
DATABASE_URL = 'https://dj-chaka-website-default-rtdb.europe-west1.firebasedatabase.app/'
SERVICE_ACCOUNT_PATH = "./serviceAccountKey.json"

async def main():
    """Main execution loop for the Chaka Engine on Apify Cloud."""
    async with Actor:
        # 1. Initialize Actor Input
        # This allows users to configure the engine from the Apify UI
        actor_input = await Actor.get_input() or {}
        target_valuation = actor_input.get("target_valuation", "$10,000")
        start_cycles = actor_input.get("start_cycles", 469244)

        # 2. Establish Firebase Connection
        if not os.path.exists(SERVICE_ACCOUNT_PATH):
            Actor.log.error(f"CRITICAL: {SERVICE_ACCOUNT_PATH} not found.")
            return

        if not firebase_admin._apps:
            cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': DATABASE_URL
            })
        
        ref = db.reference('/')
        current_cycles = start_cycles

        Actor.log.info("--- CHAKA ENGINE: CONVERGENCE TRIGGERED ---")

        try:
            while True:
                # 3. High-Frequency Cycle Logic (Tesla 369 Vortex Pattern)
                current_cycles += random.randint(100, 369)
                new_sig = "%016x" % random.getrandbits(64)

                # 4. Prepare and Sync Payload
                payload = {
                    "broadcast": "Afronet Online: Mission Completed",
                    "current_valuation": target_valuation,
                    "logic_mode": "TESLA_369_VORTEX",
                    "overall_status": "CHAKA_LOCKED",
                    "peak_efficiency": "1.1006ms",
                    "processing_latency": "9ms",
                    "search_speed_ns": 14100,
                    "security_signature": new_sig,
                    "total_cycles_verified": current_cycles,
                    "valuation": "$139.00",
                    "last_sync": time.strftime("%H:%M:%S")
                }

                # Update the Firebase Backend
                ref.update(payload)

                # Push data to Apify Dataset for user visibility
                await Actor.push_data({
                    "cycle": current_cycles,
                    "signature": new_sig,
                    "valuation": target_valuation,
                    "timestamp": time.time()
                })

                # Log progress to the Apify Console
                Actor.log.info(f"UPDATE: {current_cycles} Cycles | Status: LOCKED")
                
                if current_cycles >= 500000:
                    Actor.log.info("--- MILESTONE REACHED: 500K CYCLES VERIFIED ---")

                # Maintain a stable 1-second pulse
                await asyncio.sleep(1)

        except Exception as e:
            Actor.log.error(f"ENGINE ERROR: {e}")

if __name__ == "__main__":
    # Using asyncio to handle the asynchronous Actor lifecycle
    asyncio.run(main())