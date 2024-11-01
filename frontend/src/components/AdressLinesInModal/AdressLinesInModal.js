import React from 'react';
import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';
import './AdressLinesInModal.css';

const formatAdress = (address) => {
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

  if (street) {
    formattedAddress += 'ул.';
    formattedAddress += street;
  }

  if (house) {
    formattedAddress += ' д.';
    formattedAddress += house;
  }

  return formattedAddress;
};




const AdressLinesInModal = ({ adresses, onClick }) => {
  return (
    <div>
      {adresses.map((address, index) => (
        <React.Fragment key={index}>
          <Cell onClick={() => onClick(address)} classname="address-cell">
            <Text className="address-text">
            {formatAdress(address)}
            </Text>
          </Cell>
          {index < adresses.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </div>
  );
};

export default AdressLinesInModal;