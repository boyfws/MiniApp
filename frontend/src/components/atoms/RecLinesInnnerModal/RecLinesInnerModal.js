// Css
import './RecLinesInnerModal.css'

// Ext lib
import { Cell, Divider, Text } from '@telegram-apps/telegram-ui';
import React from 'react';

// Utils
import sliceAndFill from "./utils/sliceAndFill";


const screenHeight = window.innerHeight;

const targetHeight = screenHeight * 0.65;
  
const modalOptionsHeight = getComputedStyle(document.documentElement)
  .getPropertyValue('--modal-options-height');
  
const blockHeight = parseFloat(modalOptionsHeight);
  
const RECOMM_LENGTH = Math.ceil(targetHeight / blockHeight);


const RecLinesInnerModal = ({ recommendations, onClick }) => {
    return (
      <div>
        {sliceAndFill(recommendations, RECOMM_LENGTH).map((recom, index) => (
          <React.Fragment key={index}>
            <Cell onClick={() => onClick(recom)} className="recom-cell">
              <Text className="address-text">
              {recom}
              </Text>
            </Cell>
            {(index < RECOMM_LENGTH - 1) && (recom !== "")  && <Divider />}
          </React.Fragment>

        ))}
      </div>
    );
  };
  
  export default RecLinesInnerModal;