// Css
import './UserAddresses.css';

// Ext lib
import React from 'react';
import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';

// Utils
import formatAddress from "./utils/formatAddress";


const UserAddresses = ({ addresses, onClick }) => {
  return (
    <div>
      {addresses.map((address, index) => (
        <React.Fragment key={index}>
          <Cell onClick={() => onClick(address)} className="address-cell">
            <Text className="address-text">
            {formatAddress(address)}
            </Text>
          </Cell>
          {index < adresses.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </div>
  );
};

export default UserAddresses;