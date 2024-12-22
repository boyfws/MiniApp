const PreapareGeoJsonForDisplay = (GeoJson) => {
    const address = GeoJson.properties;

    return `${address.city} ${address.street} ${address.house}`
    // Предполагается, что у реста есть это все эти свойства

}

export default PreapareGeoJsonForDisplay;