const PreapareGeoJsonForDisplay = (GeoJson) => {
    const address = GeoJson.properties;

    return `г. ${address.city} ${address.street} ${address.house}`
    // Предполагается, что у реста есть это все эти свойства

}

export default PreapareGeoJsonForDisplay;