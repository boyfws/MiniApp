// Css
import './UserAddresses.css';

// Ext lib
import React from 'react';
import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';

// State
import AddressesStore from "../../../state_management/stores/AddressesStore";


// Utils
import formatAddress from "./utils/formatAddress";


const UserAddresses = ({ onClick }) => {
  const { Addresses } = AddressesStore()

  return (
    <div>
      {Addresses.map((address, index) => (
        <React.Fragment key={index}>
          <Cell onClick={() => onClick(address)} className="address-cell">
            <Text className="address-text">
            {formatAddress(address)}
            </Text>
          </Cell>
          {index < Addresses.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </div>
  );
};

export default UserAddresses;