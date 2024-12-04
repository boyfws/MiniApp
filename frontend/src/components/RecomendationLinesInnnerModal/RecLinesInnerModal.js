import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';
import React from 'react';
import './RecLinesInnerModal.css'


function sliceAndFill(array, size, filler) {
    const sliced = array.slice(0, size);
    
    while (sliced.length < size) {
      sliced.push(filler);
    }
  
    return sliced;
  }


const screenHeight = window.innerHeight;

const targetHeight = screenHeight * 0.65;
  
const modalOptionsHeight = getComputedStyle(document.documentElement)
  .getPropertyValue('--modal-options-height');
  
const blockHeight = parseFloat(modalOptionsHeight);
  
const RECOM_LENGTH = Math.ceil(targetHeight / blockHeight);

const filler = ""


const RecLinesInnerModal = ({ recomendations, onClick }) => {
    return (
      <div>
        {sliceAndFill(recomendations, RECOM_LENGTH, {"full_name":filler}).map((recom, index) => (
          <React.Fragment key={index}>
            <Cell onClick={() => onClick(recom)} className="recom-cell">
              <Text className="address-text">
              {recom.full_name}
              </Text>
            </Cell>
            {(index < RECOM_LENGTH - 1) && (recom.full_name != filler)  && <Divider />}
          </React.Fragment>

        ))}
      </div>
    );
  };
  
  export default RecLinesInnerModal;