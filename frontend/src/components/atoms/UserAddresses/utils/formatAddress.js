const formatAddress = (address) => {
    const city = address.properties?.city ?? '';
    const district = address.properties?.district ?? '';
    const street = address.properties?.street ?? '';
    const house = address.properties?.house ?? '';

    let formattedAddress = '';

    if (city) {
        formattedAddress += `г.${city} `;
    }

    if (district && !(street || house)) {
        formattedAddress += district;
        formattedAddress += ' райн. ';

    }

    if (street && street !== "None") {
        formattedAddress += 'ул.';
        formattedAddress += street;
    }

    if (house && house !== "None") {
        formattedAddress += ' д.';
        formattedAddress += house;
    }

    return formattedAddress;
};


export default formatAddress;