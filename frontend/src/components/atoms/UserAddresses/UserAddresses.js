// Css
import './UserAddresses.css';

// Ext lib
import React from 'react';
import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';

// State
import AddressesStore from "../../../state_management/stores/AddressesStore";
import defAddressStore from "../../../state_management/stores/DefAddressStore";
import MainPageModalsStore from "../../../state_management/stores/MianPageModalsStateStore";

// Handlers
import GetHandleAddressClick from "./utils/handleAddressClick";


// Utils
import formatAddress from "./utils/formatAddress";


const UserAddresses = ({ }) => {
  const { Addresses } = AddressesStore()
  const { setDefAddress } = defAddressStore();
  const { setModalState } = MainPageModalsStore()

  const handleAddressClick = GetHandleAddressClick(setModalState, setDefAddress);

  return (
    <div>
      {Addresses.map((address, index) => (
        <React.Fragment key={index}>
          <Cell onClick={() => {handleAddressClick(address)}} className="address-cell">
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