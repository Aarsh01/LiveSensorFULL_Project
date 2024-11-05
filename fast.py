from fastapi import FastAPI, HTTPException

app = FastAPI()

indian_places = {
    'delhi': ['Red Fort', 'Qutub Minar', 'India Gate'],
    'mumbai': ['Gateway of India', 'Marine Drive', 'Elephanta Caves'],
    'jaipur': ['Hawa Mahal', 'Amber Fort', 'City Palace'],
    'varanasi': ['Kashi Vishwanath Temple', 'Ghats of Ganges', 'Sarnath'],
    'goa': ['Baga Beach', 'Calangute Beach', 'Dudhsagar Falls']
}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Indian Places API! Use /get_items/{name} to get places."}

@app.get("/get_items/{name}")
async def get_items(name: str):
    items = indian_places.get(name.lower())
    if items is None:
        raise HTTPException(status_code=404, detail="Place not found")
    return {"items": items}
