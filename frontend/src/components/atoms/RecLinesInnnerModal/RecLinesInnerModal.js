// Css
import './RecLinesInnerModal.css'

// Ext lib
import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';
import React from 'react';
import { useHistory } from "react-router-dom";

// Stores
import DefAddressStore from "../../../state_management/stores/DefAddressStore";
import MainPageModalsStore from "../../../state_management/stores/MianPageModalsStateStore";
import AddressesStore from "../../../state_management/stores/AddressesStore";

// Utils
import sliceAndFill from "./utils/sliceAndFill";
import GetHandleAddressRecClick from './utils/handleAddressRecomClick';

const screenHeight = window.innerHeight;

const targetHeight = screenHeight * 0.65;
  
const modalOptionsHeight = getComputedStyle(document.documentElement)
  .getPropertyValue('--modal-options-height');
  
const blockHeight = parseFloat(modalOptionsHeight);
  
const RECOMM_LENGTH = Math.ceil(targetHeight / blockHeight);


const RecLinesInnerModal = ({ recommendations }) => {
    const { setModalState } = MainPageModalsStore()
    const history = useHistory();
    const { addAddress } = AddressesStore()
    const { setDefAddress } = DefAddressStore()

    const handleRecClick = GetHandleAddressRecClick(setModalState, history, addAddress, setDefAddress)

    return (
      <div>
        {sliceAndFill(recommendations, RECOMM_LENGTH).map((recom, index) => (
          <React.Fragment key={index}>
            <Cell
                onClick={async () => {await handleRecClick(recom[1])}}
                className="recom-cell">
              <Text className="address-text">
              {recom[0]}
              </Text>
            </Cell>
            {(index < RECOMM_LENGTH - 1) && (recom[0] !== "")  && <Divider />}
          </React.Fragment>

        ))}
      </div>
    );
  };
  
  export default RecLinesInnerModal;