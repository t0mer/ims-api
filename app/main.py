from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Dict, Any
from weatheril import WeatherIL

app = FastAPI(
    title="IMS Weather API",
    description="FastAPI wrapper for py-weatheril - Israel Meteorological Service API",
    version="1.0.0"
)

# Pydantic models for request/response
class ForecastResponse(BaseModel):
    days: List[Dict[str, Any]]

class CurrentWeatherResponse(BaseModel):
    data: Dict[str, Any]

# Location mapping from IMS API (updated from https://ims.gov.il/he/locations_info)
LOCATIONS = {
    1: "ירושלים", 2: "תל-אביב, חוף", 3: "חיפה", 4: "ראשון לציון",
    5: "פתח תקווה", 6: "אשדוד", 7: "נתניה", 8: "באר שבע",
    9: "בני ברק", 10: "חולון", 11: "רמת גן", 12: "אשקלון",
    13: "רחובות", 14: "בת ים", 15: "בית שמש", 16: "כפר סבא",
    17: "הרצליה", 18: "חדרה", 19: "מודיעין-מכבים-רעות", 20: "רמלה",
    21: "רעננה", 22: "מודיעין עילית", 23: "רהט", 24: "הוד השרון",
    25: "גבעתיים", 26: "קריית אתא", 27: "נהריה", 28: "ביתר עילית",
    29: "אום אל-פחם", 30: "קריית גת", 31: "אילת", 32: "ראש העין",
    33: "עפולה", 34: "נס ציונה", 35: "עכו", 36: "אלעד",
    37: "רמת השרון", 38: "כרמיאל", 39: "יבנה", 40: "טבריה",
    41: "טייבה", 42: "קריית מוצקין", 43: "שפרעם", 44: "נוף הגליל",
    45: "קריית ים", 46: "קריית ביאליק", 47: "קריית אונו", 48: "מעלה אדומים",
    49: "אור יהודה", 50: "צפת", 51: "נתיבות", 52: "דימונה",
    53: "טמרה", 54: "סח'נין", 55: "יהוד-מונוסון", 56: "באקה אל גרבייה",
    57: "אופקים", 58: "גבעת שמואל", 59: "טירה", 60: "ערד",
    61: "מגדל העמק", 62: "שדרות", 63: "ערבה", 64: "נשר",
    65: "קריית שמונה", 66: "יקנעם עילית", 67: "כפר קאסם", 68: "כפר יונה",
    69: "קלנסווה", 70: "קריית מלאכי", 71: "מעלות-תרשיחא", 72: "טירת כרמל",
    73: "אריאל", 74: "אור עקיבא", 75: "בית שאן", 76: "מצפה רמון",
    77: "לוד", 78: "נצרת", 79: "קצרין", 80: "עין גדי",
    81: "גני תקווה", 82: "באר יעקב", 83: "מע'אר", 84: "תל אביב-יפו",
    
    # National Parks and Tourist Sites (200+ range)
    200: "מבצר נמרוד", 201: "נחל חרמון - בניאס", 202: "תל דן", 203: "נחל שניר",
    204: "חרשת טל", 205: "נחל עיון", 206: "חולה", 207: "תל חצור",
    208: "אכזיב", 209: "מבצר יחיעם", 210: "ברעם", 211: "נחל עמוד",
    212: "כורזים", 213: "כפר נחום", 214: "מג'רסה", 215: "בריכת המשושים",
    216: "יהודיה", 217: "גמלא", 218: "כורסי", 219: "חמת טבריה",
    220: "ארבל", 221: "עין אפק", 222: "ציפורי", 223: "חי בר כרמל",
    224: "פארק הכרמל", 225: "בית שערים", 226: "משמר הכרמל", 227: "נחל מערות",
    228: "דור הבונים", 229: "תל מגידו", 230: "כוכב הירדן", 231: "מעיין חרוד",
    232: "בית אלפא", 233: "גן השלושה", 235: "נחל תנינים", 236: "קיסריה",
    237: "תל דור", 238: "מרכז להצלת צבים", 239: "בית ינאי", 240: "אפולוניה",
    241: "אפק הירקון", 242: "פלמחים", 243: "קסטל", 244: "עין חמד",
    245: "עיר דויד", 246: "מערת הנטיפים", 248: "בית גוברין", 249: "שער הגיא",
    250: "מגדל צדק", 251: "עין חניה", 252: "סבסטיה", 253: "הר גריזים",
    254: "נבי סמואל", 255: "עין פרת", 256: "עין מבוע", 257: "קאסר אל-יהוד",
    258: "אכסניית השומרוני הטוב", 259: "מנזר אותימיוס", 261: "קומראן", 262: "עינות צוקים",
    263: "הרודיון", 264: "תל חברון", 267: "מצדה", 268: "תל ערד",
    269: "תל באר שבע", 270: "אשכול", 271: "ממשית", 272: "שבטה",
    273: "קבר בן גוריון", 274: "עין עבדת", 275: "עבדת", 277: "חי בר יטבתה",
    278: "חוף האלמוגים",
    
    # Additional locations (700+ range)
    702: "גלגל", 703: "מעלה גילבוע", 704: "רמון-חי רמון", 705: "נאות סמדר",
    706: "הקניון האדום", 707: "חצבה"
}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "IMS Weather API",
        "description": "FastAPI wrapper for py-weatheril",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/locations")
