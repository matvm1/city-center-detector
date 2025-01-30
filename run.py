from dotenv import load_dotenv
from app import create_app
from app.image_service import initialize_gee, get_satellite_image
from flask import render_template, redirect, request
from app.geocoder import get_coordinates

load_dotenv(override=True)

app = create_app()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_landsat_img")
def get_landsat_image():
    initialize_gee()

    lat, lon = get_coordinates(request.args.get('city'),
                               request.args.get('state'))

    # Check if the coordinates are valid
    if (lat, lon) == (None, None):
        print("Could not find the coordinates for the city.")
        return

    city_landsat_img_url = get_satellite_image(lat, lon)

    if not city_landsat_img_url:
        print(f"Error getting satellite image: {e}")
        return redirect("/")

    return render_template("city_center.html",
                           city_landsat_img_url=city_landsat_img_url)


if __name__ == "__main__":
    app.run(debug=True)
