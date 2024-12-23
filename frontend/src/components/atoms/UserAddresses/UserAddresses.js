// Css
import './UserAddresses.css';

// Ext lib
import React from 'react';
import {Button, Cell, Divider, Text} from '@telegram-apps/telegram-ui';

// State
import AddressesStore from "../../../state_management/stores/AddressesStore";
import defAddressStore from "../../../state_management/stores/DefAddressStore";
import MainPageModalsStore from "../../../state_management/stores/MianPageModalsStateStore";

// Handlers
import GetHandleAddressClick from "./utils/handleAddressClick";
import GetDeleteAddress from "./utils/GetDeleteAddress";

import Icon24Trash from "../../_icons/Icon24Trash";


// Utils
import formatAddress from "./utils/formatAddress";

const UserAddresses = ({}) => {
  const { Addresses, removeAddress } = AddressesStore()
  const { setDefAddress } = defAddressStore();
  const { setModalState } = MainPageModalsStore()

  const handleAddressClick = GetHandleAddressClick(setModalState, setDefAddress);
  const DeleteAddress = GetDeleteAddress(removeAddress);

  // Возможно под замену
  if (Addresses.length === 0) {
    return (
        <div>
          <Cell classsName="address-cell">
            <Text className="address-text">
              Тут пока пусто :)
            </Text>
          </Cell>
        </div>
    )
  }

  return (
    <div>
      {Addresses.map((address, index) => (
        <React.Fragment key={index}>

          <Cell
              onClick={() => {handleAddressClick(address)}}
              className="address-cell"
              after={
            <Button
                mode={"plain"}
                onClick={async (event) => {
                  console.log("Нажата кнопка");
                  event.stopPropagation();
                  await DeleteAddress(address)
                }
            }
            >
              <Icon24Trash className="address-icon"/>
            </Button>
              }
          >

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