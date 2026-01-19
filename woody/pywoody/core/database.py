import asyncio
import threading
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from ..objects.guard import Guard

class Database:
    def __init__(self, uri):
        self.uri = uri
        self._client = None
        self.db = None        
        self.db_name = None  
        self.collection = None 
        self.loop = None
        self.thread = None

    @property
    async def client(self):
        """Ensures the client is always created on the active loop."""
        current_loop = asyncio.get_running_loop()
        
        if self._client is None:
            self._client = AsyncMongoClient(self.uri)
        return self._client

    def use(self, db_name, collection=None):
        self.db_name = db_name
        if collection:
            self.collection = collection

    # --- CRUD Operations ---
    async def get_all(self, query=None, coll=None, db_name=None):
        cli = await self.client 
        database = cli[db_name or self.db_name]
        target = database[coll or self.collection]
        return await target.find(query or {}).to_list(length=None)

    async def get_one(self, query=None, coll=None, db_name=None):
        """Returns a single document or None."""
        cli = await self.client
        database = cli[db_name or self.db_name]
        target = database[coll or self.collection]
        return await target.find_one(query or {})

    async def save_one(self, data, coll=None, db_name=None):
        cli = await self.client
        database = cli[db_name or self.db_name]
        target = database[coll or self.collection]
        return await target.insert_one(data)

    async def update(self, query, data, coll=None, db_name=None):
        """Updates matching documents using $set."""
        cli = await self.client
        database = cli[db_name or self.db_name]
        target = database[coll or self.collection]
        return await target.update_many(query, {"$set": data})

    # --- 2. Utility Methods ---
    async def list_projects(self):
        """Returns a list of all database names on the server."""
        cli = await self.client 
        dbs = await cli.list_database_names()
        return [d for d in dbs if d not in ['admin', 'config', 'local']]
    
    async def ensure_unique(self, field_name, coll=None, db_name=None):
        """Creates a unique index. Returning silent success to prevent log bloat."""
        cli = await self.client
        database = cli[db_name or self.db_name]
        target = database[coll or self.collection]
        
        try:
            await target.create_index(field_name, unique=True)
            return {"status": "ok", "message": f"Index on {field_name} verified."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # --- 3. The Execution Engine ---
    def start_ui(self):
        if self.loop: return 
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()

    def stop_ui(self):
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
            if self.thread: self.thread.join(timeout=1)
            self.loop, self.thread = None, None

    def shutdown(self):
        self.stop_ui()
        try: asyncio.run(self.client.close())
        except: pass 

    def run(self, task, callback=None):
        if self.loop and self.loop.is_running():
            async def wrapper():
                try:
                    res = await task
                    if callback: callback(res)
                    return res
                except Exception as e:
                    error_data = {"status": "error", "message": str(e)}
                    if callback: callback(error_data)
                    return error_data

            future = asyncio.run_coroutine_threadsafe(wrapper(), self.loop)
            
            if threading.current_thread() != self.thread:
                try:
                    return future.result(timeout=5)
                except Exception as e:
                    return None
        else:
            return asyncio.run(task)

# --- INITIALIZATION ---
guard = Guard()
db = None

def get_db():
    global db
    if db is None:
        addr = guard._preferences.get("mongodb_address") if guard._preferences else None
        if addr:
            db = Database(uri=addr)
            db.start_ui() 
    return db