async def get_locations():
    """Get all available locations"""
    return {"locations": LOCATIONS}

@app.get("/weather/current/{location_id}")
async def get_current_weather(
    location_id: int,
    language: str = Query(default="he", description="Language code (he/en)")
):
    """Get current weather analysis for a specific location"""
    try:
        if location_id not in LOCATIONS:
            raise HTTPException(status_code=400, detail="Invalid location ID")
        
        weather = WeatherIL(location_id, language)
        current_data = weather.get_current_analysis()
        
        # Convert Weather object to dictionary
        if hasattr(current_data, '__dict__'):
            weather_dict = vars(current_data)
        else:
            # Fallback: extract known attributes
            weather_dict = {
                "location": getattr(current_data, 'location', None),
                "humidity": getattr(current_data, 'humidity', None),
                "rain": getattr(current_data, 'rain', None),
                "temperature": getattr(current_data, 'temperature', None),
                "wind_speed": getattr(current_data, 'wind_speed', None),
                "feels_like": getattr(current_data, 'feels_like', None),
                "uv": getattr(current_data, 'uv', None),
                "time": getattr(current_data, 'time', None),
                "json_result": getattr(current_data, 'json_result', None)
            }
        
        return CurrentWeatherResponse(data=weather_dict)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/forecast/{location_id}")
async def get_weather_forecast(
    location_id: int,
    language: str = Query(default="he", description="Language code (he/en)")
):
    """Get 5-day weather forecast for a specific location"""
    try:
        if location_id not in LOCATIONS:
            raise HTTPException(status_code=400, detail="Invalid location ID")
        
        weather = WeatherIL(location_id, language)
        forecast_data = weather.get_forecast()
        
        # Convert forecast object to dictionary
        forecast_dict = []
        for day in forecast_data.days:
            day_dict = {
                "date": day.date.isoformat() if hasattr(day.date, 'isoformat') else str(day.date),
                "location": day.location,
                "day": day.day,
                "weather": day.weather,
                "minimum_temperature": day.minimum_temperature,
                "maximum_temperature": day.maximum_temperature,
                "maximum_uvi": day.maximum_uvi,
                "description": day.description,
                "hours": []
            }
            
            # Add hourly data
            for hour in day.hours:
                hour_dict = {
                    "hour": hour.hour,
                    "weather": hour.weather,
                    "temperature": hour.temperature
                }
                day_dict["hours"].append(hour_dict)
            
            forecast_dict.append(day_dict)
        
        return ForecastResponse(days=forecast_dict)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ims-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
