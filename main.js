class Province {
    constructor(name, owner, layer) {
        this.name = name;
        this.owner = owner;
        this.color = defaultFillColor;
        this.layer = layer;
    }

    set setColor(newColor) {
        this.color = newColor;

        if (newColor == defaultFillColor) {
            this.layer.setStyle({
                fillColor: newColor,
                color: newColor,
                fillOpacity: 0.6
            });
        }
        else {
            this.layer.setStyle({
                fillColor: newColor,
                color: newColor,
                fillOpacity: 0.0
            });
        }
    }
}

const provinces = {};
const defaultFillColor = "grey";
const defaultColor = "#00000000";

const map = L.map("map").setView([20, 0], 2);
map.setMaxBounds(map.getBounds());

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

await fetch("provinces.topojson")
    .then(response => response.json())
    .then(data => {
        let convertedData = topojson.feature(data, data.objects["provinces.geo"])

        L.geoJSON(convertedData, {
            style: {
                color: defaultColor,
                fillColor: defaultFillColor,
                weight: 0,
                opacity: 0.5,
                fillOpacity: 0.0
            },
            onEachFeature: (feature, layer) => {
                const province = new Province(feature.properties.NAME, 0, layer);
                provinces[feature.properties.ID] = province;
                
                layer.on("click", (e) => {
                    if (province.color != defaultFillColor) {
                        province.setColor = defaultFillColor;
                    }
                    else {
                        province.setColor = document.getElementById("color-input").value;
                    }
                });

                layer.on("mouseover", function (e) {
                    layer.setStyle({
                        fillOpacity: 0.7
                    });
                });

                layer.on("mouseout", function (e) {
                    if (province.color == defaultFillColor) {
                        layer.setStyle({
                            fillOpacity: 0.0
                        });
                    }
                    else {
                        layer.setStyle({
                            fillOpacity: 0.6
                        });
                    }
                });
            }
        }).addTo(map);
    })
    .catch(error => console.error('Error loading GeoJSON:', error));
