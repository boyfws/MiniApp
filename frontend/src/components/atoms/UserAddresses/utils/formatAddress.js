const formatAddress = (address) => {
    const city = address.properties?.city ?? '';
    const district = address.properties?.district ?? '';
    const street = address.properties?.street ?? '';
    const house = address.properties?.house ?? '';

    let formattedAddress = '';

    if (city) {
        formattedAddress += `${city} `;
    }

    if (district && !(street || house)) {
        formattedAddress += district;

    }

    if (street && street !== "None") {
        formattedAddress += street;
    }

    if (house && house !== "None") {
        formattedAddress += ' д.';
        formattedAddress += house;
    }

    return formattedAddress;
};


export default formatAddress;