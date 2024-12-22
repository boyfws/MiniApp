// Css
import './RecLinesAddAddressPage.css'

// Ext lib
import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';
import React from 'react';
import { useHistory } from "react-router-dom";

// Stores
import DefAddressStore from "../../../state_management/stores/DefAddressStore";
import MainPageModalsStore from "../../../state_management/stores/MianPageModalsStateStore";
import AddressesStore from "../../../state_management/stores/AddressesStore";

// Utils
import prepareArrayWithRecom from "./utils/PrepareArrayWithRecom";
import GetHandleAddressRecClick from './utils/handleAddressRecomClick';


const RecLinesAddAddressPage = ({ recommendations }) => {
    const { setModalState } = MainPageModalsStore()
    const history = useHistory();
    const { addAddress } = AddressesStore()
    const { setDefAddress } = DefAddressStore()

    const handleRecClick = GetHandleAddressRecClick(setModalState, history, addAddress, setDefAddress)

    return (
      <div>
        {prepareArrayWithRecom(recommendations).map((recom, index) => (
          <React.Fragment key={index}>
            <Cell
                onClick={async () => {await handleRecClick(recom[1])}}
                className="recom-cell">
              <Text className="address-text">
              {recom[1].full_name}
              </Text>
            </Cell>
            {(index < recommendations.length - 1) && <Divider />}
          </React.Fragment>

        ))}
      </div>
    );
  };
  
  export default RecLinesAddAddressPage